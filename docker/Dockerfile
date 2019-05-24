FROM walser/python

RUN apk update
RUN apk add git openssh shadow

RUN addgroup -S gitcd && adduser -S gitcd -G gitcd

ENV UID=1000
ENV GID=1000



RUN ln -s /home/gitcd/.local/bin/git-cd /usr/local/bin/git-cd


#USER gitcd

RUN mkdir -p /home/gitcd/.ssh/
RUN touch /home/gitcd/.ssh/config
RUN chown -R gitcd: /home/gitcd/.ssh/
RUN echo "Host github.com"  > /home/gitcd/.ssh/config
RUN echo "  Hostname ssh.github.com" >> /home/gitcd/.ssh/config
RUN echo "  Port 443" >> /home/gitcd/.ssh/config

#this is pretty bad actually, i need to install the current branch here
RUN pip3 install --user --upgrade gitcd

RUN mkdir -p /home/gitcd/app

WORKDIR /home/gitcd/app

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]