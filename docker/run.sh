#!/bin/bash

docker run -it\
    -v $(pwd):/home/gitcd/app\
    -v $HOME/.gitcd:/home/gitcd/.gitcd\
    -v $SSH_AUTH_SOCK:/ssh-agent\
    -e SSH_AUTH_SOCK="/ssh_agent"\
    gitcd:latest\
    $1
