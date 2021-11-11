from web3.auto import w3

from deploy_controller_predeployed import DeployControllerGenerator, DEPLOY_CONTROLLER_ADDRESS
from .tools.test_solidity_project import TestSolidityProject


class TestEtherbaseGenerator(TestSolidityProject):
    OWNER_ADDRESS = '0xd200000000000000000000000000000000000000'

    def get_dc_abi(self):
        return self.get_abi('DeployController')

    def prepare_genesis(self):
        etherbase_generator = DeployControllerGenerator()

        return self.generate_genesis(etherbase_generator.generate_allocation(
            DEPLOY_CONTROLLER_ADDRESS,
            schain_owner=self.OWNER_ADDRESS))

    def test_default_admin_role(self, tmpdir):
        genesis = self.prepare_genesis()

        with self.run_geth(tmpdir, genesis):
            assert w3.isConnected()

            etherbase = w3.eth.contract(address=DEPLOY_CONTROLLER_ADDRESS, abi=self.get_dc_abi())
            assert etherbase.functions.getRoleMemberCount(DeployControllerGenerator.DEFAULT_ADMIN_ROLE).call() == 1
            assert etherbase.functions.getRoleMember(DeployControllerGenerator.DEFAULT_ADMIN_ROLE,
                                                     0).call() == self.OWNER_ADDRESS
            assert etherbase.functions.hasRole(DeployControllerGenerator.DEFAULT_ADMIN_ROLE, self.OWNER_ADDRESS).call()

    def test_ether_manager_role(self, tmpdir):
        genesis = self.prepare_genesis()

        with self.run_geth(tmpdir, genesis):
            assert w3.isConnected()

            etherbase = w3.eth.contract(address=DEPLOY_CONTROLLER_ADDRESS, abi=self.get_dc_abi())
            assert etherbase.functions.getRoleMemberCount(DeployControllerGenerator.DEPLOYER_ROLE).call() == 1
            assert etherbase.functions.getRoleMember(DeployControllerGenerator.DEPLOYER_ROLE,
                                                     0).call() == self.OWNER_ADDRESS
            assert etherbase.functions.hasRole(DeployControllerGenerator.DEPLOYER_ROLE, self.OWNER_ADDRESS).call()
