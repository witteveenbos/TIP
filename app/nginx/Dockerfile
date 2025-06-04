FROM nginx:stable-alpine
COPY ./config/nginx.conf.template /etc/nginx/templates/default.conf.template
COPY ./config/nginx.conf /etc/nginx/nginx.conf
WORKDIR /app
COPY ./static/502.html 502.html
EXPOSE 80
