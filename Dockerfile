# ---------- Builder Image -----------
# Pull official base image
FROM python:3.9 as Builder

WORKDIR /root/

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/root/.local/bin:${PATH}"

COPY requirements.txt /root/

# Install dependenciesll
RUN pip install --user --upgrade pip
RUN pip install --user --no-cache-dir -r requirements.txt
RUN pip install --user --no-cache-dir uwsgi
RUN pip install --user --no-cache-dir --upgrade certifi
RUN rm requirements.txt

# ---------- Release Image -----------
# Pull official base image
FROM python:3.7-slim

RUN set -ex \
    && RUN_DEPS=" \
    libpcre3 \
    mime-support \
    postgresql-client \
    libxml2 \
    libjpeg62 \
    libopenjp2-7 \
    libtiff5 \
    gettext \
    libmagic1 \
    " \
    && seq 1 8 | xargs -I{} mkdir -p /usr/share/man/man{} \
    && apt-get update && apt-get install -y --no-install-recommends $RUN_DEPS \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /srv/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy pip package
COPY --from=builder /root/ /root/

# Set ENV
ENV PATH="/root/.local/bin:${PATH}"
ENV DJANGO_SETTINGS_MODULE=digisign.settings
ENV DS_SECRET_KEY=kadevkey
ENV DS_DEBUG=true

ENV DS_EMAIL_HOST='smtp.mailtrap.io'
ENV DS_EMAIL_USER='3c102df6576a22'
ENV DS_EMAIL_PASS='dcc8e4633ebb10'
ENV DS_EMAIL_PORT='2525'

#Copy source to /srv/app
COPY ./src /srv/app

# Manage Command Collectstatic
RUN python manage.py collectstatic --noinput

# Manage Command Compilemessages
RUN python manage.py compilemessages

# Create directory uploads
RUN mkdir /srv/app/uam/uploads

EXPOSE 8000
EXPOSE 8001

CMD ["uwsgi", \
    "--manage-script-name", \
    "--static-map=/static=uam/static", \
    "--static-map=/uploads=uam/uploads", \
    "--static-index=index.html", \
    "--mount=/api/uam=uam.wsgi:application", \
    "--chdir=/srv/app", \
    "--python-path=/srv/app", \
    "--http=0.0.0.0:8000", \
    "--master", \
    "--enable-threads", \
    "--threads=2", \
    "--processes=4", \
    "--stats=0.0.0.0:8001", \
    "--stats-http"]
