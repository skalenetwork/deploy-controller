pragma solidity ^0.8.9;
import "@openzeppelin/contracts-upgradeable/utils/AddressUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/access/AccessControlEnumerableUpgradeable.sol";

contract DeploymentController is AccessControlEnumerableUpgradeable {
    bytes32 public constant DEPLOYER_ROLE = keccak256("DEPLOYER_ROLE");

    function addToWhitelist(address addr) external {
        grantRole(DEPLOYER_ROLE, addr);
    }

    function removeFromWhitelist(address addr) external {
        revokeRole(DEPLOYER_ROLE, addr);
    }

    function isAddressWhitelisted(address addr) external view returns (bool) {
        return hasRole(DEFAULT_ADMIN_ROLE, addr) || hasRole(DEPLOYER_ROLE, addr) || AddressUpgradeable.isContract(addr);
    }
}