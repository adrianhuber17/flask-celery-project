#! /bin/bash

# This shell script quickly deploys your project to your
# DigitalOcean Droplet

if [ -z "143.198.49.171" ]
then
    echo "DIGITAL_OCEAN_IP_ADDRESS not defined"
    exit 0
fi

# generate TAR file from git
git archive --format tar --output ./project.tar master

echo 'Uploading project...'
rsync ./project.tar root@143.198.49.171:/tmp/project.tar
echo 'Uploaded complete.'

echo 'Building image...'
ssh -o StrictHostKeyChecking=no root@143.198.49.171 << 'ENDSSH'
    mkdir -p /app
    rm -rf /app/* && tar -xf /tmp/project.tar -C /app
    docker-compose -f /app/docker-compose.prod.yml build
ENDSSH
echo 'Build complete.'