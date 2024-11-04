#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

# Install flux-core and flux-sched with micromamba
{% include "includes/install-micromamba.sh" %}

# We require munge
{% include "includes/install-munge.sh" %}

# Configure mamba
export MAMBA_ROOT_PREFIX={% if mamba_prefix %}{{ mamba_prefix }}{% else %}/opt/conda{% endif %}
mkdir -p ${MAMBA_ROOT_PREFIX}
eval "$(micromamba shell hook -s posix)"

# Activate the base environment
micromamba activate

# Flux still using old python...
micromamba install python={% if python_version %}{{ python_version }}{% else %}3.11{% endif %} jupyter -c conda-forge --yes
micromamba activate base

# This assumes installing latest pair - we could always change this to
# be a specific version, but I don't see need for that yet.
micromamba install --yes flux-core flux-sched

# Prepare resource system directory
mkdir -p ${MAMBA_ROOT_PREFIX}/etc/flux/system/conf.d
mkdir -p ${MAMBA_ROOT_PREFIX}/etc/flux/system/cron.d
mkdir -p ${MAMBA_ROOT_PREFIX}/etc/flux/system
mkdir -p /var/lib/flux /var/run/flux

# Flux curve.cert
# Ensure we have a shared curve certificate
# This should be added via a config map. If not, we use a template
{% include "includes/ensure-curve-certificate.sh" %}

# /var/lib/flux needs to be owned by the instance owner (root)
# this should already by the case

# Either we are given the device name, or need to discover it.
# For this use case, we are likely given the name
{% if linkname %}
linkname="{{ linkname }}"
{% else %}
# Get the linkname of the device
{% include "includes/write-parse-links-py.sh" %}
linkname=$(python3 /tmp/parse-links.py)
{% endif %}
echo "Found ip link name ${linkname} to provide to flux"

# Create list of brokers for config file
brokers=""
{% for broker in brokers %}{% if loop.index0 != 0 %}brokers="${brokers},{{ broker }}"{% else %}brokers="{{ broker }}"
{% endif %}{% endfor %}

# One node cluster vs. not...
if [[ "$brokers" == "" ]]; then
    echo "No brokers found - this should not happen"
    exit 1
fi

# Generate resources!
flux R encode --hosts="${brokers}" --local > ${MAMBA_ROOT_PREFIX}/etc/flux/system/R

# Show ip addresses for debugging
ip addr

# Write broker.toml
cat <<EOF | tee /tmp/broker.toml
# Allow users other than the instance owner (guests) to connect to Flux
# Optionally, root may be given "owner privileges" for convenience
[access]
allow-guest-user = true
allow-root-owner = true

# Point to resource definition generated with flux-R(1).
# Uncomment to exclude nodes (e.g. mgmt, login), from eligibility to run jobs.
[resource]
path = "${MAMBA_ROOT_PREFIX}/etc/flux/system/R"

# Point to shared network certificate generated flux-keygen(1).
# Define the network endpoints for Flux's tree based overlay network
# and inform Flux of the hostnames that will start flux-broker(1).
[bootstrap]
curve_cert = "${MAMBA_ROOT_PREFIX}/etc/flux/system/curve.cert"

# ubuntu does not have eth0
default_port = 8050
default_bind = "tcp://${linkname}:%p"
default_connect = "tcp://%h{% if subdomain %}.{{ subdomain }}{% endif %}:%p"

# Rank 0 is the TBON parent of all brokers unless explicitly set with
# parent directives.
# The actual ip addresses (for both) need to be added to /etc/hosts
# of each VM for now.
hosts = [
   { host = "${brokers}" },
]
# Speed up detection of crashed network peers (system default is around 20m)
[tbon]
tcp_user_timeout = "2m"
EOF

# Move to conf.d
mv /tmp/broker.toml ${MAMBA_ROOT_PREFIX}/etc/flux/system/conf.d/broker.toml

# If we don't do this, fails on too many open files
# sysctl fs.inotify.max_user_instances=8192
# sysctl fs.inotify.max_user_watches=524288

# Write a small script that makes it easy to connect
cat <<EOF | tee /flux-connect.sh
#!/bin/bash

${MAMBA_ROOT_PREFIX}/bin/flux proxy local:///var/run/flux/local bash
EOF
chmod +x /flux-connect.sh

# Options for the broker. Flux installed from conda does not have
# systemd support.
brokerOptions="-Scron.directory=${MAMBA_ROOT_PREFIX}/etc/flux/system/cron.d \
-Stbon.fanout=256 \
-Srundir=/var/run/flux {% if lead_broker and command != "" %}{% else %}-Sbroker.rc2_none{% endif %} \
-Sstatedir=${MAMBA_ROOT_PREFIX}/etc/flux/system \
-Slocal-uri=local:///var/run/flux/local \
-Slog-stderr-level=6 \
-Slog-stderr-mode=local"

# The lead broker might run a command, otherwise all are interactive.
cfg="${MAMBA_ROOT_PREFIX}/etc/flux/system/conf.d/broker.toml"
{% if lead_broker and command %}
echo "🌀 flux start -o --config ${cfg} ${brokerOptions} flux submit --quiet --watch {{ command }}"
{% else %}
echo "🌀 flux broker --config-path ${cfg} ${brokerOptions}"
{% endif %}

worker_name=$(hostname)
echo "This is ${worker_name}"
cat /etc/hosts

# Retry for failure
while true
do
  {% if lead_broker and command != "" %}
  ${MAMBA_ROOT_PREFIX}/bin/flux start -o --config ${cfg} ${brokerOptions} ${MAMBA_ROOT_PREFIX}/bin/flux submit --quiet --watch {{ command }}
  {% else %}
  ${MAMBA_ROOT_PREFIX}/bin/flux broker --config-path ${cfg} ${brokerOptions}
  {% endif %}
  retval=$?
  echo "Return value for follower worker is $retval"
  if [[ "${retval}" -eq 0 ]]; then
     echo "🤓 Success! Cleaning up"
     exit 0
  fi
  echo "😪 Sleeping 15s to try again..."
  sleep 15
done
