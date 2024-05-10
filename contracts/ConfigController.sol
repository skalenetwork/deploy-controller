// SPDX-License-Identifier: AGPL-3.0-only

/*
    ConfigController.sol - config-controller
    Copyright (C) 2018-Present SKALE Labs
    @author Artem Payvin

    config-controller is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    config-controller is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with config-controller.  If not, see <https://www.gnu.org/licenses/>.
*/

pragma solidity ^0.8.9;
import "@openzeppelin/contracts-upgradeable/utils/AddressUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/access/AccessControlEnumerableUpgradeable.sol";

contract ConfigController is AccessControlEnumerableUpgradeable {
    bytes32 public constant DEPLOYER_ADMIN_ROLE = keccak256("DEPLOYER_ADMIN_ROLE");
    bytes32 public constant DEPLOYER_ROLE = keccak256("DEPLOYER_ROLE");
    bytes32 public constant MTM_ADMIN_ROLE = keccak256("MTM_ADMIN_ROLE");
    bool multiTransactionMode;
    bool freeContractDeployment;
    string public version;

    function enableMTM() external {
        require(hasRole(MTM_ADMIN_ROLE, msg.sender), "Caller is not an admin");
        require(!multiTransactionMode, "MultiTransactionMode is already enabled");
        multiTransactionMode = true;
    }

    function disableMTM() external {
        require(hasRole(MTM_ADMIN_ROLE, msg.sender), "Caller is not an admin");
        require(multiTransactionMode, "MultiTransactionMode is already disabled");
        multiTransactionMode = false;
    }

    function enableFreeContractDeployment() external {
        require(hasRole(DEPLOYER_ADMIN_ROLE, msg.sender), "Caller is not an admin");
        require(!freeContractDeployment, "Free contract deployment is already enabled");
        freeContractDeployment = true;
    }

    function disableFreeContractDeployment() external {
        require(hasRole(DEPLOYER_ADMIN_ROLE, msg.sender), "Caller is not an admin");
        require(freeContractDeployment, "Free contract deployment is already disabled");
        freeContractDeployment = false;
    }

    function addToWhitelist(address addr) external {
        grantRole(DEPLOYER_ROLE, addr);
    }

    function removeFromWhitelist(address addr) external {
        revokeRole(DEPLOYER_ROLE, addr);
    }

    function setVersion(string memory _version) external {
        require(hasRole(DEFAULT_ADMIN_ROLE, msg.sender), "Caller is not an admin");
        version = _version;
    }

    function allowOrigin(address transactionOrigin, address deployer) external onlyRole(this.allowedOriginRoleAdmin(deployer)) {
        _grantRole(allowedOriginRole(deployer), transactionOrigin);
    }

    function forbidOrigin(address transactionOrigin, address deployer) external onlyRole(this.allowedOriginRoleAdmin(deployer)) {
        _revokeRole(allowedOriginRole(deployer), transactionOrigin);
    }

    function addAllowedOriginRoleAdmin(address admin, address deployer) external onlyRole(this.DEPLOYER_ADMIN_ROLE()) {
        _grantRole(allowedOriginRoleAdmin(deployer), admin);
    }

    function removeAllowedOriginRoleAdmin(address admin, address deployer) external onlyRole(this.DEPLOYER_ADMIN_ROLE()) {
        _revokeRole(allowedOriginRoleAdmin(deployer), admin);
    }

    function isAddressWhitelisted(address addr) external view returns (bool) {
        if (freeContractDeployment) {
            return true;
        }
        return hasRole(DEPLOYER_ROLE, addr) || AddressUpgradeable.isContract(addr);
    }

    function isDeploymentAllowed(address transactionOrigin, address deployer) external view returns (bool) {
        return
            freeContractDeployment ||
            hasRole(DEPLOYER_ROLE, deployer) ||
            hasRole(DEPLOYER_ROLE, transactionOrigin) ||
            hasRole(allowedOriginRole(deployer), transactionOrigin);
    }

    function isMTMEnabled() external view returns (bool) {
        return multiTransactionMode;
    }

    function isFCDEnabled() external view returns (bool) {
        return freeContractDeployment;
    }

    function allowedOriginRole(address deployer) public pure returns (bytes32) {
        return keccak256(abi.encodeWithSelector(this.allowedOriginRole.selector, deployer));
    }

    function allowedOriginRoleAdmin(address deployer) public pure returns (bytes32) {
        return keccak256(abi.encodeWithSelector(this.allowedOriginRoleAdmin.selector, deployer));
    }
}
