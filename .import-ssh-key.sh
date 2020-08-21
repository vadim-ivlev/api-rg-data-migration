#!/bin/bash

# Скрипт используется в .gitlab-ci.yml в процессе непрерывной 
# интеграции на сервере git.rgwork.ru

echo '-----------------importing ssh-key--------------------------'
# import ssh-key
# use key name: deploy_gitupdater_base64
# public key added by user "chagin"
which ssh-agent || ( apt-get update -y && apt-get install openssh-client -y )
eval $(ssh-agent -s)
# Attention! Key need convert in base64 and add in secret variable DEPLOY_RSA_PRIVATE_KEY
ssh-add <(echo "$1" | base64 --decode)
mkdir -p /root/.ssh
echo -e "Host *\n\tStrictHostKeyChecking no\n\n" > ~/.ssh/config
echo "$1" | base64 --decode > /root/.ssh/id_rsa
chmod 600 /root/.ssh/id_rsa && chmod 700 /root/.ssh
