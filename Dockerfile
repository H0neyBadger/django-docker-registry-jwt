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
ADD . "${WORKDIR}"

# Create env
RUN pip3 install -r ./requirements_prd.txt

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "wsgi"]

