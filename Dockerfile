# TotalRecalls site V2 — Astro static build
# Multi-stage: build Astro -> serve static files
# Cloud Run: port via $PORT env, HTTP/2 OFF (H2C = 502), bind 0.0.0.0:$PORT

FROM node:22-alpine AS build
WORKDIR /src
COPY site/package*.json ./
RUN npm ci --legacy-peer-deps
COPY site/ ./
RUN npm run build

FROM alpine:3
RUN apk add --no-cache ca-certificates python3
COPY --from=build /src/dist /var/www
EXPOSE 8080
CMD ["python3", "-c", "import http.server,os; port=int(os.environ.get('PORT','8080')); http.server.ThreadingHTTPServer(('0.0.0.0',port),lambda *a,**kw: http.server.SimpleHTTPRequestHandler(*a,directory='/var/www',**kw)).serve_forever()"]