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

    function setVersion(string _version) external {
        require(hasRole(DEFAULT_ADMIN_ROLE, msg.sender), "Caller is not an admin");
        version = _version;
    }

    function isAddressWhitelisted(address addr) external view returns (bool) {
        if (freeContractDeployment) {
            return true;
        }
        return hasRole(DEPLOYER_ROLE, addr) || AddressUpgradeable.isContract(addr);
    }

    function isMTMEnabled() external view returns (bool) {
        return multiTransactionMode;
    }

    function isFCDEnabled() external view returns (bool) {
        return freeContractDeployment;
    }
}