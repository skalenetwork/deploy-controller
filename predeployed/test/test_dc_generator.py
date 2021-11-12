from web3.auto import w3

from deployment_controller_predeployed import DeploymentControllerGenerator, DEPLOYMENT_CONTROLLER_ADDRESS
from .tools.test_solidity_project import TestSolidityProject


class TestEtherbaseGenerator(TestSolidityProject):
    OWNER_ADDRESS = '0xd200000000000000000000000000000000000000'

    def get_dc_abi(self):
        return self.get_abi('DeploymentController')

    def prepare_genesis(self):
        etherbase_generator = DeploymentControllerGenerator()

        return self.generate_genesis(etherbase_generator.generate_allocation(
            DEPLOYMENT_CONTROLLER_ADDRESS,
            schain_owner=self.OWNER_ADDRESS))

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
