# ECO_January report

[Inputs](https://www.notion.so/Inputs-2f7d96a400a3807bacc6dd32f707e6d7?pvs=21)

# Team Monthly Report - 2026-Jan

## Deliverables

- **Project ECO Research Presentation**: Shared speaker card for upcoming ETHCC presentation on the incentive compatibility of challenge-based protocols ([X](https://x.com/EthCC/status/2013990037806063700)).
- **Project ECO Research Publication**: Published research paper on the incentive compatibility of challenge-based protocols ([arXiv](https://arxiv.org/abs/2512.20864)).

---

## Work

### 💰 Tokamak Economics

### Whitepaper V2 Updates and Feedback Process

- Revised and updated the whitepaper, addressing issues related to sequencer deposits, slashing mechanisms, and validator minimum collateral calculation, unifying requirements and clarifying penalties for loss of seigniorage eligibility ([Slack](https://tokamak-network.slack.com/archives/C07JU6K4KDY/p1704515887265819)).
- Established a comprehensive feedback process for the whitepaper, including a CONTRIBUTING guide and standardized issue templates ([PR](https://github.com/tokamak-network/tokamak-economics-whitepaper-v2/pull/3)).
- Created an internal checklist for publishing and adopting the new whitepaper as a discussion draft, covering positioning, minimum release package, and feedback procedures ([Notion](https://www.notion.so/Internal-Checklist-for-Publishing-Adopting-the-Whitepaper-2dfd96a400a380ce8297ff4fd361a319?pvs=21)).
- Drafted and revised a Medium blog post to introduce the new economic whitepaper, incorporating feedback on multi-tier security layers and validator examples ([Notion](https://www.notion.so/Revised-outline-for-the-new-Whitepaper-Medium-blogpost-2f0d96a400a38045b537c90fd88c8214?pvs=21)).
- Updated the whitepaper's economic layer terminology from "shared verification economics layer" to "systemized verification economics layer" ([Commit](https://github.com/tokamak-network/tokamak-economics-whitepaper-v2/commit/48f72216)).
- Updated TON circulation statistics for December 2025 ([Web](https://docs.google.com/spreadsheets/d/1-4dT3nS4q7RwLgGI6rQ7M1hPx9XHI-Ryw1rkBCvTdcs/edit?gid=681869004#gid=681869004)).

### Staking V3 & RAT System Development

- Developed and tested a comprehensive slashing mechanism logic with multiple scenarios and bug fixes, including re-staking and addressing stack-too-deep errors in the V3 SeigManager Contract ([Commit](https://github.com/tokamak-network/ton-staking-v2/commit/ff0628d7)).
- Implemented RAT verification system for TON Staking V3 using an "Adjacent Leaves" proof scheme, passing 16 Solidity unit tests and 8 Go E2E integration tests, including end-to-end slashing scenarios ([Slack](https://tokamak-network.slack.com/archives/C07JU6K4KDY/p1705030450530499)).
- Designed and analyzed a "Closest Key" challenge-based RAT, optimizing submission overhead and categorizing penalties into liveness and safety slashing ([Commit](https://github.com/tokamak-network/optimism/commit/ff980c3a)).
- Tested OP Succinct's fault dispute game with ZK proofs in both mock and real prover market modes, summarizing results and findings related to bisection game optimization ([Notion](https://www.notion.so/OP-Succinct-Real-ZK-Mode-Fault-Dispute-Game-Test-Report-2eed96a400a3803aba17ce397f2e9aa2?pvs=21)).
- Refactored and updated Staking V3 contracts (Layer2Manager, DepositManager, SeigManager) and the RAT contract for whitepaper finalization, including a comprehensive V3 test suite covering migration, security, integration, and multi-L2 functionalities ([Commit](https://github.com/tokamak-network/ton-staking-v2/commit/b6dd9563)).
- Developed the RAT Dashboard frontend, providing a main overview with metrics, live feed, security/economics sections, L2Table with Bridged TON ranking, and L2 Detail with HealthGauge ([Commit](https://github.com/tokamak-network/RAT-frontend/commit/fb1c637a)).
- Optimized operator loading in the Staking Community Version frontend using two-phase fetch and multicall for improved performance ([Commit](https://github.com/tokamak-network/staking-community-version/commit/423ed773)).
- Drafted a design document for the TON Staking V3 Delegation Platform to sequencer ([Notion](https://www.notion.so/TON-Staking-V3-Delegation-Platform-Design-Document-2ead96a400a380f6ab97c8d9d49a4b01?pvs=21)).

### ⚖️ Tokamak Governance

### DAO V2 Governance Model & Implementation

- Completed the draft for the vTON DAO Governance Model (KO/EN) and initiated an internal feedback collection process ([Notion](https://www.notion.so/vTON-DAO-Governance-Model-EN-2f1d96a400a38084b71ae5f017d963d3?pvs=21)).
- Initialized the `tokamak-dao-v2` project, incorporating Next.js, TypeScript, Tailwind CSS, ESLint, and foundational smart contracts with Foundry setup and web app components ([Commit](https://github.com/tokamak-network/tokamak-dao-v2/commit/f2cf4410)).
- Discussed and recommended a 7-day timelock period for critical DAO agendas, aligning with industry best practices (e.g., Arbitrum, Optimism) ([Slack](https://tokamak-network.slack.com/archives/C07JU6K4KDY/p1706096633276639)).
- Fixed a `currentAgendaStatus` error in `DAOCommittee_V1.sol` by adding voting period verification logic ([Commit](https://github.com/tokamak-network/ton-staking-v2/commit/f871cb77)).
- Integrated real DAO components into V3 test scenarios, including deployment scripts for DAO infrastructure, and removed the deprecated SequencerVault from the test framework ([Commit](https://github.com/tokamak-network/ton-staking-v2/commit/c4fd16c5)).

### 🏗️ Utility of TON

No significant work this month. Efforts focused on Economics and Governance themes.

### 🌀 Other Activities

### ZK Proving Market Research

- Prepared and presented a seminar on the ZK Proving Market, including a Notion summary contrasting auction vs. lottery market designs and categorizing available solutions ([Slide](https://docs.google.com/presentation/d/1EOXKqeunAStk8X3mVcC_9PdIxOWbaN5A/edit?usp=drivesdk&ouid=114240629257411445292&rtpof=true&sd=true), [Notion](https://www.notion.so/Survey-of-ZK-proving-market-WIP-2dad96a400a3807cb1b9e4c6c969f6c0?pvs=21)).

### Website Content Update

- Updated the Tokamak landing page to reflect team changes, including adding a researcher profile and removing other members ([Commit](https://github.com/tokamak-network/tokamak-landing-page/commit/ace0948a)).

---

## Next Month Goals

### 💰 Tokamak Economics

- Complete end-to-end testing for the basic slashing mechanism and prepare for PoC release.
- Initiate development and testing of the advanced slashing mechanism and protocol for Staking V2/V3.
- Finalize whitepaper publication and community communication strategy.

### ⚖️ Tokamak Governance

- Conduct in-depth research and modeling for new DAO governance mechanisms.
- Begin technical design and implementation for the DAO upgrade, focusing on recovering SafeWallet's signer.

### 🏗️ Utility of TON

- Kick-off research and design for the Tokamak Utility Expansion: Contract Audit System.