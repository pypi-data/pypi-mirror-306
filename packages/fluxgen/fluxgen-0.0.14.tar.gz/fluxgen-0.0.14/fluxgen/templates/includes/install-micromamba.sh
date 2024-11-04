# Dependencies - specifically let's install micromamba for flux
which micromamba || (
  apt-get update && apt-get install -y bzip2 curl iproute2 || (yum update -y && yum install -y bzip2 curl iproute)

  # Install to root bin
  curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/latest | tar -xvj bin/micromamba
  mv bin/micromamba /bin/micromamba || true
  which micromamba || whereis micromamba
)
