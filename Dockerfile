FROM rhscl/python-27-rhel7

MAINTAINER Ten "wataxiwax@gmail.com"

EXPOSE 8000

COPY . /opt/app-root/src

CMD /bin/bash -c 'python2 -u web.py'
