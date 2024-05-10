import chalk from "chalk";
import { contracts } from "./deploy";
import { promises as fs } from "fs";
import { ethers } from "hardhat";
import { Upgrader, AutoSubmitter } from "@skalenetwork/upgrade-tools";
import { SkaleABIFile } from "@skalenetwork/upgrade-tools/dist/src/types/SkaleABIFile";
import { ConfigController } from "../typechain-types";

async function getConfigControllerAbiAndAddresses(): Promise<SkaleABIFile> {
    if (!process.env.ABI) {
        console.log(chalk.red("Set path to file with ABI and addresses to ABI environment variables"));
        process.exit(1);
    }
    const abiFilename = process.env.ABI;
    return JSON.parse(await fs.readFile(abiFilename, "utf-8")) as SkaleABIFile;
}

class ConfigControllerUpgrader extends Upgrader {

    constructor(
        targetVersion: string,
        abi: SkaleABIFile,
        contractNamesToUpgrade: string[],
        submitter = new AutoSubmitter()) {
            super(
                "config-controller",
                targetVersion,
                abi,
                contractNamesToUpgrade,
                submitter);
        }

    async getConfigController() {
        return await ethers.getContractAt("ConfigController", this.abi.config_controller_address as string) as ConfigController;
    }

    getDeployedVersion = async () => {
        const configController = await this.getConfigController();
        try {
            return await configController.version();
        } catch {
            console.log(chalk.red("Can't read deployed version"));
        }
    }

    setVersion = async (newVersion: string) => {
        const skaleManager = await this.getConfigController();
        this.transactions.push({
            to: skaleManager.address,
            data: skaleManager.interface.encodeFunctionData("setVersion", [newVersion])
        });
    }

    // deployNewContracts = () => { };

    // initialize = async () => { };
}

async function main() {
    const upgrader = new ConfigControllerUpgrader(
        "1.9.4",
        await getConfigControllerAbiAndAddresses(),
        contracts,
    );
    await upgrader.upgrade();
}

if (require.main === module) {
    main()
        .then(() => process.exit(0))
        .catch(error => {
            console.error(error);
            process.exit(1);
        });
}
