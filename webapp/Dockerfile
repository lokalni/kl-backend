FROM node:latest

RUN apt-get update && apt-get install -y \
    bash \
    g++ \
    inotify-tools \
    yarn

RUN yarn global add @vue/cli

COPY ["package.json", "yarn.lock", "/code/"]
WORKDIR /code/

# Separate cached layer
RUN yarn install
COPY . /code

# TODO: Inject some vars?
ARG BACKEND_URL=__BACKEND_URL__
ENV BACKEND_URL ${BACKEND_URL}

# Prepare build for prod
RUN npm run build

# EXPOSE Webpack ports
EXPOSE 8080
# EXPOSE 3001

ENTRYPOINT []
