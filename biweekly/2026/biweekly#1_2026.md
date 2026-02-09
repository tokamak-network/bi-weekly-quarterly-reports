# **From Stabilization to Launch Readiness: Security, Governance, and Infrastructure Progress**
###   
![](https://cdn-images-1.medium.com/max/1600/1*SKnKNJktQeAvt0LZTaBgVA.jpeg)
2026 Tokamak Network Bi-Weekly Report #1 : Jan 16 ~ Jan 31

## Highlight

This bi-weekly period marked major milestones across three core development streams. Tokamak Private App Channels strengthened channel safety with timeout-based recovery flows and critical contract fixes, while stabilizing the transaction/proof workflow for ERC20 transfers including USDT/USDC. Decentralized Staking and Governance advanced TON Staking V3 with extensive test coverage and RAT verification, while refining Whitepaper V2 updates. Tokamak Rollup Hub completed Bug Bounty Phase 1 and progressed toward mainnet readiness by improving the deployment SDK, shutdown/backup tooling, and DRB integration.

## Ecosystem

### 1.1. Staking Update
![](https://miro.medium.com/v2/resize:fit:1400/1*WxXawCC1Kn7LZsQEeQ8zgg.png)
As of January 31st, 2026, the total amount of staked TOKAMAK(TON) has reached 27,541,531.26 TOKAMAK. By staking with Tokamak Network, you contribute to this growing total and enjoy several benefits:

1) Various benefits such as airdrops

2) The rights to participate in Tokamak Network DAO’s operations and decision-making process

### 1.2. Transactions

In the past two weeks, Tokamak Network has recorded 879 TOKAMAK transactions and 532 WTON transactions.

### 1.3. Market Cap

![](https://cdn-images-1.medium.com/max/1600/1*lJyj1KSU58nDZl9rvHdCpQ.png)

Tokamak Network recorded a market capitalization of $39.7M with a total issuance of 100,711,785 TOKAMAK. Over the past two weeks, TOKAMAK token price changed from a high of $0.75 to a low of $0.64, and the total trading volume was $6.37M. For the latest information about total supply and price, please click on [Price Dashboard](https://www.tokamak.network/about/price#/).

Currently, users can supply liquidity and trade TOKAMAK on [Upbit](https://upbit.com/exchange?code=CRIX.UPBIT.KRW-TOKAMAK), [Bithumb](https://www.bithumb.com/react/trade/order/TOKAMAK-KRW), [Coinone](https://coinone.co.kr/exchange/trade/tokamak/krw), [GOPAX](https://www.gopax.co.kr/exchange?market=tokamak-krw), [Biconomy](https://www.biconomy.com/exchange/TOKAMAK_USDT), [DigiFinex](https://www.digifinex.com/en-ww/trade/USDT/TOKAMAK), [WEEX](https://www.weex.com/trade/TOKAMAK-USDT), [Poloniex](https://www.poloniex.com/trade/TOKAMAK_USDT?type=spot), Upbit [Indonesia](https://id.upbit.com/exchange?code=CRIX.UPBIT.IDR-TOKAMAK), [XT.com](https://www.xt.com/en/trade/tokamak_usdt) and [Uniswap](https://app.uniswap.org/explore/tokens/ethereum/0xc4a11aaf6ea915ed7ac194161d2fc9384f15bff2)

## Technology Development

### 2.1. Tech Development

Tokamak Network is an On-demand Layer 2 Platform and strives to provide various Layer 2 protocols to its users.

![](https://cdn-images-1.medium.com/max/1600/1*uC35wrfsrz3ANgYwU312Ow.png)

-   There have been 440 commits in 19 repositories in the Tokamak Network GitHub during the past two weeks. Users can check the category and types of each commit in the following chart. The number of commitments by detailed theme is as follows, and detailed development progress can be found in [Tokamak Network GitHub](https://github.com/tokamak-network).

### 2.2. Zero-Knowledge Proof-Based Private App Channels ([Overview](https://medium.com/tokamak-network/project-tokamak-zk-evm-67483656fd21)).

-   Strengthened core channel contracts with timeout-based withdrawal flow and edge-case handling for improved channel safety ([PR#79](https://github.com/tokamak-network/Tokamak-zk-EVM-contracts/pull/79)).
-   Fixed critical contract issues including tree overflow/isLeader logic and withdraw targetContract validation ([Commit](https://github.com/tokamak-network/Tokamak-zk-EVM-contracts/pull/79/files#diff-8315b915a2fcaee4ed164e4c52a7c795f94506df), [Commit](https://github.com/tokamak-network/Tokamak-zk-EVM-contracts/pull/70/files#diff-c5474925e8c98494d1a9e04967cb5c167be50852)).
-   Refactored channel management to separate whitelisted users from active participants and added O(1) channel-creation tests ([PR#64](https://github.com/tokamak-network/Tokamak-zk-EVM-contracts/pull/64), [PR#69](https://github.com/tokamak-network/Tokamak-zk-EVM-contracts/pull/69)).
-   Implemented new Merkle tree structure (circuits, prover, verifier) in contracts ([PR#77](https://github.com/tokamak-network/Tokamak-zk-EVM-contracts/pull/77)).
-   Rebuilt transaction and proof flow in Synthesizer CLI and channel manager for safer proof generation ([PR#168](https://github.com/tokamak-network/Tokamak-zk-EVM/pull/168), [PR#31](https://github.com/tokamak-network/Tokamak-zkp-channel-manager/pull/31)).
-   Fixed Synthesizer RPC bug and USDT/USDC transfer errors ([PR#171](https://github.com/tokamak-network/Tokamak-zk-EVM/pull/171), [PR#174](https://github.com/tokamak-network/Tokamak-zk-EVM/pull/174)).
-   Implemented automated JSON artifact generation for contract deployments ([PR#68](https://github.com/tokamak-network/Tokamak-zk-EVM-contracts/pull/68)).
-   Built ERC20 config-generation bot for automatic input configuration ([PR#176](https://github.com/tokamak-network/Tokamak-zk-EVM/pull/176)).
-   Published timing report for SNARK proof generation analysis ([Report](https://github.com/tokamak-network/Tokamak-zk-EVM/tree/jake-backend-optimization/packages/backend#timing-report-prove)).
-   Released standalone TokamakL2JS repository for reuse across components ([Repository](https://github.com/tokamak-network/TokamakL2JS)).

### 2.3. Developing Decentralized Staking and Governance ([Overview](https://tokamak.notion.site/49e44e989c514bd683e077c01cc8f143?pvs=25)).

-   Revised and updated the Whitepaper V2, addressing sequencer deposits, slashing mechanisms, and validator minimum collateral calculation ([PR#3](https://github.com/tokamak-network/tokamak-economics-whitepaper-v2/pull/3)).
-   Updated economic layer terminology from “shared verification economics layer” to “systemized verification economics layer” ([Commit](https://github.com/tokamak-network/tokamak-economics-whitepaper-v2/commit/48f72216)).
-   Developed comprehensive slashing mechanism logic with multiple scenarios and bug fixes in V3 SeigManager Contract ([Commit](https://github.com/tokamak-network/ton-staking-v2/commit/ff0628d7)).
-   Implemented RAT verification system for TON Staking V3 using “Adjacent Leaves” proof scheme, passing 16 Solidity unit tests and 8 Go E2E integration tests.
-   Refactored Staking V3 contracts (Layer2Manager, DepositManager, SeigManager) and RAT contract with comprehensive V3 test suite covering 555 tests ([Commit](https://github.com/tokamak-network/ton-staking-v2/commit/b6dd9563)).
-   Developed RAT Dashboard frontend with main overview, live feed, security/economics sections, and L2 detail views ([Commit](https://github.com/tokamak-network/RAT-frontend/commit/fb1c637a)).
-   Completed vTON DAO Governance Model draft (KO/EN) and initiated internal feedback collection.
-   Initialized tokamak-dao-v2 project with Next.js, TypeScript, Tailwind CSS, and Foundry setup ([Commit](https://github.com/tokamak-network/tokamak-dao-v2/commit/f2cf4410)).
-   Prepared and presented seminar on ZK Proving Market with comparison of auction vs. lottery market designs.

### 2.4. Advancing Developer-Centric Appchain Infrastructure ([Overview](https://tokamak.notion.site/1433390669554ae5b09e400f4c9c0fd4?pvs=25)).

-   Completed Bug Bounty Program Phase 1 testing, analyzed results, and announced winners ([Medium](https://medium.com/@georgeWorld/tokamak-rollup-hub-platform-bug-bounty-program-phase-1-900ba5c0894e)).
-   Refactored deployment logic to support dynamic DRB node installation on EKS with regular-node command and multi-chain support ([Commit](https://github.com/tokamak-network/trh-sdk/commit/b131708c2089fb78d92fd3a3c4a17704543f2550), [Commit](https://github.com/tokamak-network/trh-sdk/commit/33afe02e)).
-   Implemented L2 chain shutdown and force withdrawal orchestration command ([PR#182](https://github.com/tokamak-network/trh-sdk/pull/182)).
-   Integrated backup functionality for resume operations in SDK and Backend ([PR#181](https://github.com/tokamak-network/trh-sdk/pull/181), [PR#42](https://github.com/tokamak-network/trh-backend/pull/42)).
-   Added monitoring-thanos-logs plugin for enhanced observability ([PR#174](https://github.com/tokamak-network/trh-sdk/pull/174)).
-   Developed L2 Shutdown helper scripts and documentation with internal seminar demonstration ([PR#383](https://github.com/tokamak-network/tokamak-thanos/pull/383)).
-   Updated DAO Authority Transfer Action Plan v2 for multi-L2 support ([Commit](https://github.com/tokamak-network/tokamak-thanos/commit/f95902db923ab4116b803ab9b8c7d0ee4f5d4f93)).
-   Implemented concurrency testing framework and resilience scenarios for DRB-node ([PR#56](https://github.com/tokamak-network/DRB-node/pull/56)).
-   Added database operation test coverage and Commit-Reveal unit tests with improved Merkle root generation ([PR#59](https://github.com/tokamak-network/DRB-node/pull/59), [PR#62](https://github.com/tokamak-network/DRB-node/pull/62)).
-   Created User Guide for Platform Cross Trade and conducted internal QA testing ([Note](https://www.notion.so/Platform-Cross-Trade-User-Guide-2e5d96a400a3808090cfc7678d2389fb)).

## 3. Community

### 3.1. FAQ

These are some of the FAQs from the community. Please check the section below.

-   **What are the Tokamak Private App Channels?**

So far, the Tokamak Network ZKP team has demonstrated that anyone can easily transform Ethereum transactions into zero-knowledge proofs. Our next step is to go beyond that — to replace Ethereum transactions entirely with ZKPs.

In other words, while keeping the original transactions hidden, the Ethereum state is updated only by verifying the proofs.

Tokamak Private App Channels are a concrete realization of this philosophy. You and your peers can autonomously open a channel, generate transactions and ZKPs within it, roll up the results, and then close the channel. All transactions that took place inside it remain your shared secret.

Zero-knowledge proofs and cryptography ensure that none of your peers can cheat — only the actions that were pre-agreed are faithfully verified and executed.

-   **What is the Tokamak Rollup Hub and why is it important?**

The **Tokamak Rollup Hub** (TRH) is an **on-demand Layer 2 infrastructure platform** designed to enable **seamless deployment** and **end-to-end lifecycle managemen**t of Appchains. It aims to serve as a comprehensive hub that not only showcases our research outputs but also offers **essential tools** for integration and smooth network operations by deployers. TRH supports various **modular rollup technologies** and **developer-friendly SDKs**. In this report, we would like to mention the successful completion of the **second round of testing for SDKv1**, marking significant progress toward a **community-ready release**.

-   **Why do we need a Rollup Hub? Aren’t there already many Layer 2 solutions?**

The Tokamak Rollup Hub is more than just another **Layer 2 solution** — it’s a **flexible platform** that empowers developers to deploy **modular Layer 2 Appchains**, supporting various rollup types like **Optimistic and ZK Rollups**. It enables the integration of components such as bridges, explorers, cross-trade module, random number generator, fraud proofs, and data availability layers based on specific project needs, allowing for **fully customized rollup chains**. Deployed chains can be **self-managed** by deployers on their own AWS infrastructure (with support for more environments planned), removing the dependency on third-party RaaS providers.

Instead of offering a one-size-fits-all rollup, Tokamak Rollup Hub provides the flexibility to **launch and manage your own rollup architecture** tailored to your application’s needs. In that sense, it’s not just a rollup — it’s a **platform for building rollups**.

-   **How to contribute to the Tokamak Network?**

**Grant program**: create your own project and apply for [GranTON](https://www.notion.so/Tokamak-Network-Grant-Program-GranTON-f2384b458ea341a0987c7e73a909aa21?pvs=4)**.**

**Part time**: apply for a part-time position in GranTON projects to expect to receive [TOKAMAK](https://www.coingecko.com/en/coins/tokamak-network) rewards. Please contact the [project leader (owner)](https://www.notion.so/Tokamak-Network-Onboarding-523bc627bd374326b5dfbec3d3b0a8e1?pvs=21) directly and discuss with them.

-   **How can I contact you if I would like to collaborate with the Tokamak Network team?**

Thank you for your interest in collaborating with the Tokamak Network team. We are open to various forms of collaboration that foster Tokamak Network ecosystem growth and value.

To discuss a potential collaboration, please send a brief description of your proposal to hello@tokamak.network, and we will review it and respond as soon as possible.

![](https://cdn-images-1.medium.com/max/1600/1*c_kP_Pw_fOoNmexsJHyOiQ.png)

[Homepage](https://tokamak.network/#/) | [Github](https://github.com/tokamak-network) | [Medium](https://medium.com/tokamak-network) | [X](https://twitter.com/tokamak_network) | [Telegram](https://t.me/tokamak_network) | [Discord](https://discord.gg/6wJ8HAA2nD) | [Linkedin](https://www.linkedin.com/company/tokamaknetwork/) | [Grant](https://www.notion.so/Tokamak-Network-Grant-Program-GranTON-f2384b458ea341a0987c7e73a909aa21?pvs=4) | [Onboarding](https://www.notion.so/Tokamak-Network-Onboarding-523bc627bd374326b5dfbec3d3b0a8e1?pvs=4)

The Tokamak Network team is collecting various opinions through its official channels and will utilize them to improve and develop the Tokamak Network. We ask for active support and participation from the community.

※Note: There are comments and direct messages from impersonators pretending to be members of Tokamak Network. In any case, Tokamak Network NEVER asks for deposits or requests private keys through comments or direct messages.
