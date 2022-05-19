#!/usr/bin/env python
from config_controller_predeployed.config_controller_generator import ConfigControllerGenerator
import json


def main():
    print(json.dumps(ConfigControllerGenerator().get_abi(), sort_keys=True, indent=4))


if __name__ == '__main__':
    main()
