#!/usr/bin/env python3
"""Run the app with uvicorn"""

from os import environ
from ssl import PROTOCOL_TLS_SERVER

import uvicorn  # type: ignore

from . import api

if __name__ == "__main__":
    uvicorn.run(
        api,
        host="127.0.0.1",
        port=8000,
        ssl_version=PROTOCOL_TLS_SERVER,
        ssl_keyfile=environ.get("SSL_KEYFILE"),
        ssl_certfile=environ.get("SSL_CERTFILE"),
        ssl_cert_reqs=1,
        ssl_ca_certs=environ.get("SSL_CA_CERTS"),
        log_level="debug",
    )
