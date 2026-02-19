**Highlight**

Over the past two weeks, Tokamak Network shipped updates across (1) privacy features, (2) TON staking and governance, and (3) developer tools for scaling Ethereum apps (“rollups”). Key releases included improvements to private voting (“ZK voting”), upgrades to our zero-knowledge Ethereum engine (“zkEVM”), stronger staking monitoring and user experience updates, and better AI-assisted tooling and documentation. For users and businesses, this means smoother private experiences (easier sign-up and sign-in), safer voting even across multiple wallets, faster and more reliable proof generation (the step that makes private transactions verifiable), and clearer staking operations—while developers get clearer architecture docs, better automated testing, and simpler “ready-to-use” deployment and integration options. Development velocity remained high with **2161** commits and **12** merged PRs across **67** repositories (engineering activity indicators), alongside user-facing releases like private voting flow completion and improved staking monitoring.

**Development Activity**

Two-week engineering progress across product, infrastructure, and developer tooling (highlights below).

**SentinAI**

SentinAI is an AI-powered security sentinel that automates smart contract auditing and verification reporting, helping projects ship faster with fewer vulnerabilities and clearer security evidence for users and partners.

• **Published the first end-to-end architecture draft**: Clarified how the system works and scales, making it easier for teams to adopt SentinAI with confidence and predictable results.  
• **Implemented a hybrid AI strategy with module-specific providers**: Improved audit accuracy and consistency by using the best-suited AI models per task, reducing false alarms and missed issues.  
• **Delivered full E2E (end-to-end) verification automation with Playwright tooling**: Enabled repeatable, “real user” style verification runs so teams can trust outputs before release and catch issues earlier.  
• **Added AI model (LLM) stress-testing with configurable server settings**: Increased reliability under heavy usage so audit results don’t slow down or time out during peak demand and large analysis workloads.  
• **Enhanced operational visibility in the dashboard**: Replaced confusing network connection indicators with clearer “scaling network → main network” status reporting and streamlined the UI so users can diagnose availability issues faster.  

**ton-staking-v2**

ton-staking-v2 powers TON token staking so holders can earn rewards while helping secure the network, with a smoother and safer experience for everyday users and node operators.

• **Integrated Fast Withdrawal foundations**: Advanced the unstaking flow so users can get their funds out faster and with more predictable timing.  
• **Delivered a web-based devnet (test network) monitoring dashboard**: Made it easier for node operators and contributors to see network and staking health at a glance, reducing downtime and speeding up issue detection.  
• **Enhanced front-end demos and tests**: Improved the staking interface reliability so users face fewer confusing states and failed actions when trying features end-to-end.  
• **Strengthened real-world integration testing**: Increased confidence that critical protections work under realistic conditions, lowering the risk of user-impacting failures in production.  
• **Updated and clarified system documentation**: Replaced outdated guidance with current design docs and verification checklists so integrators can implement correctly and users get fewer surprises.  

**zk-dex-d1-private-voting**

This zero-knowledge, on-chain voting system lets communities run governance with verifiable results while keeping individual votes private, reducing coercion and increasing participation confidence.

• **Delivered a complete D1 private voting flow (core private voting release)**: Enabled end-to-end private, verifiable governance (submit a hidden vote, then reveal verified results) so users can vote confidently without exposing their choices.
• **Added D2 quadratic voting support (a method that lets voters express strength of preference)**: Introduced fairer preference signaling so communities can better reflect intensity of support, not just simple “yes/no” majorities.
• **Strengthened anti–double-voting protections**: Ensured each eligible voter can vote only once while still keeping votes private (using “nullifier” checks under the hood).
• **Expanded multi-wallet compatibility**: Improved wallet handling so more users can participate smoothly regardless of which wallet setup they use.
• **Enhanced the voting experience and clarity**: Improved UI blocking after voting, progress indicators, faster proposal navigation, and better translations so users make fewer mistakes and get clearer feedback throughout the process.

**dust-protocol**

dust-protocol enables private, confidential token transfers with faster withdrawals and simple social-login onboarding, so users can protect their financial privacy without sacrificing convenience.

• **Expanded support to standard ERC‑20 tokens (common Ethereum tokens)**: Users can now privately send and manage common tokens (not just a single asset type), making the protocol immediately more useful for everyday transfers.  
• **Integrated a Privacy Pool for Unlinkable Withdrawals**: Withdrawals are harder to trace back to deposits, giving users stronger privacy protections when moving funds back to public wallets.  
• **Added Social Login Onboarding via Privy (Including Twitter)**: New users can start quickly with familiar logins (Google, Apple, Discord, email, Twitter) instead of wrestling with wallet setup from day one.  
• **Delivered a Unified Multi‑Address Dashboard with a Private Wallet UI**: Users can view aggregated balances across addresses and interact through a clearer “private wallet” experience, reducing confusion and improving usability.  
• **Improved Reliability and Release Readiness with UX Fixes and Testing**: Reduced onboarding loops and theme issues, resolved deployment dependency conflicts, and added comprehensive tests so users encounter fewer broken flows and transaction failures.  

**auto-research-press**

Autonomous Research Press is an automated publication platform that gathers, reviews, and publishes blockchain ecosystem research so teams and community members can access consistent, up-to-date insights without manual reporting overhead.  

• **Released Autonomous Research Press v1.1.0 with Improved Navigation**: Made it easier for readers to find relevant ecosystem reports through secondary categories and a cleaner, less confusing frontend experience.  
• **Strengthened Deployment Readiness with Complete Seed Data**: Enabled faster, more reliable production launches by preloading essential project and results data so the platform works out-of-the-box for new environments.  
• **Implemented a More Transparent Research Queue**: Improved user trust and predictability by tracking time spent and clearly separating rejected items, helping stakeholders understand what’s in progress and what won’t be published.  
• **Delivered Workflow Visualization and Analytics**: Gave users clearer visibility into how research moves from intake to publication, making it easier to monitor throughput, identify bottlenecks, and improve output quality.  
• **Enhanced Collaborative Research Cycles and Agent Quality (v1.2.0)**: Improved the consistency of published reports by adding structured feedback loops, bringing forward reviewer context from prior rounds, and expanding model support for more dependable generation.  

**Tokamak-zk-EVM**

Tokamak-zk-EVM is Tokamak Network’s system for running Ethereum-style apps with added privacy, while still allowing results to be independently verified on Ethereum.

• **Optimized proof generation performance**: Reduced the time it takes to produce zero-knowledge proofs, helping users get confirmations faster and making private transactions feel more responsive.
• **Strengthened automated testing in CI (continuous integration)**: Added end-to-end test automation to catch breaking changes earlier, improving reliability so users experience fewer failed or inconsistent transactions.
• **Improved developer tooling and circuit visibility**: Updated the circuit visualizer and timing instrumentation so teams can diagnose performance bottlenecks quicker, accelerating delivery of user-facing speed and stability improvements.
• **Improved consistency of verification across the system**: Refactored how “commitments” are handled across internal steps (setup/prove/preprocess/verify), reducing edge-case errors and making verification more dependable for users.
• **Enhanced ERC20 example configuration and multi-tree state handling**: Updated example flows to better reflect real-world state management, making it easier for builders to ship token apps that behave predictably for end users.

**tokamon**

Tokamon powers Tokamak Network’s ecosystem development by delivering the smart contracts and user apps needed to onboard users, connect wallets, and manage access in a secure, upgradable way.

• **Implemented Tokamon Smart Contracts**: Delivered the core on-chain functionality so users can rely on transparent, verifiable rules rather than centralized account management.
• **Enabled an upgradeable smart contract design**: Added a safer upgrade path so users benefit from faster feature improvements and security patches without disruptive migrations.
• **Built a Comprehensive Test Suite**: Increased reliability and reduced the chance of user-impacting failures by validating key behaviors before changes ship.
• **Rebuilt the Mobile App on React Native + Expo**: Improved cross-platform delivery so users get a smoother, more consistent experience on both iOS and Android.
• **Integrated WalletConnect (a common wallet connection method) and push-based device linking**: Made onboarding more flexible by letting users connect with popular wallets and link devices via push notifications when a wallet isn’t available.

**all-thing-eye**

all-thing-eye builds internal automation and dashboards that help the Tokamak ecosystem team respond faster, track work more clearly, and scale community support with less manual effort.  

• **Launched a Ticket-Based Support Bot**: Automated routine support and task requests so community questions and operational needs get handled faster and more consistently.  
• **Implemented Secure Authentication with OAuth**: Enabled safer, simpler sign-in so only authorized contributors can access tools while reducing account-management friction.  
• **Enhanced Bot Reliability with Sleep-Resilient Architecture**: Kept the support bot running more continuously, minimizing downtime and missed requests for users.  
• **Delivered Weekly Output Automation and a Tools Management UI**: Made progress reporting and tool configuration easier, improving transparency and reducing manual overhead for the team.  
• **Added Code Stats and Member Activity Insights**: Provided clearer visibility into contributions and workload distribution so stakeholders can better understand delivery pace and team health.  

**tokamak-dao-v2**

tokamak-dao-v2 is Tokamak Network’s on-chain governance platform that lets TON holders propose and vote on upgrades, making protocol decisions more transparent, auditable, and community-driven.

• **Implemented Network Auto-Switching**: Reduced failed transactions and confusion by automatically guiding users to the correct network when they connect their wallet.
• **Enhanced Delegation Experience**: Made it easier to delegate voting power with clearer flows, helping more holders participate in governance without needing to vote on every proposal themselves.
• **Delivered a vTON Issuance Simulator**: Gave users and stakeholders a safe way to preview and understand expected outcomes before taking real actions, improving confidence in governance-related decisions.
• **Integrated a Proposal Action Builder**: Simplified how proposals are assembled so governance actions are more consistent and easier for voters to review and trust.
• **Deployed Updated Contracts and a Demo Environment**: Improved reliability for testing and showcasing governance features through refreshed Sepolia deployments and a live demo backend/UI, accelerating feedback and ecosystem adoption.

**Tokamak-AI-Layer**

Tokamak-AI-Layer is building the on-chain contracts, developer tools (SDK), and user interfaces to run AI-powered “agents” (automated bots/services) on Tokamak Network, with validation and staking-based accountability (operators put funds at risk to encourage correct behavior).

• **Delivered the Initial Smart Contract Infrastructure**: Established the on-chain foundation so users can interact with AI agent services in a more trustworthy, verifiable way rather than relying on purely off-chain promises.  
• **Implemented Staking and Operator Management Modules**: Improved reliability and accountability by ensuring operators can be correctly registered and maintained, reducing the chance of user funds or services being disrupted by misconfiguration.  
• **Integrated a Validation Workflow and Fixed the Validation UI**: Made it easier for users to confirm agent behavior and status through a clearer validation process, improving confidence before they rely on automated actions.  
• **Released an Updated Front End, SDK, and UI Refresh**: Simplified onboarding and day-to-day use so developers can integrate faster and users can navigate agent features with less friction.  
• **Enhanced Trading and Yield Agents (Including Leverage/Short Support)**: Expanded the range of strategies users can run, enabling more flexible market approaches and improved yield automation options.  

**Other repos**

• Other Active Developments: Shipped maintenance updates across 57 other repositories, including documentation refreshes, test improvements, and automation/CI fixes to keep releases stable.