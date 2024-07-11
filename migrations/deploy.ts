import { promises as fs } from 'fs';
import { Interface } from "ethers/lib/utils";
import { ethers, upgrades, network } from "hardhat";
import {
    getAbi,
    getVersion,
    verifyProxy,
    getContractFactory,
} from '@skalenetwork/upgrade-tools';


function getContractKeyInAbiFile(contract: string) {
    return contract.replace(/([a-zA-Z])(?=[A-Z])/g, '$1_').toLowerCase();
}

export const contracts = [
    "ConfigController"
]

async function main() {
    const [ owner,] = await ethers.getSigners();

    const version = await getVersion();
    const contractArtifacts: {address: string, interface: Interface, contract: string}[] = [];

    for (const contract of contracts) {
        const contractFactory = await getContractFactory(contract);
        console.log("Deploy", contract);
        const proxy = await upgrades.deployProxy(contractFactory);
        await proxy.deployTransaction.wait();
        contractArtifacts.push({address: proxy.address, interface: proxy.interface, contract});
        await verifyProxy(contract, proxy.address, []);
    }

    console.log("Store ABIs");

    const outputObject: {[k: string]: unknown} = {};
    for (const artifact of contractArtifacts) {
        const contractKey = getContractKeyInAbiFile(artifact.contract);
        outputObject[contractKey + "_address"] = artifact.address;
        outputObject[contractKey + "_abi"] = getAbi(artifact.interface);
    }

    await fs.writeFile(
        `data/config-controller-${version}-${network.name}-abi.json`,
        JSON.stringify(outputObject, null, 4)
    );

    console.log("Done");
}

if (require.main === module) {
    main()
        .then(() => process.exit(0))
        .catch(error => {
            console.error(error);
            process.exit(1);
        });
}
