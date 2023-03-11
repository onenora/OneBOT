FROM python:alpine
WORKDIR /onebot
# The libc6-compat dependency is required to use the host's docker commands
RUN  \
    build_pkgs=" gcc libc-dev linux-headers" \
    && apk --no-cache add ${build_pkgs} \
    && apk add --no-cache tzdata gcc libc-dev linux-headers git \
    && git clone https://github.com/onenora/OneBOT /onebot \
    && pip3 install --root-user-action=ignore -r requirements.txt --no-cache-dir \
    && mkdir -p /onebot/data \
    && apk del --no-network ${build_pkgs} \
    && rm -rf .git .github .gitignore Dockerfile install.sh LICENSE README.md requirements.txt \
    && rm -rf /var/cache/apk/*

VOLUME /onebot/data

ENTRYPOINT ["python3", "-u", "main.py"]
