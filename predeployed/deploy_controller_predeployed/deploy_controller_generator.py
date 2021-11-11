#   -*- coding: utf-8 -*-
#
#   This file is part of deploy-controller
#
#   Copyright (C) 2021-Present SKALE Labs
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

from os.path import dirname, join
from typing import Dict

from web3.auto import w3

from predeployed_generator.upgradeable_contract_generator import UpgradeableContractGenerator
from predeployed_generator.openzeppelin.access_control_enumerable_generator \
    import AccessControlEnumerableGenerator


class DeployControllerGenerator(AccessControlEnumerableGenerator):
    '''Generates DeployController
    '''

    pass


class UpgradeableDeployControllerGenerator(UpgradeableContractGenerator):
    '''Generates upgradeable instance of DeployControllerUpgradeable
    '''

    pass
