FROM nginx:latest

RUN apt-get update

# Пробрасываем логи nginx'а в STDOUT
# RUN ln -sf /dev/stdout /var/log/nginx/access.log \
# 	&& ln -sf /dev/stderr /var/log/nginx/error.log

# Порты nginx'а
EXPOSE 8080

# RUN mkdir /app
# WORKDIR /app

# ADD . /app

RUN rm /etc/nginx/conf.d/default.conf
COPY ./compose/nginx/nginx.conf /etc/nginx/conf.d

CMD [ "nginx", "-g", "daemon off;" ]