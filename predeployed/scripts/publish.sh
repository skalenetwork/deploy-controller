#!/usr/bin/env bash

set -e

cd "$(dirname "$0")/.."
if [ $TEST = 1 ]; then
python3 -m twine upload --repository testpypi -u __token__ -p "$PYPI_TOKEN" dist/*
else
echo "Uploading to pypi"
python3 -m twine upload -u "$PIP_USERNAME" -p "$PIP_PASSWORD" dist/*
fi

echo "==================================================================="
echo "Uploaded to pypi, check at https://pypi.org/project/config-controller-predeployed/$VERSION/"
