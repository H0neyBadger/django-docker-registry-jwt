from docker.io/fedora

RUN dnf -y update && dnf -y clean all --enablerepo=*
RUN dnf -y install python3 && dnf -y clean all --enablerepo=*

ENV WORKDIR="/app/"

# build args 
# ARG OWNER_UID
# ARG OWNER_GID

WORKDIR "${WORKDIR}"

# Run service as non-root user
# RUN groupadd --gid "${OWNER_GID}" "django"
# RUN useradd --uid "${OWNER_UID}" \
#    --gid "${OWNER_GID}" \
#    "django"

# USER django

# copy django sources
ADD "./django-docker-registry-jwt/" "${WORKDIR}"
ADD "./requirements.txt" "${WORKDIR}"
ADD "./container/*" "/usr/bin/"

# Create env
RUN pip3 install psycopg2-binary
RUN pip3 install -r ./requirements.txt

VOLUME "/etc/django/"
ENTRYPOINT ["/usr/bin/entrypoint.sh"]
CMD ["/usr/bin/run_django.sh"]
