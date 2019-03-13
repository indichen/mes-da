#!/usr/bin/env bash

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ -z "$1" ]; then
  echo "Usage: $0 [model]"
  exit 1
fi

export model=$1

pushd "${script_dir}"

echo "[da-service] Deploying ${model}..."
echo "[da-service] CI_COMMIT_SHORT_SHA=${CI_COMMIT_SHORT_SHA}"
echo "{\"date\": \"$(date +%F)\", \"commit\": \"${COMMIT_ID}\"}" > ${model}/release.json
tar zcf ${TARBALL} -C ${model}/ -T ${model}/deploy.txt release.json || exit 1
rm ${model}/release.json
scp ${TARBALL} root@${DA_SERVER}:/tmp || exit 1
ssh root@${DA_SERVER} "cd /tmp && mkdir -p ${DA_SERVER_WEBROOT}/${model}/${COMMIT_ID} && tar zxf ${TARBALL} -C ${DA_SERVER_WEBROOT}/${model}/${COMMIT_ID} && cd ${DA_SERVER_WEBROOT}/${model}/ && rm -f latest && ln -s ${COMMIT_ID} latest" || exit 1
echo "[da-service] Done"

popd