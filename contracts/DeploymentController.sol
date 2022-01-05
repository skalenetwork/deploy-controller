pragma solidity ^0.8.9;
import "@openzeppelin/contracts-upgradeable/utils/AddressUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/access/AccessControlEnumerableUpgradeable.sol";

contract DeploymentController is AccessControlEnumerableUpgradeable {
    bytes32 public constant DEPLOYER_ADMIN_ROLE = keccak256("DEPLOYER_ADMIN_ROLE");
    bytes32 public constant DEPLOYER_ROLE = keccak256("DEPLOYER_ROLE");
    bytes32 public constant MTM_ADMIN_ROLE = keccak256("MTM_ADMIN_ROLE");
    bool public multiTransactionMode = false;

    function enableMTM() external {
        require(hasRole(MTM_ADMIN_ROLE, msg.sender), "Caller is not an admin");
        multiTransactionMode = true;
    }

    function disableMTM() external {
        require(hasRole(MTM_ADMIN_ROLE, msg.sender), "Caller is not an admin");
        multiTransactionMode = false;
    }

    function addToWhitelist(address addr) external {
        grantRole(DEPLOYER_ROLE, addr);
    }

    function removeFromWhitelist(address addr) external {
        revokeRole(DEPLOYER_ROLE, addr);
    }

    function isAddressWhitelisted(address addr) external view returns (bool) {
        return hasRole(DEPLOYER_ROLE, addr) || AddressUpgradeable.isContract(addr);
    }
}