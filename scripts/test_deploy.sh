#!/usr/bin/env bash

set -e

export VERSION=$(yarn run --silent version)
echo $VERSION
yarn exec hardhat run migrations/deploy.ts
