FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/
ADD sites-enabled  /etc/nginx/sites-enabled
