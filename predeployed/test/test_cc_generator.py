import os

import pytest
import web3.exceptions
from dotenv import load_dotenv
from web3.auto import w3
from web3 import Account
from web3.middleware import geth_poa_middleware

from config_controller_predeployed import ConfigControllerGenerator, CONFIG_CONTROLLER_ADDRESS
from .tools.test_solidity_project import TestSolidityProject

load_dotenv()

PRIVATE_KEY = os.environ['ETH_PRIVATE_KEY']


class TestEtherbaseGenerator(TestSolidityProject):
    OWNER_ADDRESS = Account.from_key(bytes.fromhex(PRIVATE_KEY[2:])).address

    def get_dc_abi(self):
        return self.get_abi('ConfigController')

    def prepare_genesis(self):
        dc_generator = ConfigControllerGenerator()

        return self.generate_genesis(
            owner=self.OWNER_ADDRESS,
            allocations=dc_generator.generate_allocation(
                CONFIG_CONTROLLER_ADDRESS,
                schain_owner=self.OWNER_ADDRESS
            )
        )

    def test_default_admin_role(self, tmpdir):
        self.datadir = tmpdir
        genesis = self.prepare_genesis()
        with self.run_geth(tmpdir, genesis):
            assert w3.is_connected()

            dc = w3.eth.contract(address=CONFIG_CONTROLLER_ADDRESS, abi=self.get_dc_abi())
            assert dc.functions.getRoleMemberCount(ConfigControllerGenerator.DEFAULT_ADMIN_ROLE).call() == 1
            assert dc.functions.getRoleMember(ConfigControllerGenerator.DEFAULT_ADMIN_ROLE,
                                              0).call() == self.OWNER_ADDRESS
            assert dc.functions.hasRole(ConfigControllerGenerator.DEFAULT_ADMIN_ROLE, self.OWNER_ADDRESS).call()
            assert dc.functions.version().call() == '0.0.0'

    def test_deployer_role(self, tmpdir):
        self.datadir = tmpdir
        genesis = self.prepare_genesis()

        with self.run_geth(tmpdir, genesis):
            assert w3.is_connected()

            dc = w3.eth.contract(address=CONFIG_CONTROLLER_ADDRESS, abi=self.get_dc_abi())
            assert dc.functions.getRoleMemberCount(ConfigControllerGenerator.DEPLOYER_ROLE).call() == 1
            assert dc.functions.getRoleAdmin(ConfigControllerGenerator.DEPLOYER_ROLE).call() == \
                   ConfigControllerGenerator.DEPLOYER_ADMIN_ROLE
            assert dc.functions.getRoleMember(ConfigControllerGenerator.DEPLOYER_ROLE,
                                              0).call() == self.OWNER_ADDRESS
            assert dc.functions.hasRole(ConfigControllerGenerator.DEPLOYER_ROLE, self.OWNER_ADDRESS).call()

    def test_deployer_admin_role(self, tmpdir):
        self.datadir = tmpdir
        genesis = self.prepare_genesis()

        with self.run_geth(tmpdir, genesis):
            assert w3.is_connected()

            dc = w3.eth.contract(address=CONFIG_CONTROLLER_ADDRESS, abi=self.get_dc_abi())
            assert dc.functions.getRoleMemberCount(ConfigControllerGenerator.DEPLOYER_ADMIN_ROLE).call() == 1
            assert dc.functions.getRoleMember(ConfigControllerGenerator.DEPLOYER_ADMIN_ROLE,
                                              0).call() == self.OWNER_ADDRESS
            assert dc.functions.hasRole(ConfigControllerGenerator.DEPLOYER_ADMIN_ROLE, self.OWNER_ADDRESS).call()

    def test_mtm_admin_role(self, tmpdir):
        self.datadir = tmpdir
        genesis = self.prepare_genesis()

        with self.run_geth(tmpdir, genesis):
            assert w3.is_connected()

            dc = w3.eth.contract(address=CONFIG_CONTROLLER_ADDRESS, abi=self.get_dc_abi())
            assert dc.functions.getRoleMemberCount(ConfigControllerGenerator.MTM_ADMIN_ROLE).call() == 1
            assert dc.functions.getRoleMember(ConfigControllerGenerator.MTM_ADMIN_ROLE,
                                              0).call() == self.OWNER_ADDRESS
            assert dc.functions.hasRole(ConfigControllerGenerator.MTM_ADMIN_ROLE, self.OWNER_ADDRESS).call()

    def test_add_whitelist(self, tmpdir):
        self.datadir = tmpdir
        genesis = self.prepare_genesis()

        with self.run_geth(tmpdir, genesis):
            assert w3.is_connected()
            if not w3.middleware_onion.get(geth_poa_middleware):
                w3.middleware_onion.inject(geth_poa_middleware, layer=0)

            dc = w3.eth.contract(address=CONFIG_CONTROLLER_ADDRESS, abi=self.get_dc_abi())
            tx = dc.functions.addToWhitelist('0xD300000000000000000000000000000000000001').build_transaction({
                'nonce': w3.eth.get_transaction_count(self.OWNER_ADDRESS),
                'from': self.OWNER_ADDRESS
            })
            signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
            tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            w3.eth.wait_for_transaction_receipt(tx_hash, timeout=15)
            assert dc.functions.isAddressWhitelisted('0xD300000000000000000000000000000000000001').call()

    def test_add_whitelist_failed(self, tmpdir):
        self.datadir = tmpdir
        genesis = self.prepare_genesis()

        with self.run_geth(tmpdir, genesis):
            assert w3.is_connected()
            if not w3.middleware_onion.get(geth_poa_middleware):
                w3.middleware_onion.inject(geth_poa_middleware, layer=0)

            dc = w3.eth.contract(address=CONFIG_CONTROLLER_ADDRESS, abi=self.get_dc_abi())
            with pytest.raises(web3.exceptions.ContractLogicError):
                dc.functions.addToWhitelist('0xD300000000000000000000000000000000000001').build_transaction({
                    'from': '0xD300000000000000000000000000000000000001'
                })

    def test_enable_and_disable_mtm(self, tmpdir):
        self.datadir = tmpdir
        genesis = self.prepare_genesis()

        with self.run_geth(tmpdir, genesis):
            assert w3.is_connected()
            if not w3.middleware_onion.get(geth_poa_middleware):
                w3.middleware_onion.inject(geth_poa_middleware, layer=0)

            dc = w3.eth.contract(address=CONFIG_CONTROLLER_ADDRESS, abi=self.get_dc_abi())
            assert not dc.functions.isMTMEnabled().call()

            tx = dc.functions.enableMTM().build_transaction({
                'nonce': w3.eth.get_transaction_count(self.OWNER_ADDRESS),
                'from': self.OWNER_ADDRESS
            })
            signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
            tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            w3.eth.wait_for_transaction_receipt(tx_hash)
            assert dc.functions.isMTMEnabled().call()

            tx = dc.functions.disableMTM().build_transaction({
                'nonce': w3.eth.get_transaction_count(self.OWNER_ADDRESS),
                'from': self.OWNER_ADDRESS
            })
            signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
            tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            w3.eth.wait_for_transaction_receipt(tx_hash)
            assert not dc.functions.isMTMEnabled().call()

    def test_enable_and_disable_mtm_failed(self, tmpdir):
        self.datadir = tmpdir
        genesis = self.prepare_genesis()

        with self.run_geth(tmpdir, genesis):
            assert w3.is_connected()
            if not w3.middleware_onion.get(geth_poa_middleware):
                w3.middleware_onion.inject(geth_poa_middleware, layer=0)

            dc = w3.eth.contract(address=CONFIG_CONTROLLER_ADDRESS, abi=self.get_dc_abi())

            with pytest.raises(web3.exceptions.ContractLogicError):
                dc.functions.enableMTM().build_transaction({
                    'from': '0xD300000000000000000000000000000000000001'
                })

            with pytest.raises(web3.exceptions.ContractLogicError):
                dc.functions.disableMTM().build_transaction({
                    'from': '0xD300000000000000000000000000000000000001'
                })

    def test_enable_and_disable_fcd(self, tmpdir):
        self.datadir = tmpdir
        genesis = self.prepare_genesis()

        with self.run_geth(tmpdir, genesis):
            assert w3.is_connected()
            if not w3.middleware_onion.get(geth_poa_middleware):
                w3.middleware_onion.inject(geth_poa_middleware, layer=0)

            dc = w3.eth.contract(address=CONFIG_CONTROLLER_ADDRESS, abi=self.get_dc_abi())
            assert not dc.functions.isMTMEnabled().call()

            tx = dc.functions.enableFreeContractDeployment().build_transaction({
                'nonce': w3.eth.get_transaction_count(self.OWNER_ADDRESS),
                'from': self.OWNER_ADDRESS
            })
            signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
            tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            w3.eth.wait_for_transaction_receipt(tx_hash)
            assert dc.functions.isFCDEnabled().call()

            tx = dc.functions.disableFreeContractDeployment().build_transaction({
                'nonce': w3.eth.get_transaction_count(self.OWNER_ADDRESS),
                'from': self.OWNER_ADDRESS
            })
            signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
            tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            w3.eth.wait_for_transaction_receipt(tx_hash)
            assert not dc.functions.isFCDEnabled().call()

    def test_enable_and_disable_fcd_failed(self, tmpdir):
        self.datadir = tmpdir
        genesis = self.prepare_genesis()

        with self.run_geth(tmpdir, genesis):
            assert w3.is_connected()
            if not w3.middleware_onion.get(geth_poa_middleware):
                w3.middleware_onion.inject(geth_poa_middleware, layer=0)

            dc = w3.eth.contract(address=CONFIG_CONTROLLER_ADDRESS, abi=self.get_dc_abi())

            with pytest.raises(web3.exceptions.ContractLogicError):
                dc.functions.enableFreeContractDeployment().build_transaction({
                    'from': '0xD300000000000000000000000000000000000001'
                })

            with pytest.raises(web3.exceptions.ContractLogicError):
                dc.functions.disableFreeContractDeployment().build_transaction({
                    'from': '0xD300000000000000000000000000000000000001'
                })
