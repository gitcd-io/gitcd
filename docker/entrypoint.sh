#!/bin/bash

ssh-keyscan github.com > $HOME/.ssh/known_hosts

#eval `ssh-agent -s` && \
#    printf "${SSH_KEY_PASSPHRASE}\n" | ssh-add $HOME/.ssh/id_rsa
