#
# VERSION               0.0.1

FROM ubuntu:14.04

MAINTAINER Eric Busboom "eric@clarinova.com"

VOLUME /cache
VOLUME /notebooks

#RUN apt-get install -y curl
#RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/clarinova/ambry/master/support/install-ubuntu.sh)"
#RUN ambry config install -f

RUN apt-get install -y openssh-server
RUN mkdir /var/run/sshd
RUN echo 'root:screencast' |chpasswd



EXPOSE 22

CMD    ["/usr/sbin/sshd", "-D"]