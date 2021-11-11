# deploy-controller-predeployed

## Description

A tool for generating predeployed deploy-controller smart contract

## Installation

```console
pip install deploy-controller-predeployed
```

## Usage example

```python
from deploy_controller_predeployed import  (UpgradeableDeployControllerGenerator, 
                                            DEPLOY_CONTROLLER_ADDRESS, 
                                            DEPLOY_CONTROLLER_IMPLEMENTATION_ADDRESS)

OWNER_ADDRESS = '0xd200000000000000000000000000000000000000'
PROXY_ADMIN_ADDRESS = '0xd200000000000000000000000000000000000001'
ALLOCATED_STORAGE = 1000000

filestorage_generator = UpgradeableDeployControllerGenerator()

genesis = {
    # genesis block parameters
    'alloc': {
        **filestorage_generator.generate_allocation(
            contract_address=DEPLOY_CONTROLLER_ADDRESS,
            implementation_address=DEPLOY_CONTROLLER_IMPLEMENTATION_ADDRESS,
            schain_owner=OWNER_ADDRESS,
            proxy_admin_address=PROXY_ADMIN_ADDRESS
        )
    }
}

```