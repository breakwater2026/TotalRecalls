# TotalRecalls marketing site for Cloud Run
# Build type: Dockerfile (this file). Port: $PORT (default 8080).

FROM nginx:1.27-alpine

ENV PORT=8080

RUN rm -f /etc/nginx/conf.d/default.conf

COPY deploy/nginx.conf /etc/nginx/conf.d/default.conf
COPY deploy/docker-entrypoint.sh /docker-entrypoint-tr.sh
COPY site/ /usr/share/nginx/html/

RUN chmod +x /docker-entrypoint-tr.sh \
    && nginx -t \
    && ls -la /usr/share/nginx/html/

EXPOSE 8080

# Use our entrypoint (not the stock nginx docker-entrypoint chain alone)
STOPSIGNAL SIGQUIT
CMD ["/docker-entrypoint-tr.sh"]
