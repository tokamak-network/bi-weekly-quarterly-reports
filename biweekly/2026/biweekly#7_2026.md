# Tokamak Network Development Report

**2026-04-16 - 2026-04-30**

Tokamak Network: 5,201,177 Code Changes Across 23 Active Projects (2026-04-16 to 2026-04-30)  
Net codebase growth of +1,818,671 lines driven by +3,509,924 additions against -1,691,253 deletions  
Across the 2026-04-16 to 2026-04-30 reporting period, engineering activity spanned 23 Active Projects and totaled 5,201,177 Code Changes. The codebase expanded by +3,509,924 lines while removing -1,691,253 lines, resulting in a net increase of +1,818,671 lines. The scale of additions and deletions indicates substantial parallel development work alongside refactoring and cleanup efforts. Overall, these numbers represent a high-velocity iteration cycle with significant net growth across the portfolio.

---

# all-thing-eye

**GitHub**: [Link](https://github.com/tokamak-network/all-thing-eye)


## Overview
This repository saw initial build-out work focused on adding a “Tokamak member mapping” scripts toolchain and accompanying project documentation. Based on the recent commits, it appears to support internal or operational workflows that require standardized member mapping, as well as maintaining structured context and notes for contributors. For stakeholders, this type of tooling and documentation work typically underpins more consistent processes and reduces manual effort and ambiguity in future development.

## Statistics
| Metric | Value |
|--------|-------|
| Commits | 2 |
| Contributors | 1 |
| Lines Added | +3,946 |
| Lines Deleted | -0 |
| Net Change | +3,946 |


## Period Goals
During this period, the primary goal was to introduce a dedicated toolchain for “Tokamak member mapping,” likely to formalize or automate how member-related data is organized and handled. A secondary goal was to improve project maintainability by adding documentation files (including CLAUDE.md subagent context files and project notes) to clarify development context and intended workflows.

## Key Accomplishments
* **Implemented a Tokamak member mapping scripts toolchain**: Added a dedicated set of scripts for “Tokamak member mapping” (*feat(scripts): add Tokamak member mapping toolchain*), establishing a concrete technical foundation for mapping-related workflows and enabling more repeatable, tool-driven handling of member data.
* **Expanded repository documentation and contributor context**: Introduced CLAUDE.md subagent context files and project notes (*docs: add CLAUDE.md subagent context files and project notes*), improving knowledge transfer and reducing ramp-up time for future contributors by capturing operational context and repository intent in writing.

## Code Analysis
The net addition of **+3,946 lines** with **0 deletions** indicates this period was dominated by new content rather than refactoring or optimization. The largest portion of growth came from adding the **Tokamak member mapping toolchain** in the scripts area (+3,606 lines), which suggests new executable or automation-oriented functionality was introduced rather than incremental tweaks. The remaining additions (+340 lines) were documentation-focused, specifically **CLAUDE.md subagent context files and project notes**, signaling an emphasis on clarifying how the repository should be used and extended. Overall, the change profile is consistent with an early-stage or expansion phase for this repository’s capabilities, where foundational tooling and its supporting documentation are being established.

## Next Steps
No explicit next steps are stated in the available commit history; subsequent work will likely center on iterating on the newly added member-mapping scripts and keeping the context/documentation in sync as the toolchain evolves.


# bi-weekly-quarterly-reports

**GitHub**: [Link](https://github.com/tokamak-network/bi-weekly-quarterly-reports)


## Overview
This repository serves as a publication and archival location for Tokamak Network’s recurring bi-weekly and quarterly reporting artifacts. Maintaining these reports in version control provides stakeholders with a traceable record of updates over time, supporting governance, accountability, and operational transparency.

## Statistics
| Metric | Value |
|--------|-------|
| Commits | 4 |
| Contributors | 1 |
| Lines Added | +6,525 |
| Lines Deleted | -3 |
| Net Change | +6,522 |


## Period Goals
During this period, the primary objective was to expand the repository’s set of report artifacts by adding new files and ensuring at least one specific bi-weekly report page was accurately updated. The work focuses on keeping the report content current and maintaining a consistent, trackable history of revisions.

## Key Accomplishments
* **Added new report files to the repository**: Included additional reporting artifacts via a bulk upload (“Add files via upload”), increasing the repository’s available documentation for stakeholder review and historical reference.
* **Updated an existing bi-weekly report page**: Made a targeted edit to `biweekly#6_2026.html` (“Update biweekly#6_2026.html”), improving the accuracy or formatting of an already-published report while preserving an auditable change history.

## Code Analysis
The net increase of **+6,522 lines** is primarily attributable to the addition of new repository content, as evidenced by the bulk commit **“Add files via upload” (+3,130 lines)**, which indicates a significant expansion of stored report materials. A smaller maintenance change, **“Update biweekly#6_2026.html” (+1/-3)**, reflects a minor correction or adjustment to an existing HTML report, with minimal deletion consistent with small edits (e.g., removing or replacing a few lines). Overall, the change pattern suggests the repository’s activity this period was centered on adding and curating reporting documents rather than refactoring code, reinforcing its role as a controlled, versioned reporting archive.

## Next Steps
Continue adding newly produced bi-weekly/quarterly report files as they are finalized and apply incremental updates to existing report pages when corrections or formatting adjustments are required.


# enshrined-vrf

**GitHub**: [Link](https://github.com/tokamak-network/enshrined-vrf)


## Overview
This repository centers on “enshrined VRF” work and its associated demonstration and documentation assets, including a Tokamak-branded web arcade and media used to explain and showcase VRF, account abstraction (AA), and session keys. During this period, the project expanded substantially beyond core protocol code into developer-facing references and end-user demo experiences that help stakeholders evaluate practical integration and usability.

## Statistics
| Metric | Value |
|--------|-------|
| Commits | 85 |
| Contributors | 1 |
| Lines Added | +56,829 |
| Lines Deleted | -5,910 |
| Net Change | +50,919 |


## Period Goals
The primary goals this period were to (1) improve the VRF implementation for compatibility with fault-proof environments and (2) build a comprehensive set of supporting materials—documentation, references, demos, and visual presentations—to communicate and validate VRF/AA/session-key concepts through interactive experiences.

## Key Accomplishments
* **Pinned the documentation toolchain for reproducible builds**: Locked the Mintlify version used by the docs site (“docs(site): pin mintlify version for reproducible builds”), reducing variability in documentation builds and improving reliability for publishing and review workflows.
* **Published a presentation deck covering VRF, AA, and session keys**: Added a dedicated slide deck (“docs(demo): add VRF / AA / session-keys presentation deck”), improving stakeholder and partner-facing communication and enabling more structured technical briefings.
* **Generated contract documentation from NatSpec**: Implemented auto-generation of contract references from NatSpec (“docs(site): auto-generate contracts reference from NatSpec”), improving documentation completeness and lowering the cost of keeping references aligned with code.
* **Added fault-proof compatibility to enshrined VRF randomness**: Introduced changes explicitly targeting fault-proof compatibility (“feat(vrf): add fault proof compatibility for enshrined VRF randomness”), addressing requirements relevant to modern rollup dispute/fault-proof contexts and improving the robustness of randomness provisioning.
* **Built a Tokamak-branded arcade demo featuring Jankenman with session keys**: Delivered a branded arcade experience (“feat(tokamak-arcade): Tokamak-branded arcade with Jankenman + session keys”), providing an interactive vehicle to demonstrate session-key flows and related UX concepts.
* **Expanded the arcade information architecture and layout**: Added a pools page, sidebar IA, and a GMX-shaped layout (“feat(tokamak-arcade): pools page + sidebar IA, GMX-shaped layout”), improving navigability and structuring the demo surface for additional modules/features.
* **Created and iterated on a next-generation arcade implementation (SvelteKit/Vite/TS)**: Established a modern frontend scaffold and ports (“feat(tokamak-arcade-next): SvelteKit + Vite + TS scaffold”, “port landing page”, “port games hub”, “port design tokens, mascots, brand”), improving maintainability and development velocity for ongoing demo work.
* **Redesigned and refactored the Jankenman experience and cabinet implementations**: Reworked Jankenman and cabinet designs through multiple iterations (“refactor(tokamak-arcade-next): redesign Jankenman around GMX skeleton”, “rebuild Jankenman cabinet in pure 2D”, “full 3D arcade cabinet for Jankenman”, “redesign Cabinet3D after the Korean 짱깸뽀 cabinet”), demonstrating sustained UI/UX refinement and technical experimentation with 2D/3D rendering approaches.
* **Integrated Three.js elements for interactive cabinet components**: Ported specific cabinet elements to Three.js (“port Jankenman wheel + LED to three.js”), enabling more dynamic visual components within the demo experience.
* **Developed additional demo surfaces, including an on-chain stablecoin game concept**: Added “pongy-bet” described as an on-chain stablecoin 짱깸뽀 arcade (“feat(pongy-bet): on-chain stablecoin 짱깸뽀 arcade”), expanding the repository’s set of interactive examples and potential demo narratives.
* **Produced video compositions for VRF and session accounts**: Added “hyperframes” video compositions (“feat(hyperframes): VRF and session-accounts video compositions”), creating reusable media assets to support explanations, demos, and stakeholder updates.
* **Removed/adjusted routes during IA iteration**: Dropped the `/games` hub route after earlier additions (“feat(tokamak-arcade-next): drop /games hub route” following “port games hub”), reflecting active iteration on navigation and content structure as the demo evolved.

## Code Analysis
The net change of **+50,919 lines** reflects a period dominated by new assets and substantial frontend/demo build-out rather than small incremental maintenance. Large additions are directly attributable to documentation and presentation/media assets (e.g., “docs(site): pin mintlify version…” with **+14,953**, “docs(demo): … presentation deck” with **+9,557**, and “feat(hyperframes): … video compositions” with **+3,493**), indicating a concerted effort to improve explainability and stakeholder-facing clarity alongside code.

On the application side, significant new code was introduced for the demo arcade and its next-generation implementation: a new **SvelteKit + Vite + TypeScript scaffold** (“feat(tokamak-arcade-next): SvelteKit + Vite + TS scaffold” with **+1,856**), multiple content/brand ports (landing page, design tokens/mascots/brand, games hub), and multiple iterations of the Jankenman cabinet across **2D and 3D implementations** (including Three.js components). These additions suggest the repository is being used not only for protocol-related work but also as a comprehensive demonstration environment for user workflows such as session keys.

The **-5,910 lines deleted** primarily correspond to redesign and restructuring work (e.g., “pools page + sidebar IA, GMX-shaped layout” included substantial deletions; “refactor… redesign Jankenman around GMX skeleton” had a net negative; “drop /games hub route” removed **-690**). This pattern indicates active iteration and consolidation—replacing earlier UI structures with updated layouts and refining code organization rather than accumulating unused features.

## Next Steps
Near-term work is likely to continue along the same evidenced tracks: further iteration on the arcade/demo surfaces (Tokamak Arcade and tokamak-arcade-next), continued refinement of documentation and generated references, and additional hardening of VRF behavior in fault-proof-compatible contexts based on the recently introduced compatibility changes.

---


# hr-automation-process

**GitHub**: [Link](https://github.com/tokamak-network/hr-automation-process)


## Overview
This repository supports Tokamak Network’s internal HR automation workflows, including candidate evaluation, reviewer/team matching, developer sourcing, and administrative finance-related functions. The work matters because it standardizes repeatable processes (evaluation, matching, reporting, and tracking) that affect hiring throughput, operational visibility, and administrative control over HR-related data.

## Statistics
| Metric | Value |
|--------|-------|
| Commits | 35 |
| Contributors | 1 |
| Lines Added | +1,635 |
| Lines Deleted | -462 |
| Net Change | +1,173 |


## Period Goals
During this period, development focused on expanding HR operational capabilities by adding administrative tooling for corporate deposit/withdrawal tracking and improving core recruiting workflows (sourcing, matching, evaluation, and reporting). A secondary goal was to improve usability and consistency across the HR UI through layout refinements, clearer button naming, and targeted fixes in key screens.

## Key Accomplishments
* **Implemented an admin-only corporate deposit/withdrawal management tab**: Added a dedicated “corporate inflow/outflow management” tab restricted to administrators, enabling centralized oversight of corporate financial entries relevant to HR operations (commit: “feat: 법인 입출금 관리 탭 (관리자 전용)”).
* **Expanded corporate inflow/outflow classification and tracking signals**: Introduced management by year/month/currency/source and added visibility into recent upload timestamps plus duplicate-exclusion guidance, improving auditability and reducing user error when handling uploads (commits: “feat: 법인 입출금 — 연도/월/통화/소스별 구분 관리”, “feat: 법인 입출금 — 최근 업로드 시점 표시 + 중복 제외 안내”).
* **Improved corporate inflow/outflow table usability and readability**: Refined table layout and font alignment, and added row expansion on click to reveal full content, supporting faster review of detailed entries without navigation overhead (commits: “fix: 법인 입출금 — 테이블 레이아웃/폰트 정렬 개선”, “fix: 법인 입출금 — 행 클릭 시 확장으로 전체 내용 표시”).
* **Added candidate analysis report export in multiple formats**: Enabled downloading candidate analysis reports as Markdown and PDF, providing a portable artifact for internal review processes and recordkeeping (commit: “feat: Candidate 분석 리포트 다운로드 (.md / PDF)”).
* **Enhanced reviewer matching logic with domain-based matching and consolidated recommendation flows**: Added domain-based reviewer matching and integrated “Recommended Reviewers” with “Team Matching,” supporting more consistent assignment workflows (commits: “feat: Reviewer 매칭 — 도메인 기반 매칭 추가”, “feat: Recommended Reviewers + Team Matching 통합”).
* **Improved developer sourcing workflow continuity and scale**: Preserved status/history during re-search, introduced a new vs. existing distinction, and implemented pagination at 100 candidates per page to support larger sourcing datasets while maintaining context (commits: “feat: Developer Sourcing — 재검색 시 상태/이력 보존 + 신규/기존 구분”, “feat: Developer Sourcing — 페이지네이션 (100명/페이지)”).
* **Extended tax simulation input options including payslip KRW support**: Added switching between USDT/KRW input modes and enabled direct KRW input for a payslip flow, increasing flexibility in how compensation/tax scenarios can be entered and reviewed (commits: “feat: 세금 시뮬레이션 — USDT/KRW 입력 모드 전환”, “feat: 세금 시뮬레이션 Payslip — KRW 직접 입력 모드 지원”).
* **Standardized evaluation and candidate detail presentation for clearer review**: Updated evaluation criteria (replacing Innovation/AI Proficiency with Documentation/Deliverable Completeness), refined analysis prompts aligned to Tokamak’s tech stack, and reorganized candidate detail fields into a card-based layout with improved description handling and scrolling (commits: “feat: 평가 항목 교체 — Innovation/AI Proficiency → Documentation/Deliverable Completeness”, “feat: 분석 프롬프트 — Tokamak 기술 스택 기반 평가 기준 구체화”, “fix: Candidate 상세 — 이메일/레포/데모/설명 카드형 레이아웃으로 정리”, “fix: Candidate 상세 — Description 별도 행 분리 + 스크롤 처리”).

## Code Analysis
The net addition of **+1,173 lines** reflects substantial feature expansion across multiple HR modules. Larger additions are tied to new functional areas such as the **admin-only corporate inflow/outflow management tab** and related categorization and UX enhancements (e.g., year/month/currency/source management; upload timestamp and duplicate-handling guidance), as well as **candidate report export** capabilities supporting **.md and PDF** outputs. Additional new logic and UI work is evidenced in **reviewer matching enhancements** (domain-based matching; integrating recommended reviewers with team matching) and **developer sourcing improvements** (state/history preservation across re-search; pagination; new vs. existing distinction).

The **-462 lines deleted** indicate iterative refinement rather than purely additive development. Several commits explicitly focus on UI clarity and consistency—such as button naming standardization, moving expense settlement controls to match established patterns, and table layout/font alignment fixes—suggesting the codebase is being actively adjusted to reduce confusion and improve day-to-day operability (e.g., “버튼명 혼동 해소…”, “전체 HR 탭 버튼명/배열 통일”, “테이블 레이아웃/폰트 정렬 개선”). Overall, the mix of new features and cleanups is consistent with a tool moving from initial capability build-out toward more stable, consistent operational use.

## Next Steps
Continue iterating on the newly added corporate inflow/outflow management and tax simulation flows, with further UX consistency fixes where needed. Extend reporting/export and workflow integrations across sourcing, candidate evaluation, and reviewer/team matching based on operational feedback from ongoing use.


# llm-api-gateway

**GitHub**: [Link](https://github.com/tokamak-network/llm-api-gateway)


## Overview
`llm-api-gateway` is a gateway and supporting web/dashboard tooling for managing access to LLM providers with usage controls, billing/credits flows, and operational visibility. Within the Tokamak ecosystem, it provides the connective layer between user authentication, API key issuance, request proxying, and metering—capabilities that are required to safely expose LLM access to end users and partners. For stakeholders, the work in this period indicates an initial end-to-end product surface (landing + dashboard + proxy + billing primitives) and a documented architecture baseline.

## Statistics
| Metric | Value |
|--------|-------|
| Commits | 27 |
| Contributors | 1 |
| Lines Added | +169,837 |
| Lines Deleted | -1,194 |
| Net Change | +168,643 |


## Period Goals
The work this period focused on establishing an initial architecture and then productizing a functional MVP that includes a landing experience, a dashboard for authentication and key management, and a proxy layer with metering, rate limiting, and observability. In parallel, the team added operational documentation and testing so the system can be run and validated more reliably.

## Key Accomplishments
* **Established an initial architectural baseline**: Added the first architectural draft, providing a concrete code foundation to build the gateway, dashboard, and operational components on top of (“Launched the first architectural draft”).
* **Implemented a credits-based billing flow geared toward deployment**: Added a “pre-deposit credit mode” and executed a “productization sprint,” indicating movement from prototype mechanics toward a more operationally usable credits model (“feat: pre-deposit credit mode + productization sprint”).
* **Delivered a SIWE-enabled dashboard for account and key operations**: Implemented a web UI for Sign-In With Ethereum (SIWE) that supports credits management, top-ups, and API key minting, enabling a self-serve workflow for end users (“feat(dashboard): SIWE web UI for credits, top-up, and API key minting”).
* **Expanded proxy capabilities for provider passthrough and auditing**: Added native Anthropic passthrough support, introduced long-lived API keys, and implemented a SQLite-backed usage audit mechanism to record usage locally (“feat(proxy): native Anthropic passthrough, long-lived API keys, and SQLite usage audit”).
* **Added traffic controls and browser compatibility for the gateway**: Implemented a token-bucket rate limiter for `/v1/messages` and enabled CORS so browser-based clients can call the gateway, improving safety and enabling web integrations (“feat(proxy): add token-bucket rate limiter for /v1/messages”; “fix(proxy): enable CORS so browsers can call the gateway”).
* **Introduced operational observability via Prometheus**: Exposed Prometheus metrics at `/metrics`, enabling standard monitoring integrations for uptime, traffic, and performance tracking (“feat(proxy): expose Prometheus metrics at /metrics”).
* **Built and refined the MVP landing experience with security and runtime configuration**: Added an MVP intro page served via `mprocs`, then productized it with runtime config, security headers, SEO/Open Graph metadata, and tests—supporting a public-facing entry point and better baseline hardening (“feat(landing): add MVP intro page served via mprocs”; “feat(landing): productize MVP page with runtime config, security headers, SEO/OG, and tests”).
* **Improved financial correctness and developer/test readiness**: Updated billing calculations to compute margin in atto-PTON to avoid “sub-micro-USD ceiling” issues, added pricing/model updates (GPT-5.4 family and Gemini 2.5), and introduced unit tests so `npm test` executes real checks rather than being “phantom” (“feat(billing): compute margin in atto-PTON…”; “feat(pricing): add GPT-5.4 family and Gemini 2.5 models”; “test(proxy): add pricing unit tests…”).

## Code Analysis
The very large net increase (+168,643 LOC) is primarily attributable to the introduction of an initial codebase and architecture (“Launched the first architectural draft” +153,138/-0), followed by substantial feature implementation across product surfaces. Added code also reflects the build-out of: (1) a dashboard with SIWE login and flows for credits, top-ups, and API key minting; (2) a proxy layer with provider passthrough (Anthropic), long-lived keys, SQLite-based usage auditing, rate limiting for `/v1/messages`, Prometheus metrics exposure, and CORS enablement; and (3) a landing page that evolved from an MVP intro into a productized page with runtime configuration, security headers, SEO/OG metadata, and tests.

The relatively small deletions (-1,194) are consistent with iterative refinement rather than a large-scale rewrite: refactoring test helpers (“extract shared SIWE login helper”), tightening weak assertions, and adjustments within productization work (e.g., credit mode sprint changes and landing page tests). Overall, the change profile suggests the repository moved quickly from an initial architectural drop toward a more operable MVP by adding monitoring, traffic controls, documentation (“add architecture, contracts, proxy, and operations references”; README rewrite), and basic test coverage.

## Next Steps
Based on the current implementation focus, the next logical steps are continued hardening of operations (monitoring/metrics usage and runbooks), and incremental expansion of the billing/credits and proxy feature set alongside additional tests to improve confidence in production usage.


# oracle-battle

**GitHub**: [Link](https://github.com/tokamak-network/oracle-battle)


## Overview
oracle-battle contains server-side code for a Tokamak Network component that exposes operational endpoints (including health checks) and integrates with an indexer. Recent changes indicate it is run in a security-sensitive environment, with configuration considerations for TEE deployments and network-request hardening. For users and investors, this work matters because it targets service reliability, deployability, and security controls—foundational requirements for production infrastructure.

## Statistics
| Metric | Value |
|--------|-------|
| Commits | 3 |
| Contributors | 1 |
| Lines Added | +653 |
| Lines Deleted | -420 |
| Net Change | +233 |


## Period Goals
During this period, the primary goal was to restructure the server codebase to improve maintainability while strengthening security posture for production deployments (including TEE-related configuration). A secondary goal was to improve operational visibility by enhancing the `/health` endpoint to report indexer staleness, alongside general cleanup to remove dead code and simplify complex logic.

## Key Accomplishments
* **Refactored the server into clearer service boundaries**: Extracted services and reworked server structure to make the codebase easier to maintain and extend over time, reducing operational risk from tightly coupled logic (*refactor(server): extract services...*).
* **Added protections against SSRF-style request abuse**: Implemented an SSRF guard, reducing exposure to a common class of server-side vulnerabilities that can impact internal network resources and hosted infrastructure (*refactor(server): ...add SSRF guard...*).
* **Hardened configuration for TEE deployments**: Strengthened configuration handling with TEE in mind, improving deployment safety and reducing the chance of misconfiguration in sensitive runtime environments (*refactor(server): ...harden config for TEE*).
* **Improved operational health reporting with indexer staleness**: Updated the `/health` endpoint to return indexer staleness, enabling better monitoring, faster incident triage, and clearer signals when upstream indexing lags (*fix(health): return indexer staleness in /health endpoint*).

## Code Analysis
The net change of **+233 lines** (from **+653 / -420**) is consistent with a significant internal restructuring rather than purely incremental feature work. The largest commit combined **service extraction**, an **SSRF guard**, and **TEE-focused configuration hardening**, which typically introduces new modules/wrappers and configuration validation code while simultaneously removing or consolidating prior implementation paths (*refactor(server): extract services, add SSRF guard, harden config for TEE*).  

The **420 lines deleted** aligns with deliberate cleanup activities: removing dead code, flattening nested ternaries, and fixing a missing import, all of which reduce complexity and make behavior easier to reason about during audits and production debugging (*refactor: simplify code — remove dead code, flatten nested ternaries, fix missing import*). The targeted `/health` change adds operational capability without large surface-area growth, suggesting attention to runtime observability as the system matures (*fix(health): return indexer staleness in /health endpoint*). Overall, the mix of refactoring, security hardening, and monitoring improvements indicates a focus on production readiness and maintainability.

## Next Steps
No PR roadmap details were available for this period. Following the refactor and security hardening work, the next practical steps would be to continue tightening configuration/validation around the TEE runtime and expand operational checks/monitoring based on the new indexer staleness signal.


# oracle-exchange

**GitHub**: [Link](https://github.com/tokamak-network/oracle-exchange)


## Overview
oracle-exchange appears to be an application layer repository focused on oracle-driven exchange/market workflows, including market fee logic, oracle status handling, and user-facing visibility into oracle agent execution. Within the Tokamak ecosystem, it matters because it shapes how users understand prices and oracle activity (e.g., KRW pricing alignment) and how reliably the app can read contracts and operate during oracle failures.

## Statistics
| Metric | Value |
|--------|-------|
| Commits | 6 |
| Contributors | 1 |
| Lines Added | +742 |
| Lines Deleted | -183 |
| Net Change | +559 |


## Period Goals
This period focused on expanding market/oracle functionality (launch fee logic, forced oracle failure handling, and keeper backfill) while improving operational resilience and transparency. The work also targeted correctness and consistency in price presentation (BTC display aligned to KRW via Upbit) and strengthened configuration safety by loading contract configuration from a backend with mismatch warnings.

## Key Accomplishments
* **Implemented market/oracle operational controls**: Added a 10-TOK launch fee, introduced an oracle `forceFail` capability, and implemented keeper backfill logic, expanding the system’s ability to manage launch economics and handle operational edge cases more explicitly (commit: “feat(market): add 10-TOK launch fee, oracle forceFail, and keeper backfill”).
* **Corrected BTC pricing representation for KRW users**: Aligned BTC price display and target calculations to KRW using Upbit as the reference, reducing the risk of user confusion or incorrect decision-making caused by inconsistent denomination (commit: “fix(oracle): align BTC price display and targets to KRW via Upbit”).
* **Improved application resilience for on-chain reads**: Added an error boundary and a retry policy around contract reads, aiming to reduce user-facing failures and increase robustness when contract calls intermittently fail (commit: “fix(resilience): add error boundary and retry policy for contract reads”).
* **Increased transparency of oracle agent activity and safer config handling**: Added real-time display of oracle agent execution progress, integrated backend `/suggestions` to preview oracle prompt content, and began loading contract config from a backend while warning on address mismatches—improving both user observability and configuration correctness (commits: “feat(reveal): show real-time oracle agent execution progress”, “feat(create): integrate backend /suggestions for oracle prompt preview”, “fix(config): load contract config from backend and warn on address mismatch”).

## Code Analysis
The net change of **+559 lines** (from **+742 added** and **-183 deleted**) indicates a period dominated by feature expansion with targeted corrections and cleanup. New capability additions are reflected in commits that introduced market-level logic (the **10-TOK launch fee**, **oracle forceFail**, and **keeper backfill**) and user-facing features (real-time **oracle agent execution progress** and backend **/suggestions** integration for oracle prompt preview). The deletions and adjustments are consistent with corrective work—particularly the **BTC price display/target alignment to KRW via Upbit** and the configuration changes that **load contract config from a backend** while adding **address mismatch warnings**, both of which suggest refinement of existing behavior rather than purely additive development. The explicit addition of an **error boundary and retry policy for contract reads** signals an increasing emphasis on operational stability and failure handling, which is typically associated with maturing application behavior under real-world conditions.

## Next Steps
Near-term work should center on validating and iterating on the newly added operational controls (launch fee handling, oracle forceFail, keeper backfill) and continuing to harden reliability measures introduced for contract reads (error boundary and retry policy). Additional follow-through is also implied for the backend-driven configuration path (address mismatch warnings) and the oracle execution progress UI to ensure consistent behavior across environments.


# scatter-dex

**GitHub**: [Link](https://github.com/tokamak-network/scatter-dex)


## Overview
scatter-dex is a codebase supporting zkScatterDEX-related applications and tooling, including a mobile client, user-facing web apps, SDK references, and operator/relayer components. It matters to Tokamak Network stakeholders because the work in this period focused on integrating zero-knowledge proving (Groth16) into end-user authorization flows, expanding product surfaces (Pay/Pro/Stealth), and improving documentation and developer usability—all of which affect adoption readiness and operational reliability.

## Statistics
| Metric | Value |
|--------|-------|
| Commits | 531 |
| Contributors | 1 |
| Lines Added | +197,519 |
| Lines Deleted | -42,465 |
| Net Change | +155,054 |


## Period Goals
During this period, the repository work centered on shipping a zkScatterDEX mobile experience using a hybrid Expo/React Native + WebView approach, and wiring native Groth16 proving into authorization paths to make private/zk flows practical on mobile. In parallel, the team expanded product applications (Pay, Pro, Stealth), introduced operator tooling and relayer workflow improvements, and invested heavily in documentation infrastructure and API/SDK references to support developer and user onboarding.

## Key Accomplishments
* **Integrated a native Groth16 prover into mobile authorization**: Wired a native Groth16 prover into the `OrderService` authorize path and completed the native proving pipeline (including a reported “60ms authorize proof”), improving feasibility of client-side authorization proofs in mobile trading flows (commits: “wire native Groth16 prover into OrderService authorize path”, “finish native Groth16 prover — 60ms authorize proof”).
* **Delivered a zkScatterDEX mobile app scaffold and hybrid architecture**: Added an Expo/React Native + WebView “ZK hybrid” mobile application scaffold, establishing the baseline for shipping mobile user experiences alongside web-based interfaces (commit: “zkScatterDEX mobile app — Expo/RN + WebView ZK hybrid (#350)”).
* **Implemented private-trade mobile scatter flow with client-side proofs**: Added a “private-trade scatter flow,” client-side authorize proof generation, expanded History views, and applied Tokamak branding, advancing end-to-end mobile usage for privacy-oriented trade interactions (commit: “private-trade scatter flow, client-side authorize proof, History expand, Tokamak branding (#385)”).
* **Built operator console scaffolding for relayer operations**: Introduced an initial `apps/operators` v1 scaffold described as a “relayer operator console,” laying groundwork for operational management interfaces needed to run relayer services (commit: “apps/operators v1 scaffold — relayer operator console”).
* **Improved relayer settlement behavior with async worker and protocol changes**: Implemented an async settlement worker and a “202 accept-then-settle protocol,” which can improve responsiveness and reliability of settlement workflows by decoupling acceptance from execution (commit: “async settlement worker + 202 accept-then-settle protocol (#391)”).
* **Expanded SDK/zk proving components for commitments and deposits**: Added zk-related SDK functionality including “commitment + deposit prover + worker runtime,” extending the toolkit available for building deposit/proving flows and offloading work to a runtime/worker model (commit: “commitment + deposit prover + worker runtime (Phase 2b-i)”).
* **Added Pay application capabilities for deposits and payout workflows**: Implemented live deposit wiring (including “native ETH wrap”), atomic batch deposits, mid-flow abort behavior, and multiple UX improvements such as dashboard sorting and “run notes” tracking (commits/PRs: “wire live deposit (Phase B v1 + native ETH wrap)”, PR#595, PR#590, PR#597).
* **Introduced Stealth wallet and inbox routing plus navigation integration**: Added `/stealth/wallet` and `/stealth/inbox` routes and a Stealth navigation element, and expanded the Pay address book with MetaAddress and Stealth-related sections to support stealth-style addressing workflows (PR#596, PR#598).
* **Hardened client storage and contract integration points**: Added a folder-storage MetaAddress provider and migrated apps (notably Pro) off `localStorage`, and migrated EIP-5792 handling to `@zkscatter/sdk/contracts`, improving portability and consistency across app surfaces (PR#594, PR#599).
* **Strengthened documentation and reference generation for developers**: Shipped a self-hosted Nextra documentation site with auto-generated SDK/REST API references, expanded coverage of the `@zkscatter/sdk` surface, added a Mintlify docs setup, and included a whitepaper iteration aligned with protocol references (commits: “self-hosted Nextra site + auto-generated SDK / REST API refs”, “expand site to cover full @zkscatter/sdk surface”, “scaffold zkScatter brand home + Mintlify docs setup”, “whitepaper v0.1 + … protocol-ref alignment”).
* **Cleaned up build/release workflows for generated references**: Adjusted CI to avoid committing generated TypeDoc SDK references and instead regenerate at build time, reducing repository noise and keeping generated artifacts consistent with the build pipeline (commit: “un-commit TypeDoc SDK reference; regenerate at build time”).
* **Expanded product surfaces with new frontends and Pro trader workflow work**: Scaffolded ScatterPay/ScatterDrop frontends and related product documentation, and iterated on Pro trading UX including trade form v1 (pair selector, advanced settings, OTC-focused copy) and “UX essentials” for production workflow (commits: “scaffold ScatterPay/ScatterDrop frontends + product docs”, “trade form v1…”, “UX essentials for production trader workflow”).

## Code Analysis
The +197,519 lines added largely reflect substantial new application scaffolding and feature implementation across multiple surfaces: the Expo/RN + WebView mobile app base (“zkScatterDEX mobile app — Expo/RN + WebView ZK hybrid”), operator console scaffolding (“apps/operators v1 scaffold”), Pay/Pro frontend expansions (“scaffold ScatterPay/ScatterDrop frontends”, “trade form v1”), and major documentation infrastructure investments (“self-hosted Nextra site + auto-generated SDK / REST API refs”, Mintlify setup, expanded SDK surface docs). A meaningful portion of additions also came from integrating and finalizing native Groth16 proving on mobile—both initial scaffolding (“scaffold native Groth16 prover via mopro”) and deep wiring into authorization paths (“wire native Groth16 prover into OrderService authorize path”), plus SDK/zk runtime work for commitments and deposits.

The -42,465 lines deleted indicate active refactoring and cleanup rather than only net-new expansion. Examples include removing the HiddenWebView component (“drop HiddenWebView”), revising generated documentation handling in CI (“un-commit TypeDoc SDK reference”), and restructuring Pay modules (“split payouts/new wizard into route-private modules”). This combination of rapid feature buildout with targeted deletions suggests the project is moving from early scaffolding into iterative hardening: features are being added quickly, then consolidated through refactors, build hygiene, and UX cleanup PRs (e.g., PR#593) to reduce maintenance burden.

## Next Steps
Near-term work is likely to continue deepening mobile zk flows and operational tooling, building on the completed native Groth16 authorize integration and the operator/relayer scaffolds (commits referencing native prover wiring and operator console; relayer async settlement worker). Additional iterations are also implied for Pay/Stealth experiences and documentation maintenance, given ongoing PRs focused on deposit batching, address book/MetaAddress handling, and expanding SDK references.


# skills

**GitHub**: [Link](https://github.com/tokamak-network/skills)


## Overview
This repository packages a set of reusable “skills” as a Claude Code plugin, focusing on structured development and maintenance workflows (for example, code review and cleanup tasks). In the Tokamak ecosystem, it serves as developer tooling that standardizes repeatable assistant-driven procedures, helping teams run consistent reviews and operational cleanups with documented outputs. For stakeholders, this matters because it reduces variability in routine engineering tasks and improves traceability through saved review artifacts.

## Statistics
| Metric | Value |
|--------|-------|
| Commits | 6 |
| Contributors | 1 |
| Lines Added | +717 |
| Lines Deleted | -76 |
| Net Change | +641 |


## Period Goals
During this period, the work centered on formalizing the repository as a Claude Code plugin and adding/organizing several skills that support code review and maintenance workflows. A secondary goal was to improve how review outputs are stored and safeguarded, alongside establishing baseline project documentation and configuration files.

## Key Accomplishments
* **Restructured the project into a Claude Code plugin**: Implemented the plugin scaffold (including `.claude-plugin/plugin.json` and a dedicated `skills/` directory), making the skills consumable in a standardized plugin format and easier to integrate into developer workflows (*feat: restructure as Claude Code plugin (.claude-plugin/plugin.json + skills/ dir)*).
* **Added new skill definitions for review and cleanup workflows**: Introduced “codex-review” and “cleanup-claude-agents” skills, expanding the set of available automation procedures teams can run consistently (*feat: add codex-review and cleanup-claude-agents skills*).
* **Improved review artifact handling and organization**: Updated the `codex-review` workflow to persist outputs under `docs/codex-review/<topic>/`, improving auditability and making review results easier to find and share (*feat(codex-review): save artifacts to docs/codex-review/<topic>/ per review*).
* **Strengthened guardrails and added operational maintenance tooling**: Restored “IMPORTANT” prompt guards across multiple codex execution calls to reduce misuse or unintended behavior, and added a dedicated docker cleanup skill definition to support routine environment maintenance (*fix(codex-review): restore IMPORTANT prompt guards…*; *feat(docker-cleanup): add docker cleanup skill definition*).

## Code Analysis
The net +641 lines largely reflect new functionality and packaging work rather than minor tweaks. A substantial portion of the +717 additions came from introducing new skill definitions (notably “codex-review,” “cleanup-claude-agents,” and “docker-cleanup”) and from reorganizing the repository into a formal Claude Code plugin structure (*feat: add codex-review and cleanup-claude-agents skills*; *feat(docker-cleanup)*; *feat: restructure as Claude Code plugin*). The addition of baseline project files—README, `package.json`, and `.gitignore`—indicates an effort to make the repository easier to understand, install, and maintain as a distributable unit (*docs: add README, package.json, .gitignore*).

The -76 deletions are explained by changes within the `codex-review` workflow when introducing a more explicit artifact storage layout under `docs/codex-review/<topic>/`. This kind of deletion is consistent with refactoring and reformatting to enforce a clearer output structure rather than removing product capability (*feat(codex-review): save artifacts…*). The presence of a follow-up fix restoring “IMPORTANT” prompt guards suggests attention to operational safety and consistency in automated review execution flows (*fix(codex-review): restore IMPORTANT prompt guards…*), which is typically associated with early-stage maturation of internal automation tooling.

## Next Steps
Continue iterating on the skill set and the plugin structure by refining artifact organization and maintaining/expanding prompt guardrails as additional skills are introduced. Further documentation updates are a logical follow-on to support consistent adoption of the plugin-based workflow.


# Tokamak-AI-Layer

**GitHub**: [Link](https://github.com/tokamak-network/Tokamak-AI-Layer)


## Overview
Tokamak-AI-Layer consolidates Tokamak Network’s work around an agent operating system fork (TokagentOS) and related tooling, templates, plugins, and on-chain vault integrations. During this period, the repository was re-based on an upstream ElizaOS release, then pruned and renamed to support Tokamak-specific packaging and product direction. This matters to users and stakeholders because it defines the maintainable codebase, developer scaffolding, and contract/plugin integration surface area for deploying and extending Tokamak-aligned agent applications.

## Statistics
| Metric | Value |
|--------|-------|
| Commits | 197 |
| Contributors | 1 |
| Lines Added | +2,447,980 |
| Lines Deleted | -1,310,987 |
| Net Change | +1,136,993 |


## Period Goals
The primary goal for the period was to import an upstream ElizaOS v2.0.0-alpha codebase, apply a Tokamak-specific fork/rename strategy (TokagentOS), and remove legacy or out-of-scope components to reduce maintenance burden. In parallel, the team focused on shipping Tokagent-related templates, plugin wiring, and vault/strategy functionality, including ABI updates and deployment-related changes reflected in the merged PRs.

## Key Accomplishments
* **Imported the upstream ElizaOS codebase as a baseline**: Brought in the upstream `elizaOS v2.0.0-alpha.223` tree as the starting point for the repository, establishing a known upstream reference for subsequent Tokamak-specific changes (`import upstream elizaOS v2.0.0-alpha.223 tree (pre-rename)`).
* **Removed large sets of unused packages and legacy integrations to narrow scope**: Eliminated 11 unused packages and 16 legacy app integrations (including categories like benchmarks, examples, scenario, bindings, prompts, interop, docs, skills, hiveexchange, and various app integrations), materially reducing surface area and future upkeep (`remove 11 unused packages`, `remove 16 legacy app integrations`; PRs `Cleanup/remove eliza legacy`, `Merge ... cleanup/remove-eliza-legacy`).
* **Applied a mechanical rename to align the fork with TokagentOS branding and packaging**: Performed broad mechanical renaming from `elizaOS` to `tokagentOS`, enabling Tokamak-aligned distribution and code ownership boundaries (`apply mechanical rename (elizaOS -> tokagentOS)`; PR `Feat/tokagentos fork`).
* **Adjusted package scopes and scaffold installability behavior**: Addressed scaffold installability and package scope behavior, including scope renames and plugin path handling, to improve reliability of generated projects (`fix(tokagentos): scaffold installability — scope rename, comment parse, plugin paths`; `revert @tokagentos/plugin-* -> @elizaos/plugin-* scope`).
* **Shifted the target environment toward web-only by removing native dependencies**: Removed Capacitor native-plugins and other native-oriented components, simplifying builds and reducing platform-specific maintenance (`remove Capacitor native-plugins (web-only target)`).
* **Eliminated external cloud references from scaffolded UI**: Stripped “Eliza Cloud” references from scaffolded UI outputs, aligning generated artifacts with the fork’s intended ecosystem and reducing dependency on upstream cloud assumptions (`strip all Eliza Cloud references from scaffolded UI`).
* **Pruned plugin surface area by removing tooling/media submodules**: Removed plugin submodules related to media/tooling (e.g., calendly, music-* and other tooling), tightening the supported plugin set and lowering ongoing integration cost (`remove media/tooling plugin submodules (calendly, music-*, github, computeruse)`).
* **Delivered iterative TokagentOS alpha releases and product polish**: Landed changes labeled as `v2.0.0-alpha.242` and `v2.0.0-alpha.252`, including a “Tokagent palette,” product polish, “eliza chat verbatim,” and a “tokagent plugin layer,” indicating active iteration on user-facing behavior and plugin architecture (`v2.0.0-alpha.242 — Tokagent palette + product polish`; `v2.0.0-alpha.252 — eliza chat verbatim + tokagent plugin layer`).
* **Synchronized CLI-bundled templates and shipped plugin sources inside templates**: Updated CLI-bundled templates to match source and shipped tokagent plugin sources in the `fullstack-app` template, improving developer onboarding and reducing drift between template outputs and current code (`sync CLI-bundled templates with source`; `ship tokagent plugin sources inside fullstack-app template`).
* **Integrated a Tokagent strategy plugin into templates and CLI, with tests**: Wired `plugin-tokagent-strategy` into templates and CLI, and added targeted test coverage for building/strategy behavior, supporting a repeatable strategy development workflow (`wire plugin-tokagent-strategy into template + CLI`; `kind + build-strategy test coverage`; PR `feat(plugin-tokagent-strategy): backtesting harness`).
* **Advanced vault and perps action support and generated TypeScript definitions**: Added CoreWriter encoding and explicit `OPEN/CLOSE_PERP_POSITION` actions and generated `.d.ts` artifacts, improving typed integration for consumers and clarifying supported action semantics (`CoreWriter encoding + OPEN/CLOSE_PERP_POSITION actions + build .d.ts`).
* **Updated contract ABIs and documented a vault implementation plan**: Regenerated `VaultFactory` ABI and added `TokagentVault` ABI for contract integration work, and captured a `TokagentVault implementation plan` document for structured execution (`regenerate VaultFactory ABI + add TokagentVault ABI`; `PR 0 TokagentVault implementation plan`; PR `feat(tokagent): non-zkp vault product — contract + plugins + strategy engine`; PR `deploy(tokagent): mainnet factory upgrade + helper wiring`).

## Code Analysis
The extremely large addition volume is primarily explained by the one-time import of the upstream ElizaOS `v2.0.0-alpha.223` tree (+2,312,516 lines) followed by subsequent fork-alignment changes (rename and restructuring). The large deletion volume is dominated by deliberate scope reduction: removing 11 unused packages (-966,978 lines) and 16 legacy app integrations (-237,448 lines), along with removal of Capacitor native-plugins (-36,508) and plugin submodules (-12,784). Beyond structural and pruning work, net-new functional additions are evidenced in template synchronization and shipping plugin sources (`sync CLI-bundled templates`, `ship tokagent plugin sources inside fullstack-app template`), strategy plugin wiring and tests, and vault/perps-related updates including ABIs and action definitions (`OPEN/CLOSE_PERP_POSITION`, ABI regeneration). Overall, the pattern indicates a repository moving from upstream intake to consolidation: importing a baseline, removing non-essential components, then building a maintainable Tokamak-specific developer and integration surface.

## Next Steps
Near-term work is likely to focus on executing the documented TokagentVault implementation plan and continuing deployment/ABI alignment (as indicated by the vault plan, ABI regeneration, and mainnet factory upgrade PR). Continued iterations on TokagentOS alpha releases, templates/CLI parity, and strategy/backtesting workflows are also implied by the recent release and template/strategy commits.


# tokamak-design

**GitHub**: [Link](https://github.com/tokamak-network/tokamak-design)


## Overview
tokamak-design is an application repository establishing an initial “Tokamak Design” app and its supporting infrastructure. The work in this period focused on standing up the first functional draft and then improving input handling, capture/loading behavior, performance, and deployment/build reliability. This matters to users and stakeholders because it creates a concrete foundation for iterating on a design-oriented product while reducing latency and operational friction in early deployment.

## Statistics
| Metric | Value |
|--------|-------|
| Commits | 11 |
| Contributors | 2 |
| Lines Added | +9,022 |
| Lines Deleted | -121 |
| Net Change | +8,901 |


## Period Goals
During this reporting period, the team aimed to launch an initial version of the Tokamak Design app and publish an early architectural draft to establish direction. Alongside initial delivery, the focus was on improving capture speed and feedback during loading, hardening input behavior, and stabilizing build/deployment configuration.

## Key Accomplishments
* **Delivered the initial Tokamak Design application baseline**: Implemented the first version of the Tokamak Design app (“feat: initial Tokamak Design app”), providing a concrete codebase to iterate on and enabling early internal/external evaluation of functionality.
* **Published an initial architectural draft**: Recorded and launched a first architectural draft (“Launched the first architectural draft”), establishing a documented starting point for future implementation and stakeholder alignment.
* **Improved capture-time user feedback during loading**: Added loading enhancements to show sub-steps and elapsed seconds during capture (“feat(loading): show substep + elapsed seconds during capture”), helping users understand progress and reducing uncertainty during longer operations.
* **Reduced capture time through targeted browser performance optimizations**: Implemented “three free optimizations to cut capture time” and adjusted page readiness strategy to use `domcontentloaded` instead of `load` (“perf(browser): …”, “perf(browser): use domcontentloaded instead of load”), improving responsiveness and throughput for capture-related workflows.
* **Hardened input handling for URL convenience**: Added support for URLs without a scheme (e.g., `base.org`, `www.base.org`) and refined input UI hints (“feat(input): accept URLs without scheme…”, “ui(input): use vercel.com as placeholder hint”), reducing user friction and improving usability at the point of entry.
* **Stabilized containerized build behavior**: Updated Docker build stages to install `devDependencies` where required (“fix(docker): install devDependencies for build stage”), decreasing build failures and improving reliability for CI/CD and deployment pipelines.
* **Adjusted Fly.io runtime resources and configuration**: Performed iterative infrastructure tuning on Fly.io VM sizing (bumping to performance resources and reverting back) (“infra(fly): bump VM…”, “infra(fly): revert VM…”), reflecting active calibration of cost/performance tradeoffs for the deployed service.
* **Streamlined developer-facing documentation**: Reduced the README to essentials (“docs: trim README to essentials”), improving signal-to-noise for onboarding and ongoing maintenance.

## Code Analysis
The net increase of **+8,901 lines** is primarily attributable to the introduction of the initial application codebase (“feat: initial Tokamak Design app” at +8,831/-1), indicating this period was foundational and focused on establishing the first working implementation. Subsequent additions and small deletions reflect iterative refinement rather than large-scale rewrites: loading-state instrumentation and UI improvements (“feat(loading)…”, “ui(input)…”), input parsing enhancements for scheme-less URLs (“feat(input)…”), and multiple performance-focused browser changes intended to reduce capture time (“perf(browser): …”, “perf(browser): use domcontentloaded…”).

The **-121 lines deleted** are concentrated in documentation trimming (“docs: trim README to essentials” at +12/-61) and small adjustments across performance and UI commits, suggesting early cleanup and tightening rather than deprecating major functionality. Overall, the commit set indicates an early-stage project moving from initial delivery toward operational maturity by addressing usability, performance, build correctness, and deployment configuration in quick iterations.

## Next Steps
Continue iterating on capture performance and loading clarity based on the recently introduced progress indicators and browser optimizations. Further stabilize deployment and build processes as the application evolves beyond the initial architectural draft and baseline implementation.


# tokamak-landing-page

**GitHub**: [Link](https://github.com/tokamak-network/tokamak-landing-page)


## Overview
This repository contains the main Tokamak Network public website, which serves as the primary entry point for users, partners, and stakeholders. It is a key channel for publishing ecosystem updates and documentation-oriented content that supports transparency and ongoing communication with the community and investors.

## Statistics
| Metric | Value |
|--------|-------|
| Commits | 2 |
| Contributors | 1 |
| Lines Added | +6,620 |
| Lines Deleted | -0 |
| Net Change | +6,620 |


## Period Goals
During this period, the work focused on updating the website’s published content, specifically by adding new biweekly reporting materials. This supports ongoing stakeholder communication by making recent progress updates accessible through the main Tokamak Network site.

## Key Accomplishments
* **Published Biweekly Reports #5 and #6 (Mar 16–31 / Apr 01–15, 2026)**: Added new report content to the site (“feat: add Biweekly Reports #5 and #6”), improving the availability of structured, time-bounded progress updates for stakeholders who rely on the website as the canonical public source.

## Code Analysis
The net change of **+6,620 lines** with **0 deletions** indicates a period dominated by content expansion rather than refactoring or cleanup. The commit message provided explicitly accounts for **+3,310 lines** tied to adding Biweekly Reports #5 and #6, consistent with introducing substantial new written or structured report material to the landing site. The remaining added lines are attributable to the second commit in the period, but details of that change are not available from the provided commit list; as a result, no further characterization of the additional additions is made here. Overall, the change profile suggests the repository is being actively used as a publishing vehicle for ongoing reporting content.

## Next Steps
Continue publishing subsequent biweekly reports and maintaining the website’s reporting sections to keep stakeholder-facing updates current. As content grows, consider periodic review to ensure navigation and organization remain clear and scalable for new report entries.


# tokamak-thanos

**GitHub**: [Link](https://github.com/tokamak-network/tokamak-thanos)


## Overview
tokamak-thanos is Tokamak Network’s optimistic rollup stack repository, focused on components needed to deploy and operate rollup-related infrastructure for Ethereum scaling. Work in this period concentrated on improving the reliability and operability of the deployment tooling, which is important for teams that need predictable L1 contract deployment and repeatable release processes.

## Statistics
| Metric | Value |
|--------|-------|
| Commits | 9 |
| Contributors | 1 |
| Lines Added | +185 |
| Lines Deleted | -9 |
| Net Change | +176 |


## Period Goals
During this reporting period, the primary goal was to introduce and operationalize a tokamak-deployer CLI binary for L1 contract deployment, with an emphasis on diagnosing and reducing deployment failures or hangs. A secondary goal was to harden the CI/release workflow for this deployer by correcting pnpm setup and cache behavior and expanding build target coverage.

## Key Accomplishments
* **Introduced a tokamak-deployer CLI binary for L1 contract deployment**: Added the deployer command-line binary to support L1 contract deployment as a discrete, packageable tool (PR#393), improving the ability to standardize deployment procedures across environments.
* **Implemented comprehensive deployment logging to diagnose deployment hangs**: Added detailed deployment logging specifically aimed at debugging cases where contract deployments hang (commit: “feat(tokamak-deployer): add comprehensive deployment logging for debugging contract deployment hangs”), increasing observability and reducing time-to-resolution when deployment issues occur.
* **Stabilized CI for release/deployer workflows with correct pnpm configuration and caching**: Updated CI to set up pnpm properly, corrected pnpm cache dependency paths, and adjusted install behavior by removing `--frozen-lockfile` to allow checksum regeneration in CI (commits: “fix(ci): add pnpm setup…”, “fix(ci): correct pnpm cache dependency path…”, “fix(ci): remove --frozen-lockfile…”), decreasing the likelihood of pipeline failures unrelated to code changes.
* **Expanded release build coverage and rebuilt deployer binaries with the new logging**: Added linux-arm64 build coverage to the release-deployer workflow and rebuilt binaries after adding comprehensive logging (commits: “fix(ci): add pnpm setup… include linux-arm64 build”, “build(tokamak-deployer): rebuild binaries with comprehensive logging”), improving compatibility for teams building/deploying from ARM-based environments and ensuring distributed binaries reflect the latest diagnostics.

## Code Analysis
The net +176 lines primarily reflect functional additions to the tokamak-deployer toolchain and supporting release infrastructure. The largest increase is attributable to “add comprehensive deployment logging for debugging contract deployment hangs” (+85/-1), indicating a material expansion in runtime diagnostics and traceability during deployment execution. Additional changes focused on CI reliability—introducing pnpm setup, correcting pnpm cache paths, and modifying lockfile strictness to accommodate CI checksum regeneration—suggesting the team prioritized reducing workflow friction and making releases more reproducible. The relatively small deletion count (-9) implies limited cleanup in this period, with work centered on capability and operational robustness rather than refactoring.

## Next Steps
Next work is likely to build on the newly introduced deployer CLI and logging by iterating on deployment reliability and maintaining CI stability as release targets and environments evolve. Continued refinement of the release-deployer workflow to minimize environment-specific build issues would be a logical follow-on to the pnpm and linux-arm64 adjustments made this period.


# Tokamak-zk-EVM

**GitHub**: [Link](https://github.com/tokamak-network/Tokamak-zk-EVM)


## Overview
Tokamak-zk-EVM is the core engine and associated tooling for executing smart contracts with zero-knowledge proof workflows, supporting private execution use cases on Ethereum. During this period, work concentrated on packaging and distribution of developer-facing components (CLI, web, containerized flows) alongside performance instrumentation and GPU/memory optimizations for polynomial/R1CS operations. This matters to users and stakeholders because it improves how the ZK-EVM can be installed, run, and measured in real environments, while tightening resource usage and proof-generation performance characteristics.

## Statistics
| Metric | Value |
|--------|-------|
| Commits | 272 |
| Contributors | 1 |
| Lines Added | +211,214 |
| Lines Deleted | -123,228 |
| Net Change | +87,986 |


## Period Goals
The primary goals for this reporting period were to reorganize and harden the project’s packaging and release workflow—especially around the synthesizer, CLI distribution, and npm publishing—so the system can be installed and operated more consistently. In parallel, the team focused on profiling and optimizing polynomial and R1CS-related computation (including GPU resource bounds), improving performance visibility and controlling runtime memory behavior.

## Key Accomplishments
* **Restructured the synthesizer into clearer deployment units**: Split the synthesizer into container, node, and web packages and created a synthesizer workspace root with debug entrypoints, improving maintainability and enabling more targeted deployment and debugging workflows (“Restructure synthesizer into container, node, and web packages”; “Create synthesizer workspace root and debug entrypoints”).
* **Strengthened and standardized npm release processes**: Adopted trusted publishing for npm releases and synchronized release version management, reducing operational risk and improving repeatability of published artifacts (“Use trusted publishing for npm releases”; “chore: synchronize release version management”).
* **Expanded CLI distribution and installation support**: Added an npm-distributed CLI package with release support and introduced Docker-backed CLI installation flows, improving accessibility for developers and operators across environments (“Add npm-distributed CLI package and release support”; PR#193 “Add Docker-backed CLI install…”; PR#189 “internalize tokamak-cli install/runtime flows”).
* **Adjusted QAP compiler packaging strategy for distribution**: Published the qap-compiler from a generated dist package, shifting distribution toward compiled artifacts for more consistent downstream consumption (“Publish qap-compiler from generated dist package”).
* **Validated and corrected CLI runtime packaging for the QAP library**: Implemented and then reverted a change related to packaging the qap library for CLI runtime, indicating active stabilization and verification of runtime packaging behavior (“fix: package qap library for cli runtime”; “Revert ‘fix: package qap library for cli runtime’”).
* **Added fine-grained performance instrumentation for polynomial arithmetic**: Introduced polynomial arithmetic line timing, broke down polynomial combination timing, and tightened prove timing boundaries to improve diagnosability of proof-generation performance (“Add polynomial arithmetic line timing”; “Break down polynomial combination timing”; “Tighten prove timing boundaries”).
* **Conducted targeted performance experiments to guide optimization work**: Recorded add-sub fast path experiments and special-form product CUDA timing, generating empirical data to support performance decisions, including GPU-specific behavior (“Record add-sub fast path experiment”; “Record special-form product CUDA timing”).
* **Optimized polynomial product and commitment workflows**: Optimized special-form polynomial products, cached permutation power tables for s0/s1, and batched encoding of independent proof commitments—reducing repeated work and potentially improving throughput in proof-related computations (“Optimize special-form polynomial products”; “Cache permutation power tables for s0 s1”; “Batch encode independent proof commitments”).
* **Improved R1CS data handling for runtime efficiency**: Added R1CS binary sparse uvwXY preload to reduce overhead of loading/processing R1CS structures at runtime (“Use r1cs binary sparse uvwXY preload”).
* **Bounded GPU memory usage in key proof computations**: Implemented tiling to bound GPU R1CS matmul memory, directly addressing operational stability and predictability when running on GPU hardware (PR#194 “Bound GPU R1CS matmul memory with tiling”).
* **Enhanced test coverage around accumulator polynomial behavior**: Added or expanded tests for resizing accumulator polynomial combine, helping validate correctness in polynomial combination pathways (“Test resize accumulator polynomial combine”).
* **Iterated on polynomial degree-bound strategy with reversions**: Introduced conservative polynomial degree bounds and then reverted the change, indicating active validation of correctness/performance tradeoffs in degree handling (“Use conservative polynomial degree bounds”; “Revert ‘Use conservative polynomial degree bounds’”).

## Code Analysis
The +211,214 / -123,228 line movement reflects a period of significant restructuring and distribution work rather than isolated feature additions. Large edits align with packaging and workspace reorganization—splitting the synthesizer into container/node/web packages and establishing a workspace root with debug entrypoints—which typically requires moving code, updating manifests, and reorganizing build outputs (“Restructure synthesizer…”; “Create synthesizer workspace root…”). Similarly, substantial changes are consistent with adding npm-distributed CLI release support and shifting qap-compiler publishing to generated dist artifacts, both of which usually involve build scripts, package metadata, and distribution scaffolding (“Add npm-distributed CLI package…”; “Publish qap-compiler from generated dist package”; PR#189).

The deletion volume is also consistent with iterative stabilization: a large revert of QAP library packaging for CLI runtime and other reversions suggest the team is actively validating release packaging choices and backing out approaches that do not meet runtime or distribution requirements (“Revert ‘fix: package qap library for cli runtime’”; “Revert ‘Use conservative polynomial degree bounds’”). In performance-related areas, additions likely represent new instrumentation (timing boundaries, breakdowns, CUDA timing logs) and optimization pathways (caching permutation power tables, batching proof commitment encoding, special-form polynomial product optimizations) that increase code while making performance measurable and tunable (“Add polynomial arithmetic line timing”; “Tighten prove timing boundaries”; “Cache permutation power tables…”; “Batch encode…”). The presence of GPU memory bounding work (tiling for R1CS matmul) and R1CS preload suggests maturing attention to operational constraints and runtime predictability, which is typical as systems move from experimentation toward repeatable execution profiles (PR#194; “Use r1cs binary sparse uvwXY preload”).

Overall, the net +87,986 lines indicates expansion in tooling, packaging, and observability, while the substantial deletions indicate active cleanup and course-correction—both signals of a codebase being prepared for more reliable distribution and performance-managed operation.

## Next Steps
Based on the current trajectory, the next work is likely to continue stabilizing the packaging/release pipeline (particularly around CLI/runtime and dist publishing) while using the newly added timing and GPU measurements to guide additional performance and memory-efficiency iterations. Further consolidation of the synthesizer workspace and distribution artifacts would be a logical follow-on to the refactors and publishing changes completed in this period.

---


# Tokamak-zk-EVM-contracts

**GitHub**: [Link](https://github.com/tokamak-network/Tokamak-zk-EVM-contracts)


## Overview
Tokamak-zk-EVM-contracts contains on-chain smart contracts and associated tooling used for ZK-EVM verification workflows, bridge deposit/withdrawal operations, and state management. During this period, the work focused on hardening deployment and verification flows (including Sepolia deployments), reducing repository coupling, and restructuring artifacts to support audit and operational readiness—areas that directly affect reliability and maintainability for users and integrators.

## Statistics
| Metric | Value |
|--------|-------|
| Commits | 199 |
| Contributors | 1 |
| Lines Added | +188,687 |
| Lines Deleted | -183,965 |
| Net Change | +4,722 |


## Period Goals
The primary goals were to prepare the bridge and private-state components for a mainnet audit and to make the build/deployment toolchain more reproducible by packaging runtime flows and removing repository submodule dependencies (PR#93, PR#92, PR#91). A second goal was to clean up deployment artifacts and snapshots (including Sepolia runs) so that deployments and verification backends can be tracked and rerun consistently.

## Key Accomplishments
* **Prepared bridge and private-state components for audit readiness**: Consolidated work explicitly aimed at “Prepare bridge and private-state for mainnet audit” (PR#93), improving the project’s ability to undergo external review and reducing ambiguity in deployment and runtime expectations.
* **Removed deployment artifacts from version control to reduce repo noise and risk**: Moved deployment artifacts out of git (“Move deployment artifacts out of git”), eliminating a large volume of tracked generated files and improving clarity around source vs. generated outputs.
* **Rewrote and stabilized private-state CLI end-to-end coverage with refreshed deployment snapshots**: Implemented a substantial rewrite of private-state CLI E2E flows and updated deployment snapshots (“Rewrite private-state CLI E2E and capture refreshed deployment snapshots”), strengthening repeatability and reducing operational friction when validating releases.
* **Fixed private-state dapp artifact resolution and paths**: Corrected artifact path issues (“Fix private-state dapp artifact paths”), reducing deployment/runtime failures attributable to incorrect build output locations.
* **Deployed and recorded Sepolia bridge and private-state dapp runs**: Executed and recorded Sepolia deployments (“Deploy Sepolia bridge and private-state dapp”, “Record Sepolia bridge upgrade deployment”, “Register Sepolia private-state with target inputs”), improving traceability of network changes and providing concrete reference points for stakeholders and auditors.
* **Refreshed verifier cryptographic constants used by Tokamak verification flows**: Updated CRS-related constants (“Refresh Tokamak verifier CRS constants”), supporting correctness and consistency in verification-related operations.
* **Upgraded bridge proof backends for Sepolia**: Updated proof backend components used in the Sepolia bridge context (“Upgrade Sepolia bridge proof backends”), aligning the deployment with updated proving/verification dependencies.
* **Decoupled tooling from internal source submodules and adopted published runtime packages**: Removed Tokamak zkEVM submodule (“Remove Tokamak zkEVM submodule”) and shifted to published runtime packages (“Use published Tokamak runtime packages”), reducing dependency complexity and making builds more reproducible across environments (PR#91).
* **Packaged private-state CLI and normalized outputs for consistency**: Released a CLI version bump (“Bump private-state CLI to 0.1.1”) and normalized byte outputs (“Normalize private-state CLI byte outputs”), improving downstream consumption by scripts and deployment automation (PR#92).
* **Improved Groth16/MPC operational tooling and workspace handling**: Implemented fixed workspace paths for Groth16 proof handling (“Use fixed Groth16 proof workspace paths”) and introduced a Rust-based uploader for Groth16 MPC workflows (“Use Rust Google Drive uploader for Groth16 MPC”), supporting more reliable handling of proving setup artifacts (PR#90).

## Code Analysis
The period’s very large churn (+188,687 / -183,965) reflects two dominant themes evidenced by the commit log: (1) major restructuring of generated artifacts and deployment snapshots, and (2) significant tooling and E2E workflow updates around private-state and bridge operations.

On the addition side, a substantial portion is attributable to expanded/rewritten E2E workflows and snapshot capture for private-state (“Rewrite private-state CLI E2E and capture refreshed deployment snapshots”), along with reorganized snapshot structures (“Restructure deployment artifact snapshots”) and updates to verification constants (“Refresh Tokamak verifier CRS constants”). These additions indicate the repository is not only maintaining contracts but also investing in reproducible operational workflows (deployment tracking, E2E validation, and deterministic output handling).

On the deletion side, the largest single reduction comes from removing tracked deployment artifacts (“Move deployment artifacts out of git”), which accounts for the majority of removed lines and represents a deliberate cleanup to keep the repository focused on source code and controlled snapshots rather than bulky generated outputs. Additional deletions are consistent with reducing coupling and simplifying dependency management (e.g., “Remove Tokamak zkEVM submodule”, “Decouple private-state tooling from Tokamak submodule”), indicating an effort to mature the codebase toward clearer boundaries and more maintainable release processes.

Overall, the net change is modest (+4,722) relative to total churn, which is consistent with a period focused on reorganization, packaging, and operational hardening rather than expanding the contract surface area.

## Next Steps
Work is expected to continue along the audit-readiness path established this period (PR#93), with further refinements to deployment snapshot handling and runtime/tooling packaging to keep Sepolia and subsequent network runs reproducible and well-documented. Ongoing updates to proof backends and verification-related assets are also implied by the recent backend upgrades and CRS refresh commits.


# toki

**GitHub**: [Link](https://github.com/tokamak-network/toki)


## Overview
`toki` appears to be a user-facing web experience supporting Tokamak Network campaigns and interactions, including an event page and a lottery claim flow. The work in this period focused on improving claim-flow usability, event-page presentation, and social sharing metadata—areas that directly affect user conversion, engagement, and the reliability of public-facing campaign distribution.

## Statistics
| Metric | Value |
|--------|-------|
| Commits | 26 |
| Contributors | 1 |
| Lines Added | +3,182 |
| Lines Deleted | -786 |
| Net Change | +2,396 |


## Period Goals
The primary objective during this period was to build and refine the lottery claim journey (including tiering and user flow changes) and to strengthen the event page experience with better visuals, messaging, and embedded media. A second major goal was to stabilize social sharing behavior through improved Open Graph (OG) metadata and platform-specific OG image handling, supported by targeted fixes and cleanup.

## Key Accomplishments
* **Implemented a visual-novel-style lottery claim flow**: Added a “visual novel style flow” to the lottery claim page to guide users through the claim journey in a more structured, narrative sequence (commit: “feat: add visual novel style flow to lottery claim page”).
* **Reworked claim authentication and failure handling**: Dropped login from the claim flow and added “bust retry” behavior with a consolation item, reducing friction while providing clearer outcomes for unsuccessful attempts (commit: “feat: drop login from claim flow, add bust retry with consolation beer”).
* **Introduced and finalized a multi-tier prize ladder**: Added a “bust tier,” reordered the claim flow accordingly, and finalized a five-tier ladder (bust/basic/lucky/super/jackpot), enabling clearer prize segmentation and more explicit user outcomes (commits: “feat: introduce bust tier and reorder lottery claim flow”; “feat: finalize 5-tier prize ladder — bust / basic / lucky / super / jackpot”).
* **Enabled tier-specific prize reveal with live KRW pricing**: Implemented tier-specific prize reveals and displayed a live TOKAMAK-to-KRW price, improving clarity of prize value for KRW-based users (commit: “feat: tier-specific prize reveal with live TOKAMAK KRW price”).
* **Hardened pricing and interaction safety in the claim UI**: Fixed KRW pricing behavior and added “safe re-entry” handling for in-flight discount cards, reducing the risk of inconsistent UI state during user interactions (commit: “feat: fixed KRW pricing and safe re-entry for in-flight discount cards”).
* **Added funnel analytics for the claim process**: Implemented GA4 funnel tracking for the lottery claim flow, improving visibility into user drop-off points and supporting data-driven iteration (commit: “feat: add GA4 funnel tracking to lottery claim flow”).
* **Improved event page presentation and assets**: Added poster effects, introduced a chat light theme, created new button assets, and embedded a launch trailer to enhance event-page clarity and engagement (commits: “feat: event page poster effects, chat light theme, new button assets”; “feat: add Toki launch trailer embed to event page”; plus PR#6).
* **Strengthened maintenance and keyword-response resilience**: Added a “friendly maintenance fallback” and expanded keyword responses to preserve a functional user experience during maintenance or unsupported input cases (commit: “feat: add friendly maintenance fallback and expand keyword responses”).
* **Stabilized social sharing metadata and OG imaging across platforms**: Iterated on OG metadata and OG image strategies, including dynamic OG images featuring the Toki character, canonical-domain fixes, and platform-specific handling (static for Facebook/WhatsApp, dynamic for X), reducing inconsistencies in link previews (commits including: “fix: improve OG metadata for social sharing”; “feat: restore dynamic OG image with Toki character and fix 시뇨리지 typo”; “fix: unify OG image across all platforms using dynamic opengraph-image”; “feat: platform-specific OG images (static for Facebook/WhatsApp, dynamic for X)”; and PRs #8–#13).
* **Resolved UI polish issues on event media/posters**: Removed poster flash issues and prevented scroll jump on poster load while optimizing images, improving perceived quality and reducing UX friction (commit: “fix: prevent scroll jump on poster load and optimize image”; PR#14; plus “refactor: remove SEASON 1 stamp effect from event poster”).

## Code Analysis
The net increase of **+2,396 lines** largely reflects new user-facing functionality in the lottery claim flow and event experience. Significant additions include the visual-novel-style claim progression (+853/-2) and a substantial refactor of the claim journey to remove login and add retry/consolation behavior (+541/-163), alongside tiering mechanics such as the bust tier, five-tier ladder finalization, and tier-specific prize reveal with KRW price integration.

The **-786 lines deleted** indicate meaningful iteration and cleanup, particularly around social-sharing implementation and poster presentation. For example, OG metadata work shows multiple cycles of change (including a large reduction in one commit: “fix: improve OG metadata for social sharing” at +9/-229) and follow-on adjustments to unify OG images and handle platform-specific requirements (dynamic vs static). Poster-related refactors (e.g., removing the “SEASON 1 stamp effect”) and fixes for flash/scroll behavior suggest ongoing refinement and consolidation rather than one-off feature drops.

Overall, the pattern of commits—feature delivery followed by UX/metadata fixes, refactors, and analytics instrumentation—suggests the repository is moving from initial campaign feature build-out toward more reliable operation, measurable funnels, and better presentation consistency across distribution channels.

## Next Steps
Continue iterating on the lottery claim flow based on GA4 funnel insights, focusing on reducing drop-off and improving clarity of outcomes across tiers. Further consolidation of OG/social preview behavior and media-loading polish would reduce ongoing maintenance overhead while improving consistency of external campaign sharing.

---


# trh-backend

**GitHub**: [Link](https://github.com/tokamak-network/trh-backend)


## Overview
trh-backend provides the backend infrastructure used to deploy, register, and manage Tokamak Rollup Hub environments across different providers (notably AWS and local setups). It matters because it operationalizes rollup and related service deployment workflows, including preset-driven configuration, logging/observability hooks, and integration points required for cross-chain or cross-application functionality.

## Statistics
| Metric | Value |
|--------|-------|
| Commits | 25 |
| Contributors | 1 |
| Lines Added | +4,092 |
| Lines Deleted | -425 |
| Net Change | +3,667 |


## Period Goals
This period focused on merging CrossTrade integration into the main codebase, extending deployment automation (especially for AWS), and tightening correctness around presets and fault-proof related configuration. Additional emphasis was placed on deployment reliability and operational visibility through improved logging, guardrails, and retry/timeout behavior.

## Key Accomplishments
* **Integrated CrossTrade into the main backend flow**: Merged CrossTrade integration into main, bringing a large set of backend changes that enable CrossTrade-related deployment and registration workflows to be managed by the service (*feat(cross-trade): merge cross-trade integration into main*).
* **Improved deployment observability and troubleshooting**: Teed `tokamak-deployer` output to both a log file and Docker stdout, increasing the ability to diagnose deployment failures in containerized environments without losing logs (*fix(deployment): tee tokamak-deployer output to log file and Docker stdout*).
* **Enabled account-abstraction operator support for AWS deployments**: Added support to enable the `aa-operator` for AWS deployments and restore it on restart, improving continuity and reducing manual intervention after restarts (*feat(aa): enable aa-operator for AWS deployments + restore on restart*).
* **Extended CrossTrade registration with bridge/messaging components**: Deployed `L1UsdcBridgeAdapter` during CrossTrade L1 registration and wired `L1CrossDomainMessenger` into CrossTrade registration, supporting required L1 components for CrossTrade workflows (*feat(backend): deploy L1UsdcBridgeAdapter during CrossTrade L1 registration*; *fix(backend): wire L1CrossDomainMessenger into CrossTrade registration + bump trh-sdk*).
* **Strengthened reliability with guards, retries, and fatal error handling**: Applied review-driven fixes including a CDM guard, adapter retry logic, and treating contract errors as fatal where appropriate, reducing the likelihood of silent misconfiguration during registration/deployment (*fix(backend): apply codex review — CDM guard + adapter retry + fatal contractsErr*).
* **Standardized and secured FaultProof configuration via presets**: Enabled `FaultProofEnabled` for all presets, added `EnableFaultProof` to `PresetDeployRequest`, verified the DTO field via tests, and ensured the runtime derives the flag from preset definitions rather than client input, reducing configuration drift and limiting incorrect client-driven toggles (*feat(presets): enable FaultProofEnabled for all presets and fix test*; *feat: add EnableFaultProof to PresetDeployRequest and wire from preset_deploy*; *test(dtos): verify EnableFaultProof field on PresetDeployRequest*; *fix(preset): derive EnableFaultProof from preset definition not client input*).
* **Increased deployment robustness through validation and timeouts**: Added a `MonitoringUrl` guard and explicit `json.Marshal` error handling, marked monitoring and DRB as installed after AWS preset deploy, and capped the `deploy-l1-contracts` step at 60 minutes to prevent unbounded waits during automation (*fix(deployment): add MonitoringUrl guard and explicit json.Marshal error handling*; *feat(deployment): mark monitoring and DRB as installed after AWS preset deploy*; *feat(deployment): cap deploy-l1-contracts step at 60 min*).
* **Aligned environment/network wiring and local development correctness**: Corrected the `rollup.json` path used by `BuildLocalChainInformation` and mapped `LocalDevnet` to the SDK network constant `local_devnet`, improving reliability of local/devnet automation paths (*fix(backend): correct rollup.json path in BuildLocalChainInformation*; *fix: map LocalDevnet entity to SDK network constant local_devnet*).

## Code Analysis
The net increase of **+3,667 lines** reflects substantial feature integration and operational enhancements, led by the CrossTrade merge (*feat(cross-trade): merge cross-trade integration into main*, +2213/-267) and major improvements in deployment logging (*fix(deployment): tee tokamak-deployer output to log file and Docker stdout*, +983/-0). Additional new capability was introduced around AWS operational components (enabling and restoring `aa-operator`) and L1 registration plumbing (deploying `L1UsdcBridgeAdapter` and wiring `L1CrossDomainMessenger`) to support CrossTrade registration paths (*feat(aa)...*; *feat(backend): deploy L1UsdcBridgeAdapter...*; *fix(backend): wire L1CrossDomainMessenger...*).

The **-425 lines deleted** are consistent with targeted corrections and tightening of behavior rather than broad refactors: deriving `EnableFaultProof` from preset definitions (reducing reliance on client input), applying review-driven guards and fatal error handling, and fixing wiring/paths and error handling (*fix(preset): derive EnableFaultProof...*; *fix(backend): apply codex review...*; *fix(backend): correct rollup.json path...*; *fix(deployment): add MonitoringUrl guard...*). The presence of DTO tests validating new request fields and multiple defensive checks (guards, explicit marshal error handling, step time caps, adapter retries) indicates the project is investing in operational maturity—reducing ambiguous states in deployment automation and making failures easier to detect and investigate.

## Next Steps
Likely next work will continue hardening the CrossTrade deployment/registration path and expanding test coverage around preset-driven configuration and runtime wiring, building on the recent DTO tests and the guard/retry additions. Ongoing SDK bumps and deployment-step refinements are also expected as the backend tracks changes in `trh-sdk` and deployment tooling.


# trh-platform

**GitHub**: [Link](https://github.com/tokamak-network/trh-platform)


## Overview
trh-platform appears to be a platform repository supporting Tokamak Network operational workflows, with an emphasis on end-to-end (E2E) automation, deployment flows, and UI-guided procedures. The work in this period centers on expanding supported user flows (e.g., CrossTrade token support and update notifications) and increasing reliability and coverage of automated testing (including AWS and Electron-based E2E suites), which matters to users through reduced operational friction and to stakeholders through improved release confidence.

## Statistics
| Metric | Value |
|--------|-------|
| Commits | 15 |
| Contributors | 1 |
| Lines Added | +4,165 |
| Lines Deleted | -3,962 |
| Net Change | +203 |


## Period Goals
The primary goals during this period were to expand product and deployment capabilities in user-facing flows (notably CrossTrade token support and update notifications) while strengthening E2E validation across environments and runtimes. A secondary goal was to reduce accumulated testing artifacts and one-time scripts by consolidating test presets and removing temporary operational tooling once no longer needed.

## Key Accomplishments
* **Expanded CrossTrade support and guidance**: Added USDC token support and updated UI guidance (including “Thanos UI guidance”), alongside Electron E2E coverage for the CrossTrade flow, improving functional breadth and reducing risk when shipping or validating CrossTrade-related changes (*feat(crosstrade): USDC token support, Thanos UI guidance, Electron E2E*).
* **Added AWS-based E2E coverage for fault-proofing**: Introduced a fault proof + AWS E2E test suite, increasing automated verification in a cloud environment and helping catch regressions that may only surface under production-like conditions (*test(e2e): add fault proof + AWS E2E test suite*).
* **Consolidated and migrated E2E presets and UI wizard coverage**: Consolidated E2E configuration to a “full preset only” approach and migrated EFL-01 coverage to a UI wizard flow, reducing fragmentation across test setups and aligning automation with user-driven UI procedures (*test(e2e): consolidate to full preset only, migrate EFL-01 to UI wizard*).
* **Implemented safer update notification handling**: Added a “safe update notification flow,” then followed with image version display and notification routing fixes, improving clarity and correctness of update messaging during runtime changes (*feat: add safe update notification flow*; *feat: add image version display and fix notification routing*).
* **Improved backend runtime and deployment notification validation**: Prepared a backend runtime directory and added a deployment notification test, strengthening operational readiness and providing automated checks around deployment signaling (*feat(docker,test): prepare backend runtime dir + add deployment notification test*).
* **Built and refined Playwright Electron E2E for DRB gaming deployments**: Added a Playwright Electron E2E spec for Gaming+USDT DRB deployment and refined UI-driven testing for “drb gaming electron deployment,” increasing reproducibility and lowering manual effort for validating these deployment paths (*test(07-drb): add Playwright Electron E2E spec for Gaming+USDT DRB deployment*; *test: drive drb gaming electron deployment through ui*).
* **Introduced and then removed one-time operational fix scripts as sessions concluded**: Added AnchorStateRegistry fix scripts for a specific session window and later removed those one-time scripts (as well as one-time AA paymaster setup scripts), reducing long-term maintenance surface and keeping the repository focused on durable tooling (*chore: add AnchorStateRegistry fix scripts (Apr 26-27 session)*; *chore: delete one-time AnchorStateRegistry fix scripts*; *chore: delete one-time AA paymaster setup scripts*).
* **Documented Phase-07 DRB orchestration plans as executable artifacts**: Created four executable PLAN.md files plus a summary for “DRB Regular Operator Orchestration,” improving repeatability and traceability of operator procedures (*docs(phase-07): create 4 executable PLAN.md files + summary for DRB Regular Operator Orchestration*).

## Code Analysis
The +4,165 lines added largely reflect expanded automated testing and new operational flows, especially the addition of an AWS E2E suite for fault-proofing (*test(e2e): add fault proof + AWS E2E test suite*), Electron/Playwright E2E specifications for DRB gaming deployments (*test(07-drb): add Playwright Electron E2E spec for Gaming+USDT DRB deployment*), and CrossTrade enhancements including USDC support and UI guidance (*feat(crosstrade): USDC token support, Thanos UI guidance, Electron E2E*). Additions also include infrastructure and runtime readiness work such as preparing the backend runtime directory and adding deployment notification tests (*feat(docker,test): prepare backend runtime dir + add deployment notification test*), plus application-level improvements to update notifications and version display (*feat: add safe update notification flow*; *feat: add image version display and fix notification routing*).

The -3,962 lines deleted indicate substantial cleanup and consolidation rather than simple churn. The single largest reduction comes from simplifying E2E testing by consolidating to a “full preset only” and migrating coverage to the UI wizard, which removed significant prior configuration or scenario scaffolding (*test(e2e): consolidate to full preset only, migrate EFL-01 to UI wizard*). Additional deletions came from removing transient assets and operational scripts: deleting one-time AnchorStateRegistry fix scripts and AA paymaster setup scripts, and cleaning E2E artifacts such as screenshots while also renaming configuration references and rotating an Alchemy key (*chore: delete one-time AnchorStateRegistry fix scripts*; *chore: delete one-time AA paymaster setup scripts*; *test(e2e): cleanup — delete screenshots, rename paymaster to live, rotate Alchemy key*). Overall, the net change of +203 suggests a maturity trend toward maintaining capability while keeping the codebase lean—adding targeted features and tests while actively removing temporary tooling and redundant test structures.

## Next Steps
Continue expanding and stabilizing E2E coverage for UI wizard and Electron-based deployment flows, particularly across AWS and region-specific configurations. Follow-on work is also implied around further refining notification routing/version visibility and maintaining consolidated test presets as new scenarios are introduced.


# trh-platform-ui

**GitHub**: [Link](https://github.com/tokamak-network/trh-platform-ui)


## Overview
trh-platform-ui is a web-based dashboard used to manage and monitor deployed L2 rollup instances in the Tokamak ecosystem. It matters to users because it guides configuration and deployment choices through preset-driven flows and review screens. For stakeholders, it represents the operational interface that can reduce misconfiguration risk and improve clarity around rollup features and account abstraction (AA) capabilities.

## Statistics
| Metric | Value |
|--------|-------|
| Commits | 9 |
| Contributors | 1 |
| Lines Added | +263 |
| Lines Deleted | -83 |
| Net Change | +180 |


## Period Goals
During this period, work focused on improving the preset wizard and configuration review experience, particularly around fault proof enablement and account abstraction/paymaster messaging. The team also strengthened test coverage to validate fault proof propagation behavior and corrected preset-selection constraints to prevent invalid deployment configurations.

## Key Accomplishments
* **Expanded automated test coverage for fault proof behavior**: Added fault proof propagation tests and updated related preset tests, improving confidence that fault proof settings are correctly applied across preset flows (*test(preset): add fault proof propagation tests*; *feat(preset): enable fault proof for all presets + update tests*).
* **Integrated fault proof visibility into the preset wizard flow**: Added a fault proof indicator in the Full preset wizard and enabled fault proof for all presets, increasing transparency for operators choosing deployment configurations (*feat: add fault proof indicator to Full preset wizard flow*; *feat(preset): enable fault proof for all presets + update tests*).
* **Corrected and standardized AA/paymaster user messaging**: Replaced an incorrect native gas notice with an AA paymaster notice in the configuration review and ensured AA tab/paymaster notice display behavior for all non-TON presets, reducing confusion during configuration validation (*fix(ui): replace incorrect native gas notice with AA paymaster notice in ConfigReview*; *feat(aa): show AA tab and paymaster notice for all non-TON presets*).
* **Tightened preset selection rules to prevent invalid environments**: Blocked Mainnet selection when the infrastructure provider is local, helping avoid deployments that are inconsistent with the chosen infrastructure setup (*fix(preset): block Mainnet selection when infraProvider is local*).

## Code Analysis
The +263/-83 net +180 lines reflect a period centered on feature clarity and correctness in the deployment/configuration UX, backed by additional tests. The largest addition came from new preset-level testing around fault proof propagation (*test(preset): add fault proof propagation tests*), indicating an emphasis on preventing regressions as fault proof settings are enabled across presets (*feat(preset): enable fault proof for all presets + update tests*). On the UI side, changes added a fault proof indicator in the Full preset wizard (*feat: add fault proof indicator to Full preset wizard flow*) and updated AA-related notices, including replacing misleading “native gas” messaging with AA paymaster guidance (*fix(ui): replace incorrect native gas notice with AA paymaster notice in ConfigReview*) and showing the AA tab and paymaster notice for all non-TON presets (*feat(aa): show AA tab and paymaster notice for all non-TON presets*).

The -83 lines deleted are primarily consistent with removing or consolidating UI notices and reducing hardcoded logic—such as removing a “Fault Proof Enabled” notice from a deployment step (*feat: remove Fault Proof Enabled notice from deployment step 3*) and refactoring to replace an AA presets hardcode with a helper function (*refactor(ConfigReview): replace AA_PRESETS hardcode with hasAASupport helper*). Alongside small test robustness improvements (e.g., replacing `as any` with a typed enum in a test: *fix(test): replace as any with RollupType enum in RollupItem test*), this mix suggests incremental maturation: improving correctness through tests, clarifying user-facing configuration signals, and modestly reducing brittle or redundant UI logic.

## Next Steps
Likely next work is to continue refining preset-driven configuration flows and associated tests as fault proof and AA behavior evolves, ensuring the wizard, review screens, and validation rules remain consistent. Additional follow-on refactors may further centralize capability checks (e.g., helpers like `hasAASupport`) to keep UI logic maintainable as preset options expand.


# trh-sdk

**GitHub**: [Link](https://github.com/tokamak-network/trh-sdk)


## Overview
trh-sdk is a developer SDK focused on deploying custom Layer 2 rollups on Tokamak Rollup Hub with minimal configuration. It packages deployment orchestration, preset-driven environment setup, and post-deploy initialization paths into a single toolchain, reducing manual steps required to stand up L2 environments. For users and investors, it is an enabling component for expanding the number and variety of rollups deployed through the Tokamak ecosystem.

## Statistics
| Metric | Value |
|--------|-------|
| Commits | 79 |
| Contributors | 1 |
| Lines Added | +47,728 |
| Lines Deleted | -2,200 |
| Net Change | +45,528 |


## Period Goals
This period concentrated on expanding deployment and initialization coverage for Tokamak Rollup Hub rollups, with a particular emphasis on DRB flows (including peer ID bootstrapping and account orchestration) and improving preset-based deployments (e.g., gaming and non-TON fee token configurations). The work also aimed to integrate CrossTrade where relevant and to strengthen correctness via behavior and end-to-end test additions, while addressing deployment reliability issues and targeted security review feedback.

## Key Accomplishments
* **Integrated CrossTrade support and compatibility shims**: Added cross-trade integration along with compatibility shims for trh-backend, and implemented automatic CrossTrade installation on AWS for DeFi/Full presets, improving interoperability and reducing manual setup during deployments (*“feat: add cross-trade integration and compatibility shims for trh-backend”*, *“feat(sdk): auto-install CrossTrade on AWS for DeFi/Full presets”*).
* **Implemented DRB peer identity bootstrapping and activation workflows**: Added peer ID bootstrap logic and on-chain operator activation, and implemented peer ID derivation plus DRBAccounts orchestration—advancing DRB deployment readiness across staged “Wave” milestones (*“feat(07-02-drb): peer ID bootstrap + on-chain operator activation (Wave 1→2 GREEN)”*, *“feat(phase-7): implement peer ID derivation + DRBAccounts orchestration (Wave 1 GREEN)”*).
* **Expanded genesis and node orchestration for rollup bring-up**: Orchestrated forge L2Genesis alongside op-node to support the genesis step, improving automation of the initial chain setup workflow (*“feat(deployer): orchestrate forge L2Genesis + op-node for genesis step”*).
* **Added and validated preset-specific deployment paths (gaming, token presets)**: Unblocked gaming preset deployment and wired local DRB orchestration for gaming presets, increasing confidence that preset configurations can be deployed consistently in local scenarios (*“fix(thanos/local/drb): unblock gaming preset deploy (bugs #5/#6a/#6b)”*, *“fix: wire drb local orchestration for gaming presets”*).
* **Improved account abstraction funding behavior for fee-token presets**: Funded AA admin in genesis for non-TON fee token presets and addressed high-severity issues raised in a Codex review around AA genesis funding, reducing the risk of misconfigured genesis state for alternative fee-token rollups (*“feat: fund AA admin in genesis for non-TON fee token presets”*, *“fix(thanos): address Codex review HIGH issues in AA genesis funding”*).
* **Implemented DGF initialization path and core contract upgrade steps**: Added a DGF init path that includes FaultDisputeGame deployment and a Portal2 upgrade, extending the SDK’s ability to execute structured post-deploy initialization and upgrades (*“feat(sdk): implement DGF init path — FaultDisputeGame deploy + Portal2 upgrade”*).
* **Hardened post-deploy initialization and registry fallback behavior**: Added CDM post-deploy initialization and an L2CDM predeploy constant, and implemented a StorageSetter fallback for AnchorStateRegistry variants lacking setInitialAnchorState (RC3), increasing compatibility across contract versions and reducing deployment-time failure modes (*“fix(sdk): StorageSetter fallback for AnchorStateRegistry without setInitialAnchorState (RC3)”*, *“fix(sdk): CDM post-deploy init + L2CDM predeploy constant”*).
* **Expanded automated test coverage for DRB and preset deployments**: Added behavior tests for DRB wiring (Wave 0) and an SDK integration E2E test for the Gaming+USDT DRB flow (Wave 2), and verified all four preset modules for AWS deployment correctness, improving regression detection for critical deployment paths (*“test(phase-6): add behavior tests for DRB wiring (Wave 0 RED)”*, *“test(07-03-drb): SDK integration E2E test for Gaming+USDT DRB flow (build tag drb_e2e; Wave 2)”*, *“test(thanos): verify all 4 preset modules for AWS deployment correctness”*).
* **Improved deployment robustness and shutdown/config resolution**: Fixed infinite loops, bridge silent failure, and prestate guard behavior in deployment, and corrected shutdown logic to resolve deploy-config.json at the new tokamak-deployer path, reducing operational risk during deployment and teardown (*“fix(deploy): fix infinite loops, bridge silent failure, and prestate guard”*, *“fix(thanos/shutdown): resolve deploy-config.json at new tokamak-deployer path”*).
* **Managed lint-driven cleanup with controlled rollback**: Removed unused code detected by golangci-lint and then reverted that change, indicating active code hygiene work while prioritizing stability when automated removals caused issues (*“fix(lint): remove unused code detected by golangci-lint”*, *“Revert "fix(lint): remove unused code detected by golangci-lint"”*).
* **Consolidated work via major branch synchronization**: Merged main into a feature branch related to cross-trade updates, bringing changes into alignment and indicating parallel development tracks being reconciled (*“chore: merge origin/main into feat/update-cross-trade”*).

## Code Analysis
The very large net increase (+45,528) is primarily explained by substantial feature additions and integration scaffolding, including a major merge from main into a cross-trade-related feature branch (*“chore: merge origin/main into feat/update-cross-trade”*), and new DRB functionality such as peer ID bootstrapping/derivation and account orchestration (*“feat(07-02-drb)…peer ID bootstrap + on-chain operator activation”*, *“feat(phase-7)…peer ID derivation + DRBAccounts orchestration”*). Additional new capability appears in deployment orchestration (forge L2Genesis + op-node) and expanded initialization/upgrade paths (FaultDisputeGame deploy + Portal2 upgrade; CDM post-deploy init and constants), reflecting a shift toward end-to-end automation rather than manual, operator-driven steps (*“feat(deployer): orchestrate forge L2Genesis + op-node…”*, *“feat(sdk): implement DGF init path — FaultDisputeGame deploy + Portal2 upgrade”*, *“fix(sdk): CDM post-deploy init + L2CDM predeploy constant”*).

The deletions (-2,200) are comparatively modest and include targeted cleanup and rework: a lint-driven removal of unused code that was subsequently reverted, suggesting that while code hygiene is being pursued, stability and correctness are being prioritized when automated refactors introduce risk (*“fix(lint): remove unused code…”*, *“Revert…”*). Multiple “fix” commits addressing deployment failure modes (infinite loops, bridge silent failure, prestate guard) and configuration resolution in shutdown indicate active stabilization of operational workflows, while compatibility-oriented fixes (AnchorStateRegistry fallback; trh-backend compatibility shims) indicate the SDK is being hardened to work across varying environments and contract interfaces (*“fix(deploy)…”, “fix(thanos/shutdown)…”, “fix(sdk): StorageSetter fallback…”*, *“feat: add cross-trade integration and compatibility shims for trh-backend”*). Overall, the pattern of large feature additions paired with growing test coverage (behavior tests, E2E DRB flow tests, AWS preset verification) suggests the repository is moving toward broader scenario coverage and improved reliability for repeatable deployments (*“test(phase-6)…”, “test(07-03-drb)…”, “test(thanos): verify all 4 preset modules…”*).

## Next Steps
Based on the current trajectory of DRB “Wave” milestones and the newly added behavior/E2E tests, the next likely focus is completing remaining DRB wiring and continuing to convert discovered issues into fixes validated by automated tests. Continued refinement of preset deployments (local and AWS) and compatibility paths (e.g., registry/initialization fallbacks and backend shims) would further reduce operator burden and deployment risk.


# trh-wiki

**GitHub**: [Link](https://github.com/tokamak-network/trh-wiki)


## Overview
trh-wiki is a documentation and knowledge-base repository supporting Tokamak Network operational workflows, with an emphasis on deployment tooling and troubleshooting for L2 and related components. It matters because it consolidates repeatable deployment guidance, known-issue analyses, and concrete fixes into written procedures that reduce execution risk and shorten time-to-resolution for engineers and operators.

## Statistics
| Metric | Value |
|--------|-------|
| Commits | 36 |
| Contributors | 1 |
| Lines Added | +3,231 |
| Lines Deleted | -215 |
| Net Change | +3,016 |


## Period Goals
During this period, the primary goal was to expand and harden operational documentation around deployment methods and deployment tooling (notably tokamak-deployer and thanos-deployer), including measured behavior and configuration guidance. A second focus was to capture troubleshooting playbooks for recurring and newly discovered issues (e.g., genesis problems, blob fee calculation bugs, DisputeGameFactory and oracle initialization issues) and to track fixes across versions and presets.

## Key Accomplishments
* **Documented deployment method tradeoffs**: Added a deploy-methods comparison focusing on Deploy.s.sol versus tokamak-deployer, helping operators choose an approach with clearer expectations and fewer trial-and-error cycles (commit: “ingest: deploy-methods-comparison — Deploy.s.sol vs tokamak-deployer”).
* **Published Thanos deployer deployment analysis**: Added an analysis of thanos-deployer deployment, improving decision-making and reducing uncertainty for teams evaluating deployment tooling options (commit: “docs(wiki): add thanos-deployer deployment analysis”).
* **Captured tokamak-deployer gas pricing and measurement behavior**: Ingested updates describing tokamak-deployer v0.0.5, including a fixed gas price strategy and Sepolia measurements, providing concrete operational guidance for cost/risk management during deployments (commit: “ingest: tokamak-deployer v0.0.5 fixed gas price strategy + Sepolia measurement”).
* **Added logging documentation for tokamak-deployer**: Documented tokamak-deployer v1.0.1 logging, improving observability during deployments and enabling faster diagnosis when runs fail or behave unexpectedly (commit: “docs(wiki): add tokamak-deployer v1.0.1 logging documentation”).
* **Strengthened DRB preset troubleshooting coverage and bug tracking**: Expanded and corrected troubleshooting for DRB “gaming preset” and runtime verification, explicitly recording fixed items (bugs #5/#6, then #5/#7 verified) and newly identified issues (bug #7 new; bug #8 new) to support predictable remediation workflows (commits: “docs(troubleshooting): drb gaming preset — bugs #5/#6 fixed, bug #7 new”; “docs(troubleshooting): drb runtime verify — Fix #5/#7 verified + Bug #8 신규”).
* **Recorded multiple DRB deployment and compose-template issues with follow-ups**: Ingested five DRB preset deploy bugs tied to local compose path templates, then updated documentation to confirm one issue and add a newly identified bug, supporting more reliable “local compose” based deployments (commits: “ingest: drb-local-compose-path-template-bugs — 5 DRB preset deploy bugs (2026-04-17)”; “update: drb-local-compose-path-template-bugs — Bug #4 확정 + Bug #6 신규”).
* **Documented and corrected blob fee–related issues under Pectra/Cancun logic**: Added documentation on an op-node Pectra blobBaseFee issue (noting use of CalcBlobFeeCancun) and then updated troubleshooting to reflect the actual root cause, improving accuracy of on-call guidance for fee-related incidents (commits: “docs: op-node Pectra blobBaseFee bug — CalcBlobFeeCancun 고정 사용 및 수정”; “fix(troubleshooting): document actual root cause of Pectra blobBaseFee bug”).
* **Added targeted troubleshooting for critical chain components and genesis flow**: Created new pages for silent/slow behavior in the forge-l2genesis step, L2OutputOracle uninitialized states, and depositAndActivate threshold mismatches—each aimed at reducing downtime and shortening diagnosis for common failure modes (commits: “docs(forge-l2genesis-silent-slow): add troubleshooting page for silent/slow L2 genesis step”; “docs: L2OutputOracle uninitialized troubleshooting page”; “docs: add DRB depositAndActivate threshold mismatch troubleshooting page”).
* **Documented fault-proof and dispute-game related failure mode and remediation**: Added documentation for DisputeGameFactory having no implementations (Bug #8 pre-v0.0.6) and a storageSetterBytecode fix, and wired the `--fault-proof` flag in DRB local compose documentation/flow to prevent misconfiguration (commits: “doc: DisputeGameFactory no implementations (Bug #8 pre-v0.0.6) + storageSetterBytecode fix”; “docs(drb-local-compose): Bug #8 fixed — --fault-proof flag wired (+52/-29)”).
* **Consolidated cross-trade E2E findings and operational guidance**: Documented three root-cause fixes from a cross-trade E2E run, confirmed USDC addresses, added Thanos UI guidance, and recorded USDC E2E tests—improving repeatability and reducing integration friction for teams running CRT flows (commits: “docs(cross-trade): document 3 root-cause fixes from CRT E2E run (2026-04-19)”; “docs(cross-trade): USDC addresses confirmed, Thanos UI guidance, USDC E2E tests documented”).
* **Recorded configuration fixes for blob fee thresholds and rollup.json pathing**: Ingested fixes related to `safe_l2=0` blob fee threshold behavior and incorrect rollup.json paths, reducing configuration-induced deployment failures (commit: “ingest: safe_l2=0 blob fee threshold + rollup.json wrong path fixes”).
* **Documented gaming enablement orchestration and genesis mismatch root cause**: Added documentation for DRB v1.1 gaming enablement (genesis predeploy + regular orchestration) and separately documented the root cause and fix for a gaming/full preset genesis hash mismatch (RC1), supporting consistent network initialization outcomes (commits: “docs(drb): document v1.1 Gaming Enablement (genesis predeploy + Regular orchestration)”; “docs: Gaming/Full preset genesis hash mismatch (RC1) 근본 원인 및 수정 문서화”).

## Code Analysis
The +3,231 lines added largely represent new or substantially expanded documentation pages that codify deployment comparisons, tool behavior, and troubleshooting playbooks. Examples include the deployment method comparison between Deploy.s.sol and tokamak-deployer, thanos-deployer deployment analysis, and operational notes for tokamak-deployer versions v0.0.5 (gas price strategy and Sepolia measurement) and v1.0.1 (logging documentation). A significant portion of additions also target incident response readiness: new pages for silent/slow L2 genesis steps, L2OutputOracle uninitialized states, depositAndActivate threshold mismatches, and detailed write-ups of blobBaseFee issues in op-node under Pectra/Cancun logic, including a subsequent correction to document the actual root cause.

The -215 lines deleted suggest iterative refinement rather than removal of capability—evidenced by commits that both add and revise troubleshooting content (e.g., correcting the Pectra blobBaseFee root cause documentation, and updates to DRB local compose and bug-tracking pages). Overall, the net increase indicates the repository is in a knowledge-capture and stabilization phase: converting operational learnings (bugs, E2E root causes, version-specific behaviors) into maintained procedures that reduce execution risk and support repeatable deployments.

## Next Steps
Continue updating troubleshooting pages as additional DRB and deployer versions are validated in practice (e.g., following up on newly logged bugs such as DRB bug #8 and any subsequent fixes). Expand and maintain the deployment and E2E runbooks so operational guidance stays aligned with evolving tooling behavior and configuration requirements.


# trust-claim

**GitHub**: [Link](https://github.com/tokamak-network/trust-claim)


## Overview
trust-claim is the codebase for “TrustClaim,” a claims and verification experience that includes a user-facing application, identity/wallet binding workflows, protocol-aware verification logic, and agent-oriented access patterns. Within the Tokamak Network ecosystem, it matters as an implementation effort focused on making claims creation, review, and verification more usable (UI/UX and narrative views) and more automatable (agent tooling and MCP server), with explicit work toward multi-asset payment support and verifiers for common onchain primitives.

## Statistics
| Metric | Value |
|--------|-------|
| Commits | 19 |
| Contributors | 1 |
| Lines Added | +32,703 |
| Lines Deleted | -1,228 |
| Net Change | +31,475 |


## Period Goals
This period focused on moving from an initial Phase 0 pilot scaffold into a Phase 1/1.5 feature set spanning claims creation, payments, identity binding, and verification. In parallel, the repository added agent-first interfaces (MCP server, bots, per-claim agent endpoints) and strengthened the product surface with editorial redesign, richer claim pages, and targeted frontend fixes and documentation updates.

## Key Accomplishments
* **Established a Phase 0 pilot foundation**: Implemented the initial pilot scaffold to provide a working baseline for subsequent phases and feature delivery (“Initial Phase 0 pilot scaffold”).
* **Delivered core discovery and communication functionality**: Shipped a discovery + communication sprint covering six stories, expanding early product capabilities and user flows (“feat: discovery + communication sprint — 6 stories shipped”).
* **Implemented Phase 1 payments and AI-assisted claim drafting**: Added multi-asset payment support and AI-drafted claims, directly expanding monetization/payment flexibility and improving claim authoring throughput (“feat: Phase 1 multi-asset payments + AI-drafted claims”).
* **Upgraded the public-facing UI with an editorial redesign**: Introduced redesigned visuals (hero imagery, ticker, seal, fingerprint) to improve presentation and readability of the experience (“feat: editorial redesign with hero imagery, ticker, seal, fingerprint”).
* **Expanded identity capabilities through multi-platform wallet binding**: Delivered an “8-platform wallet binding” sprint and associated brand-icon UI, improving identity linkage coverage and user clarity during binding flows (“feat(identity): 8-platform wallet binding sprint + brand-icon UI”).
* **Added protocol-aware verification logic for common assets and DEXs**: Implemented a verifier with awareness of Uniswap V2/V3 and ERC-20 behavior, improving the system’s ability to evaluate claims tied to widely used onchain protocols (“feat: Phase 1.5 protocol-aware verifier (Uniswap V2/V3 + ERC-20)”).
* **Enabled agent-first integration and automation paths**: Added an MCP server for agent-oriented access and included demo automation agents (claimant/challenger) plus a natural-language claimant bot CLI via LiteLLM, supporting programmatic workflows around claims (“feat(mcp): TrustClaim MCP server for agent-first access”, “feat(agents): autonomous claimant + challenger demo bots”, “feat(agents): natural-language claimant bot CLI via LiteLLM”).
* **Improved claim/agent presentation and crawlability**: Added claim and agent UI surfaces including a narrative view on `/c/[id]`, per-claim agent endpoint with inline preview, `/agents/[address]` profiles, and LLM crawler files (`/llms.txt`, `/llms-full.txt`) to make content and agent-related data easier to access and index (“feat(frontend): visualize agent-vs-agent narrative on /c/[id]”, “feat(c/[id]): per-claim agent endpoint with inline preview”, “feat(frontend): /agents/[address] profile + agent column on /explore”, “feat(frontend): add /llms.txt + /llms-full.txt for LLM crawlers”).

## Code Analysis
The net addition of **+31,475 lines** largely reflects a repository moving quickly from a scaffolded pilot into a multi-surface application with new subsystems. Large additions map directly to new functional areas: the initial Phase 0 scaffold (+9,111), a substantial discovery/communication implementation (+8,347), Phase 1 multi-asset payments plus AI-drafted claims (+6,283), identity wallet binding across multiple platforms (+1,833), and Phase 1.5 protocol-aware verification for Uniswap V2/V3 and ERC-20 (+1,641). The period also introduced agent infrastructure and tooling—an MCP server (+1,056), autonomous demo bots (+556), and a LiteLLM-based CLI (+187)—indicating explicit investment in automation and agent-driven interaction paths alongside the user interface.

The **-1,228 lines deleted** are consistent with iterative refinement rather than pure expansion. Deletions appear alongside UI/UX changes (editorial redesign with notable churn, +1,779/-330), implementation adjustments to the X OAuth 2.0 flow that was explicitly parked due to the X API becoming paid-only (+269/-157), and targeted frontend fixes (e.g., resolving an infinite render and hydration issues on `/c/3`, +49/-12). Smaller “cleanup/consistency” work (English-only UI strings alignment, +15/-15; README translation to English, +80/-31; satori OG layout and purity changes, +159/-10) suggests the codebase is beginning to formalize presentation, documentation, and correctness checks while still in active feature build-out.

Overall, the magnitude and distribution of changes indicate a phase of rapid capability build (payments, verification, identity, agent access) coupled with early stabilization work (bug fixes, layout corrections, i18n/string alignment), which is typical of a project transitioning from pilot scaffolding into broader usability and integration readiness.

## Next Steps
Near-term work is likely to continue along the established Phase 1/1.5 trajectory by extending protocol-aware verification coverage and hardening the agent access surfaces introduced this period (MCP server, per-claim agent endpoints, and agent UIs). The parked X OAuth flow may be revisited if external API constraints change (“feat(backend): X OAuth 2.0 flow (parked — X API now paid-only)”).


# zk-card-wallet

**GitHub**: [Link](https://github.com/tokamak-network/zk-card-wallet)


## Overview
zk-card-wallet is a multi-component codebase focused on enabling a card-backed wallet flow that integrates secure element (JCOP 4) signing, mobile wallet UX, and zero-knowledge proof interoperability. It matters in the Tokamak ecosystem because it combines user-facing mobile wallet operations (pairing, PIN management, sending assets) with verifiable identity/enrollment primitives (circuits, verifiers, and registry contracts) that can support privacy-preserving and attestable interactions.

## Statistics
| Metric | Value |
|--------|-------|
| Commits | 386 |
| Contributors | 1 |
| Lines Added | +112,449 |
| Lines Deleted | -13,331 |
| Net Change | +99,118 |


## Period Goals
During this period, the work centered on standing up the end-to-end foundation for a card-based zk wallet: secure-element signing primitives, a functional mobile client, and the proving/verification and registry layers needed for enrollment and identity verification. In parallel, the team advanced circuit work (including enrollment and daily proof scaffolding), introduced a prover server for enrollment, and improved determinism and security-audit documentation around contract behavior and attack surface.

## Key Accomplishments
* **Implemented dual-signer support on JCOP 4**: Added BabyJubJub + Curve25519 dual-signer functionality with BIP39, zk interoperability, and PIN handling on the secure element (“Initial: BabyJubJub + Curve25519 dual-signer on JCOP 4 with BIP39, zk interop, PIN”), strengthening the project’s hardware-backed signing foundation.
* **Established a mobile development baseline and progressively ported the SDK**: Created an initial Expo Dev Client scaffolding and executed multiple porting phases covering transport, curve math, and smart card integration (“feat(mobile): initial Expo Dev Client scaffolding (Phase 1)”, “Phase 2a — foundation SDK port (transport + curve + SC)”), enabling iterative delivery of wallet features on a modern mobile stack.
* **Built core wallet abstractions and BIP39 derivation in the app layer**: Introduced CardWallet/CardBjjWallet structures and BIP39 derive logic (“Phase 2c — CardWallet + CardBjjWallet + BIP39 derive”), supporting deterministic wallet creation and consistent key management flows for users.
* **Delivered pairing and PIN-related operational flows**: Added pairing with TOFU and PIN/pair operations using keychain-based storage and fixed a change-PIN pairing issue (“Phase 2b — pairing + TOFU + PIN/pair-ops (keychain-based)”, “mandatory ETH activation + 4-tab IA + pair CHANGE_PIN fix”), improving practical device onboarding and credential lifecycle handling.
* **Implemented end-to-end ETH transfer UX and token management surfaces**: Added SendScreen/SendService for ETH transfers and introduced an ERC-20 registry with a TokenSettingsScreen (“Phase 6.5 — SendScreen + SendService (ETH transfer end-to-end)”, “Phase 6.6a — ERC-20 registry + TokenSettingsScreen”), expanding functionality from setup toward everyday wallet usage.
* **Added key material decryption capabilities (SEED / SEED-CBC / NPKI)**: Ported SEED + SEED-CBC and NPKI decrypt logic into both mobile and host-node paths (“Phase 7.2b — SEED + SEED-CBC + NPKI decrypt (TS port)”, “host-node: Phase 7.2a-2 — SEED-CBC + PBES2 + NPKI key decrypt”), supporting interoperability with encrypted key containers and certificate-related workflows referenced in later circuit/contract work.
* **Advanced zero-knowledge circuit development for recurring proofs and enrollment**: Added “daily proof v1” scaffolding including a Schnorr-on-commit circuit and implemented enrollment-v1 Groth16 trusted setup with explicit public signal sizing (“feat(circuits): daily proof v1… Schnorr-on-commit circuit”, “PR#289: enrollment-v1 — groth16 trusted setup + nPublic=18 vkey”), laying groundwork for verifiable actions beyond basic wallet operations.
* **Expanded X.509-related circuit parsing utilities**: Implemented X509Parser offsets/length extraction for TBS parsing (“PR#298: X509Parser tbsHeaderOffset + tbsValueLen”), improving the circuit-side ability to reference structured certificate components deterministically.
* **Introduced an enrollment prover server and contract verification stack**: Added an enrollment prover server using Node + snarkjs over HTTP and implemented Solidity Groth16 verifier plus an IdentityRegistry skeleton and EnrollmentVerifier (“feat(prover-server): enrollment prover server v0 (Node + snarkjs HTTP)”, “Solidity Groth16 verifier + IdentityRegistry skeleton (v1)”, “IdentityRegistry.enroll + EnrollmentVerifier”), enabling an end-to-end path from proof generation to on-chain verification.
* **Refined contract interfaces and deployment/fixtures for determinism and maintainability**: Rewired the v1 enroll signature to accept `uint256[18]` plus `bytes32[4]` and added a deployment script for the v0 registry stack and deterministic fixture generation safeguards (“PR#297: v1 enroll(uint256[18], bytes32[4]) rewire”, “PR#285: deploy script for v0 registry stack”, “generate-fixture.js v1 _mock + determinism guard”), supporting consistent builds, testing, and predictable on-chain integration.
* **Made verifier regeneration more robust and documented security posture**: Updated verifier regeneration to be `nPublic`-agnostic and cleaned filename derivation, while refreshing security-audit documentation on gas baseline, attack-surface analysis, and revoked-gate items (“PR#279… nPublic-agnostic”, “PR#290… strip -v<N> suffix…”, “PR#281/282/283… security-audit updates”), improving maintainability and stakeholder visibility into contract risk considerations.
* **Reduced external crypto dependencies by in-repo math porting**: Ported BabyJubJub to in-repo math and removed circomlibjs (“chore(mobile): port BabyJubJub… remove circomlibjs”), tightening dependency control and easing reproducibility across environments.

## Code Analysis
The +112,449 lines added largely represent first-time implementation across multiple layers of the system: secure element signing support (“BabyJubJub + Curve25519 dual-signer on JCOP 4…”), a substantial mobile application build-out (Expo scaffolding; phased SDK ports; wallet flows like pairing, PIN operations, ETH activation, SendService, and token settings), and the zk proving/verifying pipeline (daily proof circuit scaffolding, enrollment-v1 trusted setup and wiring, an HTTP prover server, and Solidity verifier/IdentityRegistry work). Additions also include infrastructure for determinism and deployment (fixture generation determinism guard; deploy script for registry stack) and vendorized cryptographic test vectors (“vendor(circuits): … keccak-256 + golden-vector tests”).

The -13,331 lines deleted are consistent with targeted refactoring and dependency reduction rather than feature removal. The most explicit example is removing circomlibjs after porting BabyJubJub math in-repo (“remove circomlibjs”), and contract tooling refactors that generalize verifier regeneration and tidy naming conventions (“make verifier regen nPublic-agnostic”, “strip -v<N> suffix…”). The scale and distribution of changes indicate the repository is in an active build-out phase, with initial implementations being solidified through interface rewires (e.g., enroll signature changes) and maintainability improvements (regen generalization, determinism guards, and audit documentation updates).

## Next Steps
Near-term work should continue completing and hardening the enrollment and proof pipeline across circuits, prover-server, and contracts, building on the enrollment-v1 trusted setup, signal wiring, and `enroll()` rewires already landed. The mobile client is positioned for further feature completion and stabilization following the phased SDK ports, pairing/PIN fixes, and initial send/token management implementations.