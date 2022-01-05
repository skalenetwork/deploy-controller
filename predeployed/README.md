# config-controller-predeployed

## Description

A tool for generating predeployed config-controller smart contract

## Installation

```console
pip install config-controller-predeployed
```

## Usage example

```python
from config_controller_predeployed import (UpgradeableConfigControllerGenerator,
                                           CONFIG_CONTROLLER_ADDRESS,
                                           CONFIG_CONTROLLER_IMPLEMENTATION_ADDRESS)

OWNER_ADDRESS = '0xd200000000000000000000000000000000000000'
PROXY_ADMIN_ADDRESS = '0xd200000000000000000000000000000000000001'

config_generator = UpgradeableConfigControllerGenerator()

genesis = {
    # genesis block parameters
    'alloc': {
        **config_generator.generate_allocation(
            contract_address=CONFIG_CONTROLLER_ADDRESS,
            implementation_address=CONFIG_CONTROLLER_IMPLEMENTATION_ADDRESS,
            schain_owner=OWNER_ADDRESS,
            proxy_admin_address=PROXY_ADMIN_ADDRESS
        )
    }
}

```