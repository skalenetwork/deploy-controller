#!/usr/bin/env bash

set -e

if [ -z $GITHUB_WORKSPACE ]
then
    GITHUB_WORKSPACE="$(dirname "$(dirname "$(realpath "$0")")")"
fi

if [ -z $GITHUB_REPOSITORY ]
then
    GITHUB_REPOSITORY="skalenetwork/config-controller"
fi

export NVM_DIR=~/.nvm;
source $NVM_DIR/nvm.sh;

DEPLOYED_TAG=$(cat $GITHUB_WORKSPACE/DEPLOYED)
DEPLOYED_VERSION=$(echo $DEPLOYED_TAG | cut -d '-' -f 1)
DEPLOYED_DIR=$GITHUB_WORKSPACE/deployed-config-controller/

DEPLOYED_WITH_NODE_VERSION="lts/fermium"
CURRENT_NODE_VERSION=$(nvm current)

npx hardhat node > /dev/null &

git clone --branch $DEPLOYED_TAG https://github.com/$GITHUB_REPOSITORY.git $DEPLOYED_DIR

# TODO: replace with using previous deploy script
cp $DEPLOYED_DIR/contracts/ConfigController.sol contracts/

# TODO: remove this operation after the next upgrade
cat contracts/ConfigController.sol | sed '$ d' | echo "$(cat -)
    function initialize() external initializer {
        _setupRole(DEFAULT_ADMIN_ROLE, msg.sender);
    }
}" > contracts/ConfigController.sol
rm contracts/test/ConfigControllerTester.sol
VERSION=$DEPLOYED_VERSION npx hardhat run migrations/deploy.ts --network localhost
ABI_FILENAME="config-controller-$DEPLOYED_VERSION-localhost-abi.json"
git checkout -- contracts/ConfigController.sol
git checkout -- contracts/test/ConfigControllerTester.sol

rm -r --interactive=never $DEPLOYED_DIR

export VERSION=$(yarn run --silent version)
ALLOW_NOT_ATOMIC_UPGRADE="OK" ABI="data/$ABI_FILENAME" npx hardhat run migrations/upgrade.ts --network localhost

npx kill-port 8545
