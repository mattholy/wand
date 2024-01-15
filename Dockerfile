# Stage 01 - Build Vue
FROM node:20 as vue
WORKDIR /app
COPY service/frontend/wand-zero/package*.json ./
RUN npm install
COPY service/frontend/wand-zero/ .
RUN npm run build

# Stage 02 - Build FastAPI
FROM python:3.11
WORKDIR /app

ARG VERSION
ENV WD_VERSION=${VERSION}

COPY service/backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY service/backend .
COPY --from=vue /app/dist /app/app/web

COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 80

CMD ["/start.sh"]
