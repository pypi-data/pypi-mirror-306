# This is just for development - we need a means to generate and distribute this.

if [ ! -f /flux_framework/curve.cert ]; then
cat <<EOF | tee /tmp/curve.cert
#  ZeroMQ CURVE **Secret** Certificate
#  DO NOT DISTRIBUTE

metadata
    name = "flux-service"
    keygen.flux-core-version = "0.64.0"
    keygen.hostname = "flux-service"
    keygen.time = "2024-10-28T13:30:32"
    keygen.userid = "0"
    keygen.zmq-version = "4.3.5"
curve
    public-key = "uMQkII5d)VB?![bXY1.(PBV([Qew1x2l.ar3}5cg"
    secret-key = "ifW737B*JG:U\$s8lvlt6JeMsVfWZ#*eL5JWX2y(b"
EOF

mv /tmp/curve.cert /opt/conda/etc/flux/system/curve.cert
else
cp /flux_framework/curve.cert ${MAMBA_ROOT_PREFIX}/etc/flux/system/curve.cert
fi

chmod o-r ${MAMBA_ROOT_PREFIX}/etc/flux/system/curve.cert
chmod g-r ${MAMBA_ROOT_PREFIX}/etc/flux/system/curve.cert
