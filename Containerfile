FROM public.ecr.aws/docker/library/golang:1.19-alpine3.16 AS hugo-builder

WORKDIR /src

RUN apk upgrade --update-cache \
    && apk add ca-certificates git gcc g++ musl-dev \
    && git clone --depth 1 'https://github.com/gohugoio/hugo'

WORKDIR /src/hugo

#ENV CC=clang
#ENV CXX=clang
ENV CGO_ENABLED=1 

RUN go build --tags extended

FROM public.ecr.aws/docker/library/alpine:3.16 AS python-base

RUN apk upgrade --no-cache \
    && apk add ca-certificates git python3

FROM python-base AS python-builder

RUN apk upgrade --no-cache \
    && apk add py3-pip make

ENV VIRTUAL_ENV="/opt/venv"

WORKDIR /src

RUN --mount=type=bind,source=.,target=/src,readwrite \
    python3 -m venv "${VIRTUAL_ENV}" \
    && . "${VIRTUAL_ENV}/bin/activate" \
    && pip install -U pip \
    && pip install -U build \
    && make build \
    && make install

FROM python-base

RUN apk upgrade --no-cache \
    && apk add --no-cache libstdc++ libgcc openssh-client

COPY --from=hugo-builder --chown=root:root --chmod=0755 /src/hugo/hugo /usr/bin/hugo

ENV VIRTUAL_ENV="/opt/venv"

COPY --from=python-builder "${VIRTUAL_ENV}" "${VIRTUAL_ENV}"

ARG UID=10000
ARG GID=10001

RUN mkdir -p /var/lib/hugo \
    && addgroup -g "${GID}" -S _hugo \
    && adduser \
        -u "${UID}" \
        -h /var/lib/hugo \
        -g 'hugo privsep user' \
        -s /sbin/nologin \
        -G _hugo \
        -S _hugo \
    && chown -R _hugo:_hugo /var/lib/hugo

VOLUME ["/var/lib/hugo"]

WORKDIR "/var/lib/hugo"

USER _hugo

EXPOSE 8443

ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

ENTRYPOINT ["python3"]

CMD ["-m", "hwwwook"]

# vim:ft=dockerfile
