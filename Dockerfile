FROM alpine:3.19.1

RUN apk add python3 && apk add py3-yaml && apk add git 
RUN adduser -D argo-mm-generator
USER argo-mm-generator
WORKDIR /app
COPY --chown=argo-mm-generator ./argo-mm-generator.py ./argo-mm-generator.py
COPY --chown=argo-mm-generator ./wiki-updater.sh ./wiki-updater.sh
RUN chmod +x /app/wiki-updater.sh

RUN mkdir /app/tmp

CMD ["/app/wiki-updater.sh"]

