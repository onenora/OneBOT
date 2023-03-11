FROM python:alpine
WORKDIR /onebot
# The libc6-compat dependency is required to use the host's docker commands
RUN  \
    build_pkgs="gcc libc-dev linux-headers python3-dev" \
    && apk --no-cache add ${build_pkgs} \
    && git clone https://github.com/onenora/OneBOT /onebot \
    && pip install --upgrade pip
    && pip install --root-user-action=ignore -r requirements.txt --no-cache-dir \
    && mkdir -p /onebot/data \
    && apk del --no-network ${ build_pkgs} \
    && rm -rf .git .github .gitignore Dockerfile install.sh LICENSE README.md requirements.txt \
    && rm -rf /var/cache/apk/*

VOLUME /onebot/data

ENTRYPOINT ["python3", "-u", "main.py"]
