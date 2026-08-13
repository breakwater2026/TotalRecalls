# TotalRecalls site V2 — Astro static build served by python http.server
# Build type: Dockerfile (Cloud Build). Port 8080 via $PORT.
# HTTP/2 end-to-end must stay OFF on Cloud Run (H2C vs HTTP/1.1 = 502).

FROM node:22-alpine AS build
WORKDIR /src
COPY site/package*.json ./
RUN npm ci
COPY site/ ./
RUN npm run build

FROM python:3.12-alpine
ENV PORT=8080 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /srv
COPY --from=build /src/dist/ /srv/
RUN adduser -D -u 10001 web && chown -R web:web /srv
USER web
EXPOSE 8080
CMD ["sh", "-c", "echo \"TotalRecalls site v2 on 0.0.0.0:${PORT}\" && exec python -m http.server \"${PORT}\" --bind 0.0.0.0"]
