# Stage 01 - Build Vue Application
FROM node:20 as vue-builder
WORKDIR /app
# Copying package.json and package-lock.json
COPY service/frontend/wand-zero/package*.json ./
# Installing Node.js dependencies
RUN npm install
# Copying the rest of the frontend application
COPY service/frontend/wand-zero/ .
# Building the Vue application
RUN npm run build

# Stage 02 - Build FastAPI Application
FROM python:3.12-alpine as fastapi-builder
WORKDIR /app

# Installing Poetry
RUN apk add --no-cache curl && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s $HOME/.local/bin/poetry /usr/local/bin/poetry

# Copying the Python project files
COPY pyproject.toml poetry.lock* ./

# Installing Python dependencies with Poetry without creating a virtual environment
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

# Copying the FastAPI application code
COPY service/backend .

# Copying the Vue build artifacts from the vue-builder stage
COPY --from=vue-builder /app/dist /app/app/web

# Preparing the start script and creating a non-root user
COPY start.sh /start.sh
RUN chmod +x /start.sh && \
    adduser --system --no-create-home wand

USER wand
EXPOSE 80
CMD ["/start.sh"]
