# deploy-controller-predeployed

## Description

A tool for generating predeployed deploy-controller smart contract

## Installation

```console
pip install deploy-controller-predeployed
```

## Usage example

```python
from deployment_controller_predeployed import  (UpgradeableDeploymentControllerGenerator, 
                                                DEPLOYMENT_CONTROLLER_ADDRESS, 
                                                DEPLOYMENT_CONTROLLER_IMPLEMENTATION_ADDRESS)

OWNER_ADDRESS = '0xd200000000000000000000000000000000000000'
PROXY_ADMIN_ADDRESS = '0xd200000000000000000000000000000000000001'

deployment_generator = UpgradeableDeploymentControllerGenerator()

genesis = {
    # genesis block parameters
    'alloc': {
        **deployment_generator.generate_allocation(
            contract_address=DEPLOYMENT_CONTROLLER_ADDRESS,
            implementation_address=DEPLOYMENT_CONTROLLER_IMPLEMENTATION_ADDRESS,
            schain_owner=OWNER_ADDRESS,
            proxy_admin_address=PROXY_ADMIN_ADDRESS
        )
    }
}

```