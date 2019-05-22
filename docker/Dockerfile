FROM walser/python

RUN apk update
RUN apk add git openssh

RUN addgroup -S gitcd && adduser -S gitcd -G gitcd

USER gitcd
ENV PATH="/home/gitcd/.local/bin:${PATH}"

RUN mkdir -p /home/gitcd/.ssh/
RUN touch /home/gitcd/.ssh/config
RUN chown -R gitcd: /home/gitcd/.ssh/
RUN echo "Host github.com"  > /home/gitcd/.ssh/config
RUN echo "  Hostname ssh.github.com" >> /home/gitcd/.ssh/config
RUN echo "  Port 443" >> /home/gitcd/.ssh/config
RUN pip3 install --user --upgrade gitcd
RUN mkdir -p /home/gitcd/app

COPY entrypoint.sh /entrypoint.sh

WORKDIR /home/gitcd/app

ENTRYPOINT ["/entrypoint.sh"]

