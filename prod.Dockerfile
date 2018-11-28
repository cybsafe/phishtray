FROM centos:7

# Upodate OS (IUP - Inline with Upstream Stable)
# more info here - https://ius.io/
RUN yum -y install https://centos7.iuscommunity.org/ius-release.rpm \
&&  yum -y clean all

# Install Python 3 and OS dependencies
RUN yum -y install \
	gcc \
	wget \
	python36u \
	python36u-pip \
	python36u-devel \
	mariadb-devel \
&&  yum -y clean all

# Set PYTHONUNBUFFERED so output is displayed in the Docker log
ENV PYTHONUNBUFFERED=1

RUN pip3.6 install --upgrade pip
RUN pip3.6 install --upgrade setuptools

# Set working directory
WORKDIR /usr/src/app

# Install python packages
COPY requirements.txt /usr/src/app
RUN pip3.6 install -r requirements.txt

# Copy project files
COPY . /usr/src/app

# TODO: Update to use a proper web server like gunicorn or uwsgi
ENTRYPOINT exec bash -c "python3.6 manage.py migrate && python3.6 manage.py runserver 0:9000"
