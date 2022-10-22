#!/bin/bash

set -euxo pipefail

readonly SERVER='http://localhost:8000/gitolite'

readonly REPOSITORY="${REPOSITORY:?}"
readonly SOURCEPATH="${SOURCEPATH:?}"
readonly TARGET="${TARGET:?}"
readonly CACERT="${CACERT:?}"
readonly CERT="${CERT:?}"
readonly KEY="${KEY:?}"

curl \
    --cacert "${CACERT}" \
    --cert "${CERT}" \
    --key "${KEY}" \
    --request POST \
    --header 'accept: application/json' \
    --header 'content-Type: application/json' \
    --data "{
        \"repository\": \"${REPOSITORY}\",
        \"sourcepath\": \"${SOURCEPATH}\",
        \"target\": \"${TARGET}\",
        \"reset\": false
    }" "${SERVER}"
