

### Highlight

Over the past two weeks, Tokamak Network accelerated delivery across our privacy stack, TON staking & governance, and the rollup-focused developer platform—shipping major ZK voting and zkEVM improvements, expanding staking infrastructure with new monitoring and UX upgrades, and advancing AI-assisted tooling and documentation to support ecosystem growth. For users and businesses, this means smoother private experiences (from onboarding and social login to safer multi-wallet voting), faster and more reliable proving workflows, and more transparent staking operations—while developers get clearer architecture docs, better testing/automation, and increasingly turnkey deployment and integration paths. Development velocity remained high with **2161** commits and **12** merged PRs across **67** repositories.

### Development Activity


### SentinAI

SentinAI is an AI-powered security sentinel that automates smart contract auditing and verification reporting, helping projects ship faster with fewer vulnerabilities and clearer security evidence for users and partners.

- **Published the first end-to-end architecture draft**: Clarified how the system works and scales, making it easier for teams to adopt SentinAI with confidence and predictable results.  
- **Implemented a hybrid AI strategy with module-specific providers**: Improved audit accuracy and consistency by using the best-suited AI models per task, reducing false alarms and missed issues.  
- **Delivered full E2E verification automation with Playwright tooling**: Enabled repeatable, user-like verification runs so teams can trust outputs before release and catch regressions earlier.  
- **Added LLM stress-testing with configurable API server settings**: Increased reliability under heavy usage so audits remain responsive during peak demand and large analysis workloads.  
- **Enhanced operational visibility in the dashboard**: Replaced confusing RPC indicators with clearer L2-to-L1 status reporting and streamlined the UI so users can diagnose availability issues faster.


### ton-staking-v2

ton-staking-v2 powers TON token staking so holders can earn rewards while helping secure the network, with a smoother and safer experience for everyday users and node operators.

- **Integrated Fast Withdrawal foundations**: Advanced the unstaking flow so users can get their funds out faster and with more predictable timing.  
- **Delivered a web-based devnet monitoring dashboard**: Made it easier for operators and contributors to see network and staking health at a glance, reducing downtime and speeding up issue detection.  
- **Enhanced front-end demos and tests**: Improved the staking interface reliability so users face fewer confusing states and failed actions when trying features end-to-end.  
- **Strengthened real-world integration testing**: Increased confidence that critical protections work under realistic conditions, lowering the risk of user-impacting failures in production.  
- **Updated and clarified system documentation**: Replaced outdated guidance with current design docs and verification checklists so integrators can implement correctly and users get fewer surprises.


### zk-dex-d1-private-voting

This zero-knowledge, on-chain voting system lets communities run governance with verifiable results while keeping individual votes private, reducing coercion and increasing participation confidence.

* **Delivered a complete D1 private voting flow**: Enabled end-to-end private, verifiable governance (from committing a vote to revealing results) so users can vote confidently without exposing their choices.
* **Added D2 quadratic voting support**: Introduced fairer preference signaling so communities can better reflect intensity of support, not just simple “yes/no” majorities.
* **Strengthened anti–double-voting protections**: Implemented critical nullifier verification so each eligible voter can vote only once without compromising anonymity.
* **Expanded multi-wallet compatibility**: Improved wallet handling so more users can participate smoothly regardless of which wallet setup they use.
* **Enhanced the voting experience and clarity**: Improved UI blocking after voting, progress indicators, faster proposal navigation, and better translations so users make fewer mistakes and get clearer feedback throughout the process.


### dust-protocol

dust-protocol enables private, confidential token transfers with faster withdrawals and simple social-login onboarding, so users can protect their financial privacy without sacrificing convenience.

- **Expanded Support to Standard ERC‑20 Tokens**: Users can now privately send and manage common tokens (not just a single asset type), making the protocol immediately more useful for everyday transfers.  
- **Integrated a Privacy Pool for Unlinkable Withdrawals**: Withdrawals are harder to trace back to deposits, giving users stronger privacy protections when moving funds back to public wallets.  
- **Added Social Login Onboarding via Privy (Including Twitter)**: New users can start quickly with familiar logins (Google, Apple, Discord, email, Twitter) instead of wrestling with wallet setup from day one.  
- **Delivered a Unified Multi‑Address Dashboard with a Private Wallet UI**: Users can view aggregated balances across addresses and interact through a clearer “private wallet” experience, reducing confusion and improving usability.  
- **Improved Reliability and Release Readiness with UX Fixes and Testing**: Reduced onboarding loops and theme issues, resolved deployment dependency conflicts, and added comprehensive tests so users encounter fewer broken flows and transaction failures.


### auto-research-press

Autonomous Research Press is an automated publication platform that gathers, reviews, and publishes blockchain ecosystem research so teams and community members can access consistent, up-to-date insights without manual reporting overhead.  

- **Released Autonomous Research Press v1.1.0 with Improved Navigation**: Made it easier for readers to find relevant ecosystem reports through secondary categories and a cleaner, less confusing frontend experience.  
- **Strengthened Deployment Readiness with Complete Seed Data**: Enabled faster, more reliable production launches by preloading essential project and results data so the platform works out-of-the-box for new environments.  
- **Implemented a More Transparent Research Queue**: Improved user trust and predictability by tracking time spent and clearly separating rejected items, helping stakeholders understand what’s in progress and what won’t be published.  
- **Delivered Workflow Visualization and Analytics**: Gave users clearer visibility into how research moves from intake to publication, making it easier to monitor throughput, identify bottlenecks, and improve output quality.  
- **Enhanced Collaborative Research Cycles and Agent Quality (v1.2.0)**: Improved the consistency of published reports by adding structured feedback loops, bringing forward reviewer context from prior rounds, and expanding model support for more dependable generation.


### Tokamak-zk-EVM

Tokamak-zk-EVM is Tokamak Network’s zero-knowledge EVM engine that lets developers run smart contracts with privacy and verifiable correctness, enabling users to transact with stronger confidentiality without giving up Ethereum security guarantees.

* **Optimized proof generation performance**: Reduced the time it takes to produce zero-knowledge proofs, helping users get confirmations faster and making private transactions feel more responsive.
* **Strengthened automated test coverage with synthesizer CI**: Added end-to-end test automation to catch breaking changes earlier, improving reliability so users experience fewer failed or inconsistent transactions.
* **Improved developer tooling and circuit visibility**: Updated the circuit visualizer and timing instrumentation so teams can diagnose performance bottlenecks quicker, accelerating delivery of user-facing speed and stability improvements.
* **Simplified and unified commitment handling across the pipeline**: Refactored how public commitments are split across setup/prove/preprocess/verify, reducing edge-case errors and improving consistency of verification for users.
* **Enhanced ERC20 example configuration and multi-tree state handling**: Updated example flows to better reflect real-world state management, making it easier for builders to ship token apps that behave predictably for end users.


### tokamon

Tokamon powers Tokamak Network’s ecosystem development by delivering the smart contracts and user apps needed to onboard users, connect wallets, and manage access in a secure, upgradable way.

- **Implemented Tokamon Smart Contracts**: Delivered the core on-chain functionality so users can rely on transparent, verifiable rules rather than centralized account management.
- **Enabled Upgradeable UUPS Architecture**: Added a safer upgrade path so users benefit from faster feature improvements and security patches without disruptive migrations.
- **Built a Comprehensive Test Suite**: Increased reliability and reduced the chance of user-impacting failures by validating key behaviors before changes ship.
- **Rebuilt the Mobile App on React Native + Expo**: Improved cross-platform delivery so users get a smoother, more consistent experience on both iOS and Android.
- **Integrated WalletConnect and Push-Based Device Claiming**: Made onboarding more flexible by letting users connect with popular wallets and claim devices via push notifications when a wallet isn’t available.


### all-thing-eye

all-thing-eye builds internal automation and dashboards that help the Tokamak ecosystem team respond faster, track work more clearly, and scale community support with less manual effort.  

* **Launched a Ticket-Based Support Bot**: Automated routine support and task requests so community questions and operational needs get handled faster and more consistently.  
* **Implemented Secure Authentication with OAuth**: Enabled safer, simpler sign-in so only authorized contributors can access tools while reducing account-management friction.  
* **Enhanced Bot Reliability with Sleep-Resilient Architecture**: Kept the support bot running more continuously, minimizing downtime and missed requests for users.  
* **Delivered Weekly Output Automation and a Tools Management UI**: Made progress reporting and tool configuration easier, improving transparency and reducing manual overhead for the team.  
* **Added Code Stats and Member Activity Insights**: Provided clearer visibility into contributions and workload distribution so stakeholders can better understand delivery pace and team health.


### tokamak-dao-v2

tokamak-dao-v2 is Tokamak Network’s on-chain governance platform that lets TON holders propose and vote on upgrades, making protocol decisions more transparent, auditable, and community-driven.

- **Implemented Network Auto-Switching**: Reduced failed transactions and confusion by automatically guiding users to the correct network when they connect their wallet.
- **Enhanced Delegation Experience**: Made it easier to delegate voting power with clearer flows, helping more holders participate in governance without needing to vote on every proposal themselves.
- **Delivered a vTON Issuance Simulator**: Gave users and stakeholders a safe way to preview and understand expected outcomes before taking real actions, improving confidence in governance-related decisions.
- **Integrated a Proposal Action Builder**: Simplified how proposals are assembled so governance actions are more consistent and easier for voters to review and trust.
- **Deployed Updated Contracts and a Demo Environment**: Improved reliability for testing and showcasing governance features through refreshed Sepolia deployments and a live demo backend/UI, accelerating feedback and ecosystem adoption.


### Tokamak-AI-Layer

Tokamak-AI-Layer is building the smart contracts, SDK, and user interfaces needed to run AI-powered agents on Tokamak Network, making it easier for users and ecosystem partners to deploy automated strategies with clear validation and staking-backed accountability.

- **Delivered the Initial Smart Contract Infrastructure**: Established the on-chain foundation so users can interact with AI agent services in a more trustworthy, verifiable way rather than relying on purely off-chain promises.  
- **Implemented Staking and Operator Management Modules**: Improved reliability and accountability by ensuring operators can be correctly registered and maintained, reducing the chance of user funds or services being disrupted by misconfiguration.  
- **Integrated a Validation Workflow and Fixed the Validation UI**: Made it easier for users to confirm agent behavior and status through a clearer validation process, improving confidence before they rely on automated actions.  
- **Released an Updated Front End, SDK, and UI Refresh**: Simplified onboarding and day-to-day use so developers can integrate faster and users can navigate agent features with less friction.  
- **Enhanced Trading and Yield Agents (Including Leverage/Short Support)**: Expanded the range of strategies users can run, enabling more flexible market approaches and improved yield automation options.


### Other repos

* Other Active Developments: Managed consistent updates across 57 other repositories, focusing on continuous maintenance, documentation, and automated testing to ensure a robust ecosystem.
