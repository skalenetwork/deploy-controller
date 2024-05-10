import "@nomiclabs/hardhat-ethers";
import "@openzeppelin/hardhat-upgrades"
import '@typechain/hardhat'
import { HardhatUserConfig } from "hardhat/config";


const config: HardhatUserConfig = {
  solidity: "0.8.9",
  typechain: {
    target: 'ethers-v5'
  }
};

export default config;
