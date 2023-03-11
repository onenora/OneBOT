#FROM --platform=$TARGETPLATFORM python:alpine
FROM python:alpine
ENV TZ=Asia/Shanghai
WORKDIR /onebot

RUN  \
    build_pkgs=" gcc libc-dev linux-headers" \
    && apk --no-cache add ${build_pkgs} \
    && apk add --no-cache tzdata gcc libc-dev linux-headers git \
    && git clone https://github.com/onenora/OneBOT /onebot \
    && pip3 install --root-user-action=ignore -r requirements.txt \
    && apk del --no-network ${build_pkgs} \
    && rm -rf /var/cache/apk/*

CMD [ "sh", "-c", "/onebot/__main__.py" ]
