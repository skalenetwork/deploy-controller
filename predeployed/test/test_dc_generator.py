import os

import pytest
import web3.exceptions
from web3.auto import w3

from deployment_controller_predeployed import DeploymentControllerGenerator, DEPLOYMENT_CONTROLLER_ADDRESS
from .tools.test_solidity_project import TestSolidityProject

PRIVATE_KEY = os.environ['ETH_PRIVATE_KEY']


class TestEtherbaseGenerator(TestSolidityProject):
    OWNER_ADDRESS = w3.eth.account.privateKeyToAccount(PRIVATE_KEY).address

    def get_dc_abi(self):
        return self.get_abi('DeploymentController')

    def prepare_genesis(self):
        print(self.OWNER_ADDRESS)
        dc_generator = DeploymentControllerGenerator()

        return self.generate_genesis(
            owner=self.OWNER_ADDRESS,
            allocations=dc_generator.generate_allocation(
                DEPLOYMENT_CONTROLLER_ADDRESS,
                schain_owner=self.OWNER_ADDRESS
            )
        )

    def test_default_admin_role(self, tmpdir):
        genesis = self.prepare_genesis()

        with self.run_geth(tmpdir, genesis):
            assert w3.isConnected()

            dc = w3.eth.contract(address=DEPLOYMENT_CONTROLLER_ADDRESS, abi=self.get_dc_abi())
            assert dc.functions.getRoleMemberCount(DeploymentControllerGenerator.DEFAULT_ADMIN_ROLE).call() == 1
            assert dc.functions.getRoleMember(DeploymentControllerGenerator.DEFAULT_ADMIN_ROLE,
                                              0).call() == self.OWNER_ADDRESS
            assert dc.functions.hasRole(DeploymentControllerGenerator.DEFAULT_ADMIN_ROLE, self.OWNER_ADDRESS).call()

    def test_deployer_role(self, tmpdir):
        genesis = self.prepare_genesis()

        with self.run_geth(tmpdir, genesis):
            assert w3.isConnected()

            dc = w3.eth.contract(address=DEPLOYMENT_CONTROLLER_ADDRESS, abi=self.get_dc_abi())
            assert dc.functions.getRoleMemberCount(DeploymentControllerGenerator.DEPLOYER_ROLE).call() == 1
            assert dc.functions.getRoleAdmin(DeploymentControllerGenerator.DEPLOYER_ROLE).call() == \
                   DeploymentControllerGenerator.DEPLOYER_ADMIN_ROLE
            assert dc.functions.getRoleMember(DeploymentControllerGenerator.DEPLOYER_ROLE,
                                              0).call() == self.OWNER_ADDRESS
            assert dc.functions.hasRole(DeploymentControllerGenerator.DEPLOYER_ROLE, self.OWNER_ADDRESS).call()

    def test_deployer_admin_role(self, tmpdir):
        genesis = self.prepare_genesis()

        with self.run_geth(tmpdir, genesis):
            assert w3.isConnected()

            dc = w3.eth.contract(address=DEPLOYMENT_CONTROLLER_ADDRESS, abi=self.get_dc_abi())
            assert dc.functions.getRoleMemberCount(DeploymentControllerGenerator.DEPLOYER_ADMIN_ROLE).call() == 1
            assert dc.functions.getRoleMember(DeploymentControllerGenerator.DEPLOYER_ADMIN_ROLE,
                                              0).call() == self.OWNER_ADDRESS
            assert dc.functions.hasRole(DeploymentControllerGenerator.DEPLOYER_ADMIN_ROLE, self.OWNER_ADDRESS).call()

    def test_add_whitelist(self, tmpdir):
        genesis = self.prepare_genesis()

        with self.run_geth(tmpdir, genesis):
            assert w3.isConnected()

            dc = w3.eth.contract(address=DEPLOYMENT_CONTROLLER_ADDRESS, abi=self.get_dc_abi())
            print(w3.eth.getBalance(self.OWNER_ADDRESS))
            tx = dc.functions.addToWhitelist('0xD300000000000000000000000000000000000001').buildTransaction({
                'nonce': w3.eth.getTransactionCount(self.OWNER_ADDRESS),
                'from': self.OWNER_ADDRESS
            })
            signed_tx = w3.eth.account.signTransaction(tx, private_key=PRIVATE_KEY)
            tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
            w3.eth.waitForTransactionReceipt(tx_hash)
            assert dc.functions.isAddressWhitelisted('0xD300000000000000000000000000000000000001').call()

    def test_add_whitelist_failed(self, tmpdir):
        genesis = self.prepare_genesis()

        with self.run_geth(tmpdir, genesis):
            assert w3.isConnected()

            dc = w3.eth.contract(address=DEPLOYMENT_CONTROLLER_ADDRESS, abi=self.get_dc_abi())
            with pytest.raises(web3.exceptions.SolidityError):
                dc.functions.addToWhitelist('0xD300000000000000000000000000000000000001').buildTransaction({
                    'from': '0xD300000000000000000000000000000000000001'
                })
