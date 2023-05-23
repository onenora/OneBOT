#FROM --platform=$TARGETPLATFORM alpine
FROM alpine

WORKDIR /TMBot
RUN apk add --no-cache tzdata python3 python3-dev py3-pip gcc libc-dev linux-headers git && \
    git clone https://github.com/noreph/TMBot /TMBot && \
    pip3 install --root-user-action=ignore -r requirements.txt && \
    rm -rf /var/cache/apk/*

ENV TZ=Asia/Shanghai \
    API_ID=0000000 \
    API_HASH=00000000000000000000000000000000

CMD [ "sh", "-c", "/TMBot/__main__.py" ]
