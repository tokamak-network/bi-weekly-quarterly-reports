

### Highlight

Tokamak Network accelerated across privacy, staking & governance, and rollup infrastructure this period—shipping major zero-knowledge and private voting upgrades, advancing TON staking with faster withdrawal tooling and devnet monitoring, and delivering new AI-assisted operator and automation capabilities. For users and partners, this means smoother private participation with stronger nullifier verification and multi-wallet support, more reliable staking operations with improved visibility and UX, and easier paths for developers to deploy and operate Layer 2 systems with clearer docs, tests, and tooling. Activity highlights: **2161** commits, **12** merged PRs across **67** repositories.

### Development Activity


### SentinAI

SentinAI is an AI-powered security sentinel that helps teams audit smart contracts, detect vulnerabilities, and generate verification reports faster—reducing risk for users and accelerating safer ecosystem growth.

* **Published the First Architecture Blueprint**: Gave builders and reviewers a clear, shared design map so integrations and future features can ship faster with fewer surprises.  
* **Implemented a Hybrid AI Provider Strategy**: Improved audit quality and reliability by selecting the best AI model per task, reducing missed issues and inconsistent results for users.  
* **Delivered End-to-End Verification Automation**: Added a full verification script and test pipeline so teams can validate releases with higher confidence before deploying to production.  
* **Strengthened Testing and Scaling Readiness**: Expanded unit coverage and Kubernetes scaling tests to help ensure SentinAI remains stable and responsive as more projects onboard.  
* **Enhanced the Operator Dashboard Experience**: Simplified the UI and replaced confusing RPC indicators with clearer L2-backed status, making it easier to monitor system health at a glance.


### ton-staking-v2

ton-staking-v2 powers TON token staking so holders can earn rewards while helping secure the network, with a focus this period on faster unstaking, clearer visibility, and safer releases.

* **Integrated the latest V3 staking improvements into Fast Withdrawal work**: Accelerated delivery of quicker unstaking flows so users can access their funds sooner without sacrificing network safety.
* **Launched a web-based devnet monitoring dashboard**: Gave the community and operators clearer, real-time visibility into test-network health, reducing surprises before features reach mainnet.
* **Strengthened end-to-end reliability testing (including challenger scenarios)**: Increased confidence that staking and withdrawal actions behave correctly under stress, lowering the risk of user-impacting failures.
* **Upgraded front-end demos and test coverage**: Improved the staking experience and reduced UI/transaction errors so users see more consistent results when depositing, staking, and withdrawing.
* **Delivered updated, decision-ready documentation and verification checklists**: Made Fast Withdrawal and system behavior easier to understand and validate, helping users and reviewers trust what’s being shipped.


### zk-dex-d1-private-voting

This repository delivers a zero‑knowledge, on‑chain voting system that keeps individual ballots private while still producing verifiable results, enabling more trustworthy governance for users and token holders.

* **Delivered a full D1 private voting flow**: Enabled users to vote privately via a commit‑reveal process while still allowing anyone to verify the final outcome on-chain.  
* **Implemented D2 Quadratic Voting support**: Let communities express preference strength more fairly (reducing whale dominance) while preserving voter privacy.  
* **Strengthened anti‑fraud protections with critical nullifier verification and multi‑wallet support**: Prevented double‑voting and improved reliability for users managing multiple wallets.  
* **Added end‑to‑end ZK proof generation and deployment tooling**: Made it easier and faster to stand up new voting rounds, reducing friction for governance operators and integrators.  
* **Enhanced the voting experience with clearer progress, blocked repeat actions, and improved navigation/translations**: Reduced user confusion and misclicks so voters can complete private ballots with more confidence.


### dust-protocol

dust-protocol enables confidential token transfers with fast, user-friendly withdrawals and social-login onboarding, making privacy accessible without sacrificing speed or usability.

* **Expanded Support for ERC-20 Tokens**: Enabled users to privately send and manage a broader range of tokens beyond a single asset type, making the protocol immediately more practical for everyday use.  
* **Integrated Social Login Onboarding (Google, Discord, Apple, Email, Twitter)**: Let users create and access wallets with familiar sign-in methods, reducing setup friction and helping new users start privately transacting in minutes.  
* **Strengthened Withdrawal Privacy with Railgun Privacy Pool**: Improved “unlinkability” so withdrawals are harder to trace back to deposits, giving users stronger privacy guarantees when moving funds out.  
* **Delivered Gasless/Relayed Transactions via Gelato**: Reduced the need for users to hold gas upfront, making private transfers smoother—especially for first-time users and cross-chain activity.  
* **Enhanced App Reliability and UX End-to-End**: Fixed onboarding loops, naming and theme issues, added a unified multi-address dashboard with balance aggregation, and introduced a Private Wallet interface so users experience fewer blockers and clearer control of their private funds.


### auto-research-press

Autonomous Research Press automatically gathers, reviews, and publishes blockchain ecosystem research so users can access timely, consistent insights without manual report production.

* **Launched Autonomous Research Press v1.1.0 with better navigation**: Made it easier for readers to find and explore ecosystem reports through improved categories and a smoother frontend experience.  
* **Deployed production-ready backend infrastructure and research outputs**: Enabled reliable, end-to-end report generation and publication so stakeholders can depend on consistent availability of new analyses.  
* **Implemented a collaborative, multi-cycle research workflow**: Improved report quality by adding structured research cycles and plan feedback, reducing missed details and increasing clarity for readers.  
* **Enhanced review continuity with historical reviewer context**: Helped reviewers and contributors make faster, better decisions by carrying forward prior feedback, resulting in more coherent final publications.  
* **Strengthened reporting operations with queue time tracking and cleanup**: Reduced delays and clutter by tracking progress, handling rejected sections transparently, and automatically cleaning outdated items so users see fresher, more relevant results.


### Tokamak-zk-EVM

Tokamak-zk-EVM is the core zero-knowledge EVM engine that lets developers run smart contracts with privacy while still proving correctness on Ethereum, enabling secure applications that don’t expose sensitive user data.

* **Streamlined Public Commitment Handling**: Reworked how commitments are generated and verified across the proving workflow, reducing integration friction and helping users experience more consistent proof verification across environments.
* **Expanded ERC20 Example and Multi-Tree State Support**: Updated configs and state handling so builders can simulate and validate more realistic token and state scenarios, accelerating dApp development and reducing setup errors.
* **Optimized Proof Generation Performance**: Improved backend proving paths (including smarter caching and more efficient data handling) to cut proof time, making private transactions feel faster and cheaper to run at scale.
* **Automated End-to-End Synthesizer Testing in CI**: Added and integrated synthesizer test automation so regressions are caught before release, improving reliability for teams building on top of the engine.
* **Upgraded Performance Visibility Tooling**: Enhanced timing instrumentation and the circuit visualizer so developers can quickly pinpoint bottlenecks, leading to faster iteration cycles and steadier performance improvements over time.


### tokamon

Tokamon delivers a mobile-first Web3 product and smart-contract foundation that helps ecosystem partners launch user-friendly experiences with secure on-chain logic and smooth wallet connectivity.

* **Implemented an Upgradeable Smart-Contract Architecture**: Enabled safer, faster feature rollouts so users can benefit from improvements without disruptive migrations or losing access to existing assets.
* **Optimized Contract Performance and Synced App–Contract Interfaces**: Reduced transaction friction and prevented “something went wrong” app errors by keeping the mobile/web apps perfectly aligned with the latest contract behavior.
* **Rebuilt the Mobile App on React Native + Expo**: Improved cross-platform delivery so users get quicker updates and a more consistent experience on both iOS and Android.
* **Added Role-Based In-App Navigation**: Made the product easier to use by showing each user the right flows and screens for their role, reducing confusion and missteps.
* **Integrated WalletConnect and Push-Based Device Claiming**: Expanded onboarding options so users can connect common wallets when they want—or start using key flows through device verification even before setting up a wallet.


### all-thing-eye

all-thing-eye builds automation, analytics, and support tooling that helps Tokamak Network teams run ecosystem operations more efficiently and transparently for faster, more reliable delivery to users and partners.

* **Delivered Secure OAuth Login and Authentication**: Enabled safer, simpler access so contributors and operators can sign in with fewer friction points while keeping internal tools protected.
* **Launched a Ticket-Based Support Bot with High Uptime Design**: Automated support tasks through tickets and improved resilience so requests keep getting handled even when the bot would otherwise “sleep” or disconnect.
* **Implemented AI-Powered Issue Diagnosis and Fix Assistance**: Helped teams identify root causes faster and reduce time-to-resolution, leading to fewer recurring problems that impact users.
* **Introduced Weekly Output Automation and a Tools Management UI**: Made progress reporting and tool administration easier so stakeholders can track delivery and teams can manage workflows without manual overhead.
* **Strengthened Slack Integration Security and Reliability**: Separated sensitive credentials and improved request forwarding so Slack-based workflows are more stable and reduce the risk of token misuse.


### tokamak-dao-v2

Tokamak DAO v2 is a decentralized governance platform where TON holders can propose, delegate, and vote on protocol changes—ensuring upgrades are transparent, community-driven, and safer for everyone using the network.

* **Delivered Automatic Network Switching & Smoother Delegation**: Reduced wallet friction by guiding users to the correct network automatically and making it easier to delegate voting power without confusion or stalled flows.  
* **Enabled DAO-Adjustable Governance Parameters**: Let the community update key governance settings through on-chain decisions, improving responsiveness without relying on centralized operators.  
* **Integrated Proposal Action Building Tools**: Made it simpler to create reliable, well-formed proposals so voters can approve changes with clearer intent and fewer execution surprises.  
* **Launched a vTON Issuance Simulator**: Gave users and delegates a practical way to preview outcomes and understand token issuance dynamics before voting or participating.  
* **Expanded Testing & Demo Infrastructure**: Improved real-world trialability by refreshing the Sepolia deployment and adding demo/sandbox APIs and UI components so community members can validate governance experiences earlier.


### Tokamak-AI-Layer

Tokamak-AI-Layer is building an on-chain foundation for AI-driven agents (trading, yield, and validation) on Tokamak Network so users can access automated strategies with clearer controls, safer execution, and a smoother experience.

- **Launched Core Smart-Contract Infrastructure**: Established the on-chain backbone for AI agents, giving users a more trustworthy and transparent way to run automated strategies.
- **Implemented Staking and Operator Modules**: Improved how operators and staking are managed so users can participate more reliably and experience fewer disruptions when delegating or running services.
- **Delivered Yield Agents and Documentation Updates**: Made yield automation easier to understand and use, helping users set up strategies with less guesswork and fewer setup mistakes.
- **Enhanced Trading Agent Capabilities**: Expanded strategy support (including leverage and short-selling options) so advanced users can pursue more flexible trading approaches within the same framework.
- **Upgraded Front End, SDK, and Validation Workflow**: Streamlined the user interface and developer tooling so users can onboard faster, connect more consistently, and validate actions with fewer failed interactions.


### Other repos

* Other Active Developments: Managed consistent updates across 57 other repositories, focusing on continuous maintenance, documentation, and automated testing to ensure a robust ecosystem.
