// SPDX-License-Identifier: AGPL-3.0-only

/*
    ConfigControllerTester.sol - config-controller
    Copyright (C) 2024-Present SKALE Labs
    @author Dmytro Stebaiev

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
import "../ConfigController.sol";

contract ConfigControllerTester is ConfigController {
    function initialize() external initializer {
        _setupRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _setRoleAdmin(DEPLOYER_ROLE, DEPLOYER_ADMIN_ROLE);
    }
}
