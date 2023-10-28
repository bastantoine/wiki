FROM python:3.11 AS python-build

RUN pip install --upgrade pip
RUN pip install poetry

WORKDIR /app
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry config virtualenvs.create false --local
RUN poetry install

COPY sources sources
COPY templates templates

COPY main.py .
RUN python main.py --ignored-dirs '.obsidian,.git' --verbose sources . build templates

FROM node:16 AS node-build

WORKDIR /app
COPY package.json .
COPY package-lock.json .
RUN npm install

COPY .vitepress/config.mts .vitepress/config.mts
COPY --from=python-build /app/build wiki
RUN cp wiki/links.json .vitepress/links.json
RUN npm run docs:build

FROM nginx:1.25.3-alpine
COPY --from=node-build /app/.vitepress/dist /usr/share/nginx/html
EXPOSE 80
