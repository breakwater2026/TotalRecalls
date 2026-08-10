# TotalRecalls marketing site — Cloud Run / any container host
# Serves static files from site/ via nginx.
# Build type in Cloud Build: Dockerfile (this file).

FROM nginx:1.27-alpine

# Cloud Run sends traffic to $PORT (default 8080). Our nginx listens on 8080.
ENV PORT=8080

# Remove stock default site
RUN rm -f /etc/nginx/conf.d/default.conf

COPY deploy/nginx.conf /etc/nginx/conf.d/default.conf
COPY site/ /usr/share/nginx/html/

# Non-root is nice-to-have; nginx official image runs master as root then workers as nginx.
# Cloud Run is fine with this default.

EXPOSE 8080

# Smoke-check config at build time
RUN nginx -t

CMD ["nginx", "-g", "daemon off;"]
