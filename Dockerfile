ARG KEYCLOAK_VERSION="26.1.2"

FROM registry.access.redhat.com/ubi9 AS ubi-micro-build
ARG KEYCLOAK_VERSION

# avoid error of ubi registry
# [MIRROR] tzdata-2023c-1.el9.noarch.rpm: Interrupted by header callback: Inconsistent server data, reported file Content-Length: 864432, repository metadata states file length: 864888 (please report to repository maintainer) 
ADD tzdata-2023d-1.el9.noarch.rpm /root/
ADD https://github.com/keycloak/keycloak/releases/download/${KEYCLOAK_VERSION}/keycloak-${KEYCLOAK_VERSION}.tar.gz /tmp/

RUN mkdir -p /mnt/rootfs/etc/yum.repos.d && \
    cp /etc/yum.repos.d/ubi.repo /mnt/rootfs/etc/yum.repos.d/ && \
    dnf install --installroot /mnt/rootfs /root/tzdata-2023d-1.el9.noarch.rpm --releasever 9 --setopt install_weak_deps=false --nodocs -y
RUN dnf install --installroot /mnt/rootfs python3-pip python3-wheel python3 tar gzip vim --releasever 9 --setopt install_weak_deps=false --nodocs -y && \
    dnf --installroot /mnt/rootfs clean all && \
    rpm --root /mnt/rootfs -e --nodeps setup
# build keycloak
COPY apache-maven-3.9.6-bin.zip /opt/
# COPY keycloak-webauthn-conditional-mediation-kc25.zip /opt/
COPY files/first-stage/UserResource.patch /tmp/

RUN dnf install -y unzip git patch java-21-openjdk java-21-openjdk-devel && \
    cd /opt && \
    unzip apache-maven-3.9.6-bin.zip && \
    export PATH=/opt/apache-maven-3.9.6/bin:$PATH && \
    # unzip keycloak-webauthn-conditional-mediation-kc25.zip && \
    # tar xzf /tmp/keycloak-${KEYCLOAK_VERSION}.tar.gz && \
    # cd keycloak-webauthn-conditional-mediation-kc25 && \
    # mvn clean package && \
    cd /root && \
    git clone https://github.com/keycloak/keycloak.git -b ${KEYCLOAK_VERSION} && \
    cd keycloak/services && \
    patch src/main/java/org/keycloak/services/resources/admin/UserResource.java /tmp/UserResource.patch && \
    mvn -DskipTests=true clean package

FROM quay.io/keycloak/keycloak:${KEYCLOAK_VERSION} AS builder
ARG KEYCLOAK_VERSION

# Enable health and metrics support
ENV KC_HEALTH_ENABLED=true
ENV KC_METRICS_ENABLED=true

# Configure a database vendor
ENV KC_DB=mysql
# COPY --from=ubi-micro-build /opt/keycloak-webauthn-conditional-mediation-kc25/target/keycloak-webauthn-conditional-mediation.jar /opt/keycloak/providers/
COPY --from=ubi-micro-build /root/keycloak/services/target/keycloak-services-${KEYCLOAK_VERSION}.jar /opt/keycloak/lib/lib/main/org.keycloak.keycloak-services-${KEYCLOAK_VERSION}.jar
WORKDIR /opt/keycloak
# for demonstration purposes only, please make sure to use proper certificates in production instead
# RUN keytool -genkeypair -storepass password -storetype PKCS12 -keyalg RSA -keysize 2048 -dname "CN=s# erver" -alias server -ext "SAN:c=DNS:localhost,IP:127.0.0.1" -keystore conf/server.keystore
RUN /opt/keycloak/bin/kc.sh build

FROM quay.io/keycloak/keycloak:${KEYCLOAK_VERSION}

COPY --from=builder /opt/keycloak/ /opt/keycloak/
COPY --from=ubi-micro-build /mnt/rootfs /

ENV KC_BOOTSTRAP_ADMIN_USERNAME="admin"
ENV KC_BOOTSTRAP_ADMIN_PASSWORD="admin"
# ENV KEYCLOAK_ADMIN="admin"
# ENV KEYCLOAK_ADMIN_PASSWORD="admin"
ENV KC_HOSTNAME_URL="http://localhost:8080"
ENV KC_HOSTNAME_STRICT_BACKCHANNEL=false
ENV KC_DB=mysql

USER root
COPY files/final-stage/realm-export.json /etc
RUN pip install uuid supervisor
COPY files/final-stage/docker-entrypoint.py /usr/bin
COPY files/final-stage/supervisord.conf /etc
RUN mkdir -p /etc/supervisor.d
COPY files/final-stage/keycloak.ini /etc/supervisor.d
RUN chmod +x /usr/bin/docker-entrypoint.py && \
    mkdir -p /opt/keycloak/data/import && \
    chown 1000 /opt/keycloak/data/import

ENTRYPOINT ["/usr/bin/docker-entrypoint.py"]
