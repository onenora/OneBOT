#!/usr/bin/with-contenv bash

welcome () {
    echo 
    echo "onebot Docker 。"
    echo "配置即将开始"
    echo 
    sleep 2
}

red='\033[0;31m'
green='\033[0;32m'
yellow='\033[0;33m'
plain='\033[0m'


check_and_create_config(){
if [ ! -f /onebot/data/config.ini ]; then

mkdir -p "/onebot/data" >/dev/null 2>&1

read -p "Please input your api_id：" api_id
read -p "Please input your api_hash：" api_hash

cat > /onebot/data/config.ini <<EOF
[pyrogram]
api_id=${api_id}
api_hash=${api_hash}
[plugins]
root=plugins
EOF
fi
}
login () {
    echo
    echo "下面进行程序运行。"
    echo "请在账户授权完毕后，按 Ctrl + C 使 Docker 在后台模式下运行。"
    echo
    sleep 2
    echo "Hello world!" > /onebot/data/install.lock
    python -u main.py
    exit 0
}

main () {
    cd /onebot/data
    if [ ! -s "/onebot/data/install.lock" ]; then
        welcome
        configure
        login
    else
        if [ ! -f "/onebot/data/pagermaid.session" ]; then
            welcome
            configure
        fi
        login
    fi
}

main