#!/bin/bash



groupmod -g $GID gitcd
usermod -u $UID gitcd

#ssh-keyscan github.com > $HOME/.ssh/known_hosts

#eval `ssh-agent -s` && \
#    printf "${SSH_KEY_PASSPHRASE}\n" | ssh-add $HOME/.ssh/id_rsa


exec "$@"
