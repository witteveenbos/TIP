# Manual deployment to GR acceptance

This guide deploys TIP from a local checkout to the GR acceptance environment.
It does not deploy PNH or production.

## Targets

| Component | Build context | Image | Azure target |
| --- | --- | --- | --- |
| Frontend | `app/frontend` | `c25050243cr.azurecr.io/frontend:accept-gr` | Container App `frontend-accept-app` |
| Backend | `app/src` | `c25050243cr.azurecr.io/backend:accept-gr` | Container App `backend-accept-app` |
| Hail/rekenkern | `hail` | `c25050243cr.azurecr.io/data:accept-gr` | Web App `accept-data-app-gr`, sitecontainer `accept-data-app` |

All targets use subscription `Business Servers Production Environment`, resource
group `C2608-0156`, and registry `c25050243cr`. The nginx image is not part of
the current GR acceptance deployment.

## Prepare

Docker and the Azure CLI must be installed and authenticated.

```bash
cd /home/tamk/repos/TIP

git branch --show-current
git log -1 --oneline
git status --short

az account set --subscription "Business Servers Production Environment"
az account show --query '{name:name,id:id,user:user.name}' -o json
az acr login --name c25050243cr
docker version

TIP_SUBSCRIPTION="Business Servers Production Environment"
TIP_RESOURCE_GROUP="C2608-0156"
TIP_ACR="c25050243cr"
TIP_REGISTRY="c25050243cr.azurecr.io"
TIP_TAG="accept-gr"
```

Docker includes uncommitted files inside a build context. Prefer deploying a
commit. If the worktree is dirty, review every listed file first.

Build only affected components:

- `app/frontend/` changes require the frontend image.
- `app/src/` changes require the backend image.
- `hail/` changes require the data image.
- Documentation, dev-container, and inactive nginx-only changes need no GR app
  deployment.

If frontend and backend both changed, deploy the backend first.

## Record rollback digests

The `accept-gr` tags are mutable. Capture their current digests before pushing:

```bash
TIP_OLD_FRONTEND_DIGEST=$(az acr manifest show-metadata \
  --registry "$TIP_ACR" --name "frontend:$TIP_TAG" \
  --query digest -o tsv)

TIP_OLD_BACKEND_DIGEST=$(az acr manifest show-metadata \
  --registry "$TIP_ACR" --name "backend:$TIP_TAG" \
  --query digest -o tsv)

TIP_OLD_DATA_DIGEST=$(az acr manifest show-metadata \
  --registry "$TIP_ACR" --name "data:$TIP_TAG" \
  --query digest -o tsv)

printf 'frontend=%s\nbackend=%s\ndata=%s\n' \
  "$TIP_OLD_FRONTEND_DIGEST" \
  "$TIP_OLD_BACKEND_DIGEST" \
  "$TIP_OLD_DATA_DIGEST"
```

Keep these variables until verification is complete.

## Frontend: build and validate

Frontend values are embedded during `next build`. Load
`app/frontend/.env.production` and forward all build arguments:

```bash
set -a
source app/frontend/.env.production
set +a

docker build --pull \
  --build-arg WAGTAIL_API_URL \
  --build-arg NEXT_PUBLIC_WAGTAIL_API_URL \
  --build-arg NEXT_PUBLIC_API_URL \
  --build-arg NEXT_PUBLIC_REKENKERN_API_URL \
  --label "org.opencontainers.image.source-branch=$(git branch --show-current)" \
  --label "org.opencontainers.image.revision=$(git rev-parse HEAD)" \
  -f app/frontend/prod.Dockerfile \
  -t "$TIP_REGISTRY/frontend:$TIP_TAG" \
  app/frontend
```

For direct browser login, `NEXT_PUBLIC_WAGTAIL_API_URL` must contain the full GR
backend URL and the request helper must use `credentials: 'include'`.

```bash
docker run --rm -d \
  --name tip-frontend-smoke \
  -p 127.0.0.1:3001:3000 \
  "$TIP_REGISTRY/frontend:$TIP_TAG"

curl --retry 10 --retry-delay 2 --retry-all-errors --fail \
  http://127.0.0.1:3001/maplibre-gl-csp-worker.js \
  --output /dev/null

docker logs --tail 30 tip-frontend-smoke
docker stop tip-frontend-smoke
```

The first request may reset while Next.js starts; the retry handles that window.

## Backend: build and validate

```bash
docker build --pull \
  --label "org.opencontainers.image.source-branch=$(git branch --show-current)" \
  --label "org.opencontainers.image.revision=$(git rev-parse HEAD)" \
  -f app/src/prod.Dockerfile \
  -t "$TIP_REGISTRY/backend:$TIP_TAG" \
  app/src

docker run --rm --entrypoint python \
  -e DB_NAME=smoke \
  -e DB_USER=smoke \
  -e DB_PASSWORD=smoke \
  -e DB_HOST=127.0.0.1 \
  -e DB_PORT=5432 \
  -e SECRET_KEY=smoke-check \
  -e ALLOWED_HOSTS=localhost \
  -e MEDIA_PATH=/tmp/media \
  -e STATIC_PATH=/tmp/static \
  -e TRUSTED_ORIGINS=https://localhost \
  "$TIP_REGISTRY/backend:$TIP_TAG" \
  manage.py check
```

Review migration files before deployment. The backend entrypoint runs
`python manage.py migrate --noinput` against the acceptance database.

At the time this guide was written, `makemigrations --check --dry-run` reports
pre-existing drift for `futurevision/0005_alter_futurevision_geo_id.py`. Do not
generate migrations during deployment; resolve and review that drift separately.

## Hail: build and validate

```bash
docker build --pull \
  --label "org.opencontainers.image.source-branch=$(git branch --show-current)" \
  --label "org.opencontainers.image.revision=$(git rev-parse HEAD)" \
  -f hail/Dockerfile \
  -t "$TIP_REGISTRY/data:$TIP_TAG" \
  hail

docker run --rm --entrypoint poetry \
  -e REDIS_HOST=localhost \
  -e REDIS_PORT=6379 \
  -e ETM_API_KEY=smoke-check \
  -e SUPER_SECRET_KEY=smoke-check \
  -e TRUSTED_ORIGINS_DATA=http://localhost \
  "$TIP_REGISTRY/data:$TIP_TAG" \
  run python -c \
  "from app import app; from hail.models.scenario import ScenarioDisplay; from pathlib import Path; scenarios = ScenarioDisplay.multiple_from_config(Path('/app/config')); assert scenarios; print(f'routes={len(app.routes)} scenarios={len(scenarios)}')"
```

This does not warm Redis or call the ETM API.

## Push images

Run only commands for rebuilt images:

```bash
docker push "$TIP_REGISTRY/frontend:$TIP_TAG"
docker push "$TIP_REGISTRY/backend:$TIP_TAG"
docker push "$TIP_REGISTRY/data:$TIP_TAG"
```

Confirm each pushed digest as needed:

```bash
az acr manifest show-metadata \
  --registry "$TIP_ACR" --name "frontend:$TIP_TAG" \
  --query '{digest:digest,lastUpdated:lastUpdateTime}' -o json
```

Replace `frontend` with `backend` or `data` for the other images.

## Deploy the backend

```bash
TIP_REVISION_SUFFIX="accept-gr-$(date -u +%Y%m%d%H%M%S)"

az containerapp update \
  --subscription "$TIP_SUBSCRIPTION" \
  --resource-group "$TIP_RESOURCE_GROUP" \
  --name backend-accept-app \
  --image "$TIP_REGISTRY/backend:$TIP_TAG" \
  --revision-suffix "$TIP_REVISION_SUFFIX"

TIP_BACKEND_REVISION=$(az containerapp show \
  --subscription "$TIP_SUBSCRIPTION" \
  --resource-group "$TIP_RESOURCE_GROUP" \
  --name backend-accept-app \
  --query properties.latestRevisionName -o tsv)

az containerapp logs show \
  --subscription "$TIP_SUBSCRIPTION" \
  --resource-group "$TIP_RESOURCE_GROUP" \
  --name backend-accept-app \
  --revision "$TIP_BACKEND_REVISION" \
  --type console --tail 200 --format text
```

Confirm migrations finish and Gunicorn starts, then check the API and traffic:

```bash
curl --fail --max-time 30 \
  'https://backend-accept-app.yellowsea-a6617e80.westeurope.azurecontainerapps.io/wt/api/nextjs/v1/page_relative_urls/' \
  --output /dev/null

az containerapp show \
  --subscription "$TIP_SUBSCRIPTION" \
  --resource-group "$TIP_RESOURCE_GROUP" \
  --name backend-accept-app \
  --query '{latestRevision:properties.latestRevisionName,traffic:properties.configuration.ingress.traffic}' \
  -o json
```

## Deploy Hail

The Web App has a main `accept-data-app` container and a `redis-accept`
sidecar. Update only the main container:

```bash
az webapp sitecontainers update \
  --subscription "$TIP_SUBSCRIPTION" \
  --resource-group "$TIP_RESOURCE_GROUP" \
  --name accept-data-app-gr \
  --container-name accept-data-app \
  --image "$TIP_REGISTRY/data:$TIP_TAG" \
  --target-port 7000 \
  --is-main true

az webapp restart \
  --subscription "$TIP_SUBSCRIPTION" \
  --resource-group "$TIP_RESOURCE_GROUP" \
  --name accept-data-app-gr

az webapp sitecontainers list \
  --subscription "$TIP_SUBSCRIPTION" \
  --resource-group "$TIP_RESOURCE_GROUP" \
  --name accept-data-app-gr \
  --query '[].{name:name,image:image,isMain:isMain,status:status}' \
  -o table

az webapp sitecontainers log \
  --subscription "$TIP_SUBSCRIPTION" \
  --resource-group "$TIP_RESOURCE_GROUP" \
  --name accept-data-app-gr \
  --container-name accept-data-app
```

Verify the API and CORS response:

```bash
curl --fail --max-time 30 \
  --header 'Origin: https://frontend-accept-app.yellowsea-a6617e80.westeurope.azurecontainerapps.io' \
  --dump-header - \
  'https://accept-data-app-gr-fsanhgfteufcfkbm.westeurope-01.azurewebsites.net/list_scenarios/' \
  --output /dev/null
```

Expect HTTP `200` and the frontend URL in `Access-Control-Allow-Origin`.

## Deploy the frontend

```bash
TIP_REVISION_SUFFIX="accept-gr-$(date -u +%Y%m%d%H%M%S)"

az containerapp update \
  --subscription "$TIP_SUBSCRIPTION" \
  --resource-group "$TIP_RESOURCE_GROUP" \
  --name frontend-accept-app \
  --image "$TIP_REGISTRY/frontend:$TIP_TAG" \
  --revision-suffix "$TIP_REVISION_SUFFIX"

TIP_FRONTEND_REVISION=$(az containerapp show \
  --subscription "$TIP_SUBSCRIPTION" \
  --resource-group "$TIP_RESOURCE_GROUP" \
  --name frontend-accept-app \
  --query properties.latestRevisionName -o tsv)

az containerapp revision show \
  --subscription "$TIP_SUBSCRIPTION" \
  --resource-group "$TIP_RESOURCE_GROUP" \
  --name frontend-accept-app \
  --revision "$TIP_FRONTEND_REVISION" \
  --query '{name:name,active:properties.active,health:properties.healthState,provisioning:properties.provisioningState,replicas:properties.replicas}' \
  -o json

az containerapp show \
  --subscription "$TIP_SUBSCRIPTION" \
  --resource-group "$TIP_RESOURCE_GROUP" \
  --name frontend-accept-app \
  --query '{latestRevision:properties.latestRevisionName,traffic:properties.configuration.ingress.traffic}' \
  -o json

az containerapp logs show \
  --subscription "$TIP_SUBSCRIPTION" \
  --resource-group "$TIP_RESOURCE_GROUP" \
  --name frontend-accept-app \
  --revision "$TIP_FRONTEND_REVISION" \
  --type console --tail 100 --format text
```

Smoke-test the frontend and direct backend login transport:

```bash
curl --fail --location --max-time 45 \
  'https://frontend-accept-app.yellowsea-a6617e80.westeurope.azurecontainerapps.io/sv/' \
  --output /dev/null

curl --fail --max-time 30 \
  --header 'Origin: https://frontend-accept-app.yellowsea-a6617e80.westeurope.azurecontainerapps.io' \
  --dump-header - \
  'https://backend-accept-app.yellowsea-a6617e80.westeurope.azurecontainerapps.io/wt/api/nextjs/v1/csrf/' \
  --output /dev/null
```

Expect HTTP `200`, `Access-Control-Allow-Credentials: true`, and the frontend
URL in `Access-Control-Allow-Origin`. Test a real login in the browser; do not
put credentials in shell history.

## Rollback

Use the digest captured before the push. This deploys the exact previous image
even after the `accept-gr` tag moves.

```bash
# Backend
TIP_ROLLBACK_SUFFIX="rollback-$(date -u +%Y%m%d%H%M%S)"
az containerapp update \
  --subscription "$TIP_SUBSCRIPTION" \
  --resource-group "$TIP_RESOURCE_GROUP" \
  --name backend-accept-app \
  --image "$TIP_REGISTRY/backend@$TIP_OLD_BACKEND_DIGEST" \
  --revision-suffix "$TIP_ROLLBACK_SUFFIX"

# Frontend
TIP_ROLLBACK_SUFFIX="rollback-$(date -u +%Y%m%d%H%M%S)"
az containerapp update \
  --subscription "$TIP_SUBSCRIPTION" \
  --resource-group "$TIP_RESOURCE_GROUP" \
  --name frontend-accept-app \
  --image "$TIP_REGISTRY/frontend@$TIP_OLD_FRONTEND_DIGEST" \
  --revision-suffix "$TIP_ROLLBACK_SUFFIX"

# Hail
az webapp sitecontainers update \
  --subscription "$TIP_SUBSCRIPTION" \
  --resource-group "$TIP_RESOURCE_GROUP" \
  --name accept-data-app-gr \
  --container-name accept-data-app \
  --image "$TIP_REGISTRY/data@$TIP_OLD_DATA_DIGEST" \
  --target-port 7000 \
  --is-main true

az webapp restart \
  --subscription "$TIP_SUBSCRIPTION" \
  --resource-group "$TIP_RESOURCE_GROUP" \
  --name accept-data-app-gr
```

An image rollback does not reverse database migrations. Backend migrations must
remain backward-compatible with the previous image. Never reverse an acceptance
database migration automatically during incident rollback.
