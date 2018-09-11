FROM centos:7

# SSH
RUN (cd /lib/systemd/system/sysinit.target.wants/; for i in *; do [ $i == \
systemd-tmpfiles-setup.service ] || rm -f $i; done); \
rm -f /lib/systemd/system/multi-user.target.wants/*;\
rm -f /etc/systemd/system/*.wants/*;\
rm -f /lib/systemd/system/local-fs.target.wants/*; \
rm -f /lib/systemd/system/sockets.target.wants/*udev*; \
rm -f /lib/systemd/system/sockets.target.wants/*initctl*; \
rm -f /lib/systemd/system/basic.target.wants/*;\
rm -f /lib/systemd/system/anaconda.target.wants/*;
VOLUME [ "/sys/fs/cgroup" ]
RUN yum -y install openssh-server openssh-clients
RUN echo root:pass | chpasswd

CMD ["/usr/sbin/sshd", "-D"]

# Upodate OS (IUP - Inline with Upstream Stable)
# more info here - https://ius.io/
RUN yum -y install https://centos7.iuscommunity.org/ius-release.rpm \
&&  yum -y clean all

# Install Python 3 and OS dependencies
RUN yum -y install \
	gcc \
	python36u \
	python36u-pip \
	python36u-devel \
	mariadb-devel \
&&  yum -y clean all

# Add aliases
RUN echo "alias py3='python3.6'" >> ~/.bashrc

# PIP Requirements
COPY requirements.txt ./

RUN pip3.6 install --upgrade pip
RUN pip3.6 install --upgrade setuptools
RUN pip3.6 install -r requirements.txt

WORKDIR /usr/src/app
