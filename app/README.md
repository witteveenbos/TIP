# Getting Started

We work using LTAP. Local runs on dev containers (see below). All TAP environments are automatically built containers that are hosted on Azure webapp instances. In addition, we have a bleeding edge Integration Testing (IT) environment.

## Start Dev Container

Visual Studio Code will detect that you are working in a Dev Container, click "Reopen in Container" to start the Dev container. After you reopen visual studio code in a devcontainer you are ready to start the backend and frontend, run the following commands in two seperate terminals:

```
cd frontend
npm run dev

cd src
python manage.py runserver
```

For the frontend Prettier and EsLin1t is used. Make sure you installed these extenstions in your VSCode. These extensions are automatically installed in the dev container:

```
Name: ESLint
Id: dbaeumer.vscode-eslint
Description: Integrates ESLint JavaScript into VS Code.
Publisher: Microsoft
VS Marketplace Link: https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint

---

Name: Prettier - Code formatter
Id: esbenp.prettier-vscode
Description: Code formatter using prettier
Publisher: Prettier
VS Marketplace Link: https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode

```

## Configure stuff inside the container

If you want for example do an Django migration, you can just run any command from the terminal in the correct folder, for example:

```
cd src
python manage.py makemigrations
```

## Admin

To see the data that is saved in the database, you can take a look in the admin.
To do so, you have to create a local superuseraccount:

```
cd src
python manage.py createsuperuser
```

After finishing all the steps, you can login on localhost:8000/wt/admin

## Wagtail

Wagtail can be accessed at localhost:8000/wt/cms

## Frontend components

The frontend uses ShadCN components. These are located at frontend/components/ui. You can simply add components through:

```
npx shadcn-ui@latest add [name components]
```
