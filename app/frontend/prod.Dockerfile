# Install dependencies only when needed
FROM node:20.5.1 AS deps
# When switching from Debian to Apline uncomment the apk command below
# Check https://github.com/nodejs/docker-node/tree/b4117f9333da4138b03a546ec926ef50a31506c3#nodealpine to understand why libc6-compat might be needed.
#RUN apk add --no-cache libc6-compat
WORKDIR /app

# Install dependencies based on the preferred package manager
COPY package.json package-lock.json* ./
RUN npm ci


# Rebuild the source code only when needed
FROM node:20.5.1 AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Next.js collects completely anonymous telemetry data about general usage.
# Learn more here: https://nextjs.org/telemetry
# Uncomment the following line in case you want to disable telemetry during the build.
# ENV NEXT_TELEMETRY_DISABLED 1

# Publish this environment variable at build time
ARG NEXT_PUBLIC_WAGTAIL_API_URL
ARG NEXT_PUBLIC_API_URL
ARG WAGTAIL_API_URL
ARG NEXT_PUBLIC_REKENKERN_API_URL
ENV NEXT_PUBLIC_WAGTAIL_API_URL=${NEXT_PUBLIC_WAGTAIL_API_URL}
ENV NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}
ENV WAGTAIL_API_URL=${WAGTAIL_API_URL}
ENV NEXT_PUBLIC_BASE_URL=${NEXT_PUBLIC_BASE_URL}
ENV NEXT_PUBLIC_REKENKERN_API_URL=${NEXT_PUBLIC_REKENKERN_API_URL}

RUN echo "WAGTAIL_API_URL: $WAGTAIL_API_URL"
RUN echo "NEXT_PUBLIC_API_URL: $NEXT_PUBLIC_API_URL"
RUN echo "NEXT_PUBLIC_WAGTAIL_API_URL: $NEXT_PUBLIC_WAGTAIL_API_URL"
RUN echo "NEXT_PUBLIC_REKENKERN_API_URL: $NEXT_PUBLIC_REKENKERN_API_URL"


RUN npm run build


# Production image, copy all the files and run next
FROM node:20.5.1 AS runner
WORKDIR /app

ENV NODE_ENV production
# Uncomment the following line in case you want to disable telemetry during runtime.
# ENV NEXT_TELEMETRY_DISABLED 1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public

# Automatically leverage output traces to reduce image size
# https://nextjs.org/docs/advanced-features/output-file-tracing
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

# Environment variables must be redefined at run time
ARG NEXT_PUBLIC_WAGTAIL_API_URL
ARG NEXT_PUBLIC_API_URL
ARG WAGTAIL_API_URL
ARG NEXT_PUBLIC_REKENKERN_API_URL
ENV NEXT_PUBLIC_WAGTAIL_API_URL=${NEXT_PUBLIC_WAGTAIL_API_URL}
ENV NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}
ENV WAGTAIL_API_URL=${WAGTAIL_API_URL}
ENV NEXT_PUBLIC_BASE_URL=${NEXT_PUBLIC_BASE_URL}
ENV NEXT_PUBLIC_REKENKERN_API_URL=${NEXT_PUBLIC_REKENKERN_API_URL}


USER nextjs

EXPOSE 3000

ENV PORT 3000
ENV HOSTNAME 0.0.0.0

CMD ["node", "server.js"]
