# LocalStack EventStudio

Visual UI to develop and debug event driven AWS services

You need a LocalStack Pro license to install and use extension and activate it via the variable `LOCALSTACK_AUTH_TOKEN` either in localstack config file or as an environment variable.

## Install extension to LocalStack

You can either add EXTENSION_AUTO_INSTALL="git+https://github.com/localstack/localstack-extension-event-studio/" to your localstack config file or run the following command:

```bash
localstack extensions install "git+https://<personal-private-access-token>@github.com/localstack/localstack-extension-event-studio/#egg=eventstudio"
```

Run the extension from the docker container via the following command:

```bash
PROVIDER_OVERRIDE_EVENTS=v2 EXTRA_CORS_ALLOWED_ORIGINS=* localstack start
```

you can see the extension running at https://localhost.localstack.cloud:4566/_extension/eventstudio/events directly
or via the LocalStack Web App under https://app.localstack.cloud/inst/default/extensions/manage

## Install local development version

First you need to create the `.env.development.local` file in the root of the project based on the `.env.example` file.

To install the extension into localstack in developer mode, you will need Python 3.11, and create a virtual environment in the extensions project, example using virtualenv:

```bash
virtualenv -p python3.11 .venv
source .venv/bin/activate
```

You will also need to install [yarn](https://yarnpkg.com/getting-started/install) as package manager if you haven't already, with corepack enabled.
Furthermore you need to have localstack and localstack-pro correctly set up in their respective source folders.
In the newly generated project, simply run

```bash
make install-dev
```

To check that the extension is installed correctly, you can run the following command:

```bash
make list-extension
```

You can then start LocalStack with `EXTENSION_DEV_MODE=1` to load all enabled extensions:

```bash
make start-extension
```

which is equivalent to:

```bash
EXTENSION_DEV_MODE=1 PROVIDER_OVERRIDE_EVENTS=v2 EXTRA_CORS_ALLOWED_ORIGINS=* localstack start
```

to access the frontend via the React dev server, you can run:

```bash
make start-frontend
```

You can access the frontend served from the extension directly under https://localhost.localstack.cloud:4566/_extension/eventstudio/events
or via the React dev server under http://localhost:3000/.

## Deploying sample application

The default sample application used for development and testing:

```bash
make deploy-test-stack && make put-event
```

Second sample application:

```bash
cd samples/fintech_demo
cdklocal bootstrap
cdklocal deploy
```
