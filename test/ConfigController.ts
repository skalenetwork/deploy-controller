import { ethers, upgrades } from "hardhat";
import { ConfigController } from "../typechain-types";
import { loadFixture } from "@nomicfoundation/hardhat-network-helpers"
import { SignerWithAddress } from "@nomiclabs/hardhat-ethers/signers";
import { expect } from "chai";

describe("ConfigController", () => {

    let deployer: SignerWithAddress;
    let team: SignerWithAddress;
    let user1: SignerWithAddress;
    let user1Contract: SignerWithAddress;
    let user2: SignerWithAddress;
    let user2Contract: SignerWithAddress;

    const deployConfigControllerFixture = async () => {
        const factory = await ethers.getContractFactory("ConfigController");
        const configController = await upgrades.deployProxy(factory) as ConfigController;
        await configController.grantRole(await configController.DEPLOYER_ADMIN_ROLE(), deployer.address);
        await configController.grantRole(await configController.DEPLOYER_ADMIN_ROLE(), team.address);
        return configController;
    }

    before(async () => {
        [
            deployer,
            team,
            user1,
            user1Contract,
            user2,
            user2Contract
        ] = await ethers.getSigners();
    })

    describe("deployment permissions", () => {
        it("should allow anyone to deploy on free deployment", async () => {
            const configController = await loadFixture(deployConfigControllerFixture);
            await configController.enableFreeContractDeployment();
            expect(await configController.isDeploymentAllowed(user1.address, user1.address)).to.be.true;
            expect(await configController.isDeploymentAllowed(user1.address, user1.address)).to.be.true;

            await configController.disableFreeContractDeployment();
            expect(await configController.isDeploymentAllowed(user1.address, user1.address)).to.be.false;
            expect(await configController.isDeploymentAllowed(user1.address, user1.address)).to.be.false;
        });

        it("should allow to deploy with DEPLOYER_ROLE", async () => {
            const configController = await loadFixture(deployConfigControllerFixture);
            expect(await configController.isDeploymentAllowed(user1.address, user1.address)).to.be.false;
            await configController.connect(team).addToWhitelist(user1.address);
            expect(await configController.isDeploymentAllowed(user1.address, user1.address)).to.be.true;
            expect(await configController.isDeploymentAllowed(user1.address, user1Contract.address)).to.be.true;
            await configController.connect(team).removeFromWhitelist(user1.address);
            expect(await configController.isDeploymentAllowed(user1.address, user1.address)).to.be.false;
            expect(await configController.isDeploymentAllowed(user1.address, user1Contract.address)).to.be.false;
        });

        it("should allow to deploy via smart contract", async () => {
            const configController = await loadFixture(deployConfigControllerFixture);
            await expect(configController.connect(user1).addAllowedOriginRoleAdmin(user1.address, user1Contract.address))
                .to.be.rejected;
            await configController.connect(team).addAllowedOriginRoleAdmin(user1.address, user1Contract.address);

            expect(await configController.isDeploymentAllowed(user1.address, user1Contract.address)).to.be.false;

            await configController.connect(user1).allowOrigin(user1.address, user1Contract.address);
            await expect(configController.connect(user1).allowOrigin(user1.address, user2Contract.address))
                .to.be.rejected;

            expect(await configController.isDeploymentAllowed(user1.address, user1Contract.address)).to.be.true;
            expect(await configController.isDeploymentAllowed(user1.address, user2Contract.address)).to.be.false;

            await expect(configController.connect(user2).forbidOrigin(user1.address, user1Contract.address))
                .to.be.rejected;
            await configController.connect(user1).forbidOrigin(user1.address, user1Contract.address);

            expect(await configController.isDeploymentAllowed(user1.address, user1Contract.address)).to.be.false;

            await expect(configController.connect(user2).removeAllowedOriginRoleAdmin(user1.address, user1Contract.address))
                .to.be.rejected;
            await configController.connect(team).removeAllowedOriginRoleAdmin(user1.address, user1Contract.address);
            await expect(configController.connect(user1).allowOrigin(user1.address, user1Contract.address))
                .to.be.rejected;
        })
    });
});
