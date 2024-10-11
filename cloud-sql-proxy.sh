#!/bin/bash

# Copyright 2016 Google, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This init script installs a cloud-sql-proxy on each node in the cluster, and
# uses that proxy to expose TCP proxies of CloudSQL PostgreSQL instances.

set -euo pipefail

# Variables for PostgreSQL setup
readonly POSTGRES_PORT='5432'
readonly POSTGRES_ADMIN_USER='postgres'
readonly POSTGRES_DRIVER='org.postgresql.Driver'
readonly POSTGRES_PROTO='postgresql'
readonly JARS_DIR='/usr/lib/spark/jars'

# Download required JARs
gsutil cp gs://dataproc-staging-us-central1-353241962082-fj6qfu9g/postgresql-42.3.1.jar $JARS_DIR
gsutil cp gs://dataproc-staging-us-central1-353241962082-fj6qfu9g/jdbc-socket-factory-core-1.20.1.jar $JARS_DIR
gsutil cp gs://dataproc-staging-us-central1-353241962082-fj6qfu9g/google-auth-library-oauth2-http-1.24.1.jar $JARS_DIR
function err() {
  echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')] [$(hostname)]: ERROR: $*" >&2
  return 1
}

function log() {
  echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')] [$(hostname)]: INFO: $*" >&2
}

# Proxy binary and directories
readonly PROXY_DIR='/var/run/cloud_sql_proxy'
readonly PROXY_BIN='/usr/local/bin/cloud_sql_proxy'
readonly INIT_SCRIPT='/usr/lib/systemd/system/cloud-sql-proxy.service'
readonly PROXY_LOG_DIR='/var/log/cloud-sql-proxy'

# Metadata retrieval
ADDITIONAL_INSTANCES="$(/usr/share/google/get_metadata_value attributes/additional-cloud-sql-instances || echo '')"
readonly ADDITIONAL_INSTANCES

function get_proxy_flags() {
  local proxy_instances_flags=''
  
  # Pass additional PostgreSQL instances to the proxy
  if [[ -n "${ADDITIONAL_INSTANCES}" ]]; then
    proxy_instances_flags+=" -instances_metadata=instance/attributes/additional-cloud-sql-instances"
  fi

  echo "${proxy_instances_flags}"
}

function install_cloud_sql_proxy() {
  echo 'Installing Cloud SQL Proxy ...' >&2
  # Install proxy.
  wget -nv --timeout=30 --tries=5 --retry-connrefused \
    https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64
  mv cloud_sql_proxy.linux.amd64 ${PROXY_BIN}
  chmod +x ${PROXY_BIN}

  mkdir -p ${PROXY_DIR}
  mkdir -p ${PROXY_LOG_DIR}

  local proxy_flags
  proxy_flags="$(get_proxy_flags)"

  # Install proxy as systemd service for reboot tolerance.
  cat <<EOF >${INIT_SCRIPT}
[Unit]
Description=Google Cloud SQL Proxy
After=local-fs.target network-online.target

[Service]
Type=simple
ExecStart=/bin/sh -c '${PROXY_BIN} \
  -dir=${PROXY_DIR} \
  ${proxy_flags} >> /var/log/cloud-sql-proxy/cloud-sql-proxy.log 2>&1'

[Install]
WantedBy=multi-user.target
EOF
  chmod a+rw ${INIT_SCRIPT}

  log 'Cloud SQL Proxy installation succeeded'
}

function start_cloud_sql_proxy() {
  log 'Starting Cloud SQL proxy ...'
  systemctl enable cloud-sql-proxy
  systemctl start cloud-sql-proxy ||
    err 'Unable to start cloud-sql-proxy service'

  log 'Cloud SQL Proxy started'
  log 'Logs can be found in /var/log/cloud-sql-proxy/cloud-sql-proxy.log'
}

function install_postgres_cli() {
  if command -v psql >/dev/null; then
    log "POSTGRES CLI is already installed"
    return
  fi

  log "Installing POSTGRES CLI ..."
  if command -v apt >/dev/null; then
    apt update && apt install postgresql-client -y
  elif command -v yum >/dev/null; then
    yum -y update && yum -y install postgresql
  fi
  log "POSTGRES CLI installed"
}

function validate() {
  if [[ -z "${ADDITIONAL_INSTANCES}" ]]; then
    err 'No Cloud SQL PostgreSQL instances to proxy'
  fi
}

function update_master() {
  install_cloud_sql_proxy
  start_cloud_sql_proxy
}

function update_worker() {
  install_cloud_sql_proxy
  start_cloud_sql_proxy
}

function main() {
  local role
  role="$(/usr/share/google/get_metadata_value attributes/dataproc-role)"

  validate

  if [[ "${role}" == 'Master' ]]; then
    update_master
  else
    update_worker
  fi

  log 'All done'
}

main
