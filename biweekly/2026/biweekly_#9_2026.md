# Tokamak Network Development Report

**2026-06-01 - 2026-06-15**

Tokamak Network: 505,233 Code Changes Across 16 Active Projects  
Net growth of 412,831 lines reflects sustained delivery velocity with relatively low deletion volume  

From 2026-06-01 to 2026-06-15, engineering activity spanned 16 Active Projects and produced 505,233 Code Changes. These changes included 459,032 lines added and 46,201 lines deleted, resulting in a net increase of 412,831 lines. The scale of additions indicates substantial expansion of code and capabilities during the period, while deletions suggest targeted refinement rather than broad removal. Overall, the numbers represent a high-volume development cycle with clear net codebase growth.

---

# all-thing-eye

**GitHub**: [Link](https://github.com/tokamak-network/all-thing-eye)


## Overview
This repository appears to support operational workflows around member data handling and reporting, including export pipelines and email-based distribution. The work in this period focuses on adding an archival pathway for “retired members,” improving data export reliability, and introducing tooling for subscriber management and local development—all of which reduces operational risk around reporting and data lifecycle management.

## Statistics
| Metric | Value |
|--------|-------|
| Commits | 12 |
| Contributors | 1 |
| Lines Added | +4,475 |
| Lines Deleted | -95 |
| Net Change | +4,380 |


## Period Goals
This period concentrated on consolidating report distribution capabilities into all-thing-eye and establishing a structured approach for retired-member data archival. In parallel, the team aimed to make exports safer and more reversible (rollback/import scripts), while smoothing day-to-day operations through local-run tooling, UI for subscriber management, and targeted bug fixes.

## Key Accomplishments
* **Implemented a dedicated retired-members archival scaffold using a separate-DB approach**: Added the structural groundwork to handle “retired members” as an archive domain rather than mixing with active member data, supporting cleaner data lifecycle separation and reducing the likelihood of operational mistakes during reporting or exports (commit: `checkpoint(archive): retired-members archive scaffold (separate-DB approach)`).
* **Ported biweekly report email distribution into this repository**: Integrated report distribution logic directly into all-thing-eye, centralizing operational reporting and reducing reliance on external/manual processes for scheduled communications (commit: `feat(report-distribution): port biweekly report email distribution into all-thing-eye`).
* **Delivered subscriber management capabilities, including a UI and stdin-based import**: Added mechanisms to manage report distribution recipients more maintainably, enabling updates via an interface and bulk ingestion via standard input for operational flexibility (commit: `feat(report-distribution): subscriber management UI + stdin import`).
* **Added reversible retired-member import tooling with rollback scripts**: Introduced import paths for retired-member data with explicit rollback support, improving recoverability and lowering the risk of irreversible data changes during migrations or operational corrections (commit: `feat(unified-export): reversible retired-member import + rollback scripts`).
* **Isolated archived data into a dedicated collection and updated exports accordingly**: Refactored “retired members” handling into an `archive_members` collection and adjusted custom export logic to read from `archive_members` and `member_artifacts`, improving data organization and simplifying export correctness (commits: `refactor(unified-export): retired members -> isolated archive_members collection`, `feat(unified-export): custom-export reads archive_members + member_artifacts`).
* **Expanded export outputs with per-member tenure CSV and archive sourcing**: Added export capabilities that generate tenure-oriented CSVs per member and explicitly draw from archive sources in custom-export, improving traceability and enabling more granular downstream analysis (commit: `feat(export): per-member tenure-data CSV + archive source in custom-export`).
* **Introduced member materials import into a dedicated artifacts store**: Routed member materials ingestion into `ati.member_artifacts`, separating artifacts from core member records and supporting more structured export and archival workflows (commit: `feat(unified-export): member materials import -> ati.member_artifacts`).
* **Improved operability through local-run scripting, documentation, and targeted fixes**: Added a one-command local runner plus a dev-only auth bypass to speed up development iteration, documented local-dev Mongo/Drive “gotchas,” fixed a GraphQL crash when members have no email, and tightened git hooks to trigger backend rebuilds on relevant changes (commits: `chore(dev): add run-local.sh one-command runner + dev-only auth bypass`, `docs(skills): capture local-dev + mongo/drive gotchas as learned skills`, `fix(graphql): members query crashed on members with no email`, `fix(git-hooks): trigger backend rebuild on src/ and requirements.txt changes`).

## Code Analysis
The +4,475 lines added largely reflect new functional surfaces rather than minor tweaks: a substantial portion is attributable to the retired-members archive scaffold and related “separate-DB” setup (`checkpoint(archive): retired-members archive scaffold...`), as well as porting biweekly report email distribution into this codebase (`feat(report-distribution): port biweekly report email distribution...`). Additional additions correspond to operational tooling and data pipeline work—rollback scripts for reversible imports (`feat(unified-export): reversible retired-member import + rollback scripts`), subscriber management UI and stdin import (`feat(report-distribution): subscriber management UI + stdin import`), and expanded export formats (tenure CSVs, archive sourcing) (`feat(export): per-member tenure-data CSV + archive source...`).

The -95 lines deleted suggest light refactoring and cleanup rather than removal of major functionality. This is consistent with reorganizing data handling by isolating retired members into an `archive_members` collection (net reshaping of data model usage) (`refactor(unified-export): retired members -> isolated archive_members collection`) and small, focused fixes (GraphQL query crash and git-hook tweak). Overall, the mix of large feature adds with modest refactors and stability fixes indicates a phase of capability build-out (archival + distribution + export) while beginning to enforce clearer separation of concerns in the data model and improving day-to-day operability.

## Next Steps
Next work should logically follow from the newly introduced archive and distribution components: continuing to harden the retired-member archival and export flows (especially around reversible operations) and iterating on report distribution management based on operational feedback. Further incremental stabilization is also implied by the targeted bug fixes and developer tooling added during this period.


# bi-weekly-quarterly-reports

**GitHub**: [Link](https://github.com/tokamak-network/bi-weekly-quarterly-reports)


## Overview
This repository serves as a centralized record for Tokamak Network’s bi-weekly and quarterly reporting materials, providing a durable, versioned history of updates over time. For users and investors, maintaining reports in a Git-based repository improves traceability (what changed, when, and by whom) and supports consistent disclosure practices across reporting periods.

## Statistics
| Metric | Value |
|--------|-------|
| Commits | 1 |
| Contributors | 1 |
| Lines Added | +3,104 |
| Lines Deleted | -0 |
| Net Change | +3,104 |


## Period Goals
During this period, the primary objective appears to have been populating or expanding the repository’s contents by adding report-related files in a single upload. With no PRs recorded and a single bulk commit, the focus was on establishing or updating the reporting corpus rather than iterative revisions.

## Key Accomplishments
* **Added a new set of repository files via upload**: Introduced a substantial body of new material in one commit (“Add files via upload”), increasing the repository’s tracked content by 3,104 lines and strengthening the completeness of the reporting archive for stakeholder review.
* **Established a clean baseline for future reporting changes**: By adding content without deletions in this period (“Add files via upload”), the repository now has a clearer starting point for subsequent comparisons and version-to-version auditing as future bi-weekly/quarterly updates are committed.

## Code Analysis
All recorded activity stems from a single commit (“Add files via upload”) that added 3,104 lines with no deletions. This pattern indicates the period’s work was centered on introducing new files rather than modifying, refactoring, or cleaning up existing content. From a maturity perspective, the absence of deletions and the presence of a single bulk addition suggest the repository is in a content accumulation phase (building out the reporting set) rather than an optimization or maintenance phase.

## Next Steps
Next work for this repository should focus on continuing to add new bi-weekly and quarterly reporting files as they are produced, ideally with more descriptive commit messages (and/or PRs) to make specific reporting-period changes easier to trace and review over time.


# fair-bounty

**GitHub**: [Link](https://github.com/tokamak-network/fair-bounty)


## Overview
fair-bounty appears to implement a report-driven bug bounty workflow for Tokamak Network programs, including submission review, status management, and automated on-chain payout handling. During this period, the repository evolved from an initial architectural draft into an integrated system with an AI-assisted auditor component, administrative reporting tools, and production-oriented security and validation fixes. This work matters to users and stakeholders because it directly impacts how efficiently and safely security reports can be processed and how reliably bounty funds can be escrowed and paid.

## Statistics
| Metric | Value |
|--------|-------|
| Commits | 48 |
| Contributors | 1 |
| Lines Added | +295,378 |
| Lines Deleted | -10,234 |
| Net Change | +285,144 |


## Period Goals
The main goals for this period were to establish an initial end-to-end architecture for a bounty/report platform, implement an AI-assisted auditing flow with robust report status handling, and connect reporting outcomes to on-chain payment execution. In parallel, the work focused on operational readiness: adding comprehensive automated tests, improving deployment/tooling (including Docker sandboxing), migrating target execution to Sepolia with fallback options, and addressing security and validation risks identified during implementation.

## Key Accomplishments
* **Delivered an initial system architecture baseline**: Launched an architectural draft to define the project’s first cohesive structure, enabling subsequent feature work to land on a consistent foundation (“Launched the first architectural draft”).
* **Implemented an AI auditor agent with report status management**: Added an AI auditor component and explicit report status management to support automated/assisted review workflows and clearer tracking of report lifecycle (“feat: add AI auditor agent, report status management, and OpenZeppelin contracts”; “feat: AI auditor on-chain review & auto-pay, synced backend cache layer”).
* **Introduced report-based bounty payment flows with on-chain automation**: Built a report-centric payment mechanism that can preserve ACCEPT reasons and trigger automatic payments on-chain, tightening the linkage between review outcomes and payouts (“feat: report-based bounty payment, preserve ACCEPT reason, auto-pay on chain”; “feat: AI auditor on-chain review & auto-pay, synced backend cache layer”).
* **Strengthened payment reliability and user-facing validation**: Added payment retry handling and hardened validation while also improving user experience elements tied to transaction feedback and warnings (“feat: payment retry, improved UX, and validation hardening”; “refactor(frontend): auto-dismiss tx hash toast and simplify withdrawal warning”).
* **Added administrative reporting UI for operational oversight**: Implemented an admin “All Reports” view with statistics, filters, and expandable detail panels to improve triage, auditing, and operational transparency for program managers (“feat: admin All Reports tab with stats, filters, and expandable detail panels”).
* **Integrated wallet-based authentication and deposit verification**: Added wallet signature authentication and on-chain deposit verification to support stronger identity/authorization controls and ensure deposits are verified against chain state (“feat: add wallet signature authentication and on-chain deposit verification”).
* **Expanded quality assurance with a comprehensive backend test suite**: Added a substantial automated test suite (120 tests) to reduce regression risk and improve confidence in core backend logic as features expanded (“test: add comprehensive backend test suite (120 tests)”).
* **Addressed production security risks and correctness gaps**: Patched multiple security/correctness issues including a false-ACCEPT parsing risk, a SQL duplicate detection gap related to vulnerability type handling, and additional critical vulnerabilities identified as blockers for production readiness (“fix: patch parseVerdict false-ACCEPT risk and SQL duplicate detection vulnType gap”; “fix: patch 3 critical security vulnerabilities for production”).

## Code Analysis
The very large net increase (+285,144) is consistent with building substantial new functionality and scaffolding in a relatively short window. The biggest additions are tied to: (1) establishing the initial codebase structure (“Launched the first architectural draft”), (2) implementing AI auditor capabilities and report status management (“feat: add AI auditor agent, report status management…”; “feat: AI auditor on-chain review & auto-pay…”), and (3) adding on-chain payment logic and associated contracts (“…and OpenZeppelin contracts”; “report-based bounty payment…auto-pay on chain”). Significant added surface area also comes from operational tooling and testing, including a Docker sandbox for forge commands and Foundry tests (“feat: add Docker sandbox for forge commands and ProgramManager Foundry tests”) and a comprehensive backend test suite (“120 tests”).

The deletions (-10,234) align with iterative hardening and maintainability work rather than feature removal. Refactors modularized the auditor into clearer separations (interfaces, implementation, pipeline, pure functions), which typically reduces coupling and makes auditing logic easier to test and modify (“refactor: modularize auditor…”). Additional cleanup included simplifying report filenames to UUID-only and hiding them from the frontend (“refactor: simplify report filename to UUID only…”), narrowing language/localization choices (“refactor: localize auditor to English…”), and repository hygiene through `.gitignore` updates that exclude database files and dependency directories (“chore: update .gitignore…”). Collectively, this blend of rapid feature build-out, focused refactoring, and targeted security patches indicates the project is moving from an initial architecture into an implementation phase where correctness, operational safety, and maintainability are increasingly prioritized (as evidenced by multiple security fixes and the addition of extensive automated tests).

## Next Steps
Next work should continue reducing operational and security risk by extending test coverage and validation around report verdict parsing, duplicate detection, and payment execution paths, building on the fixes already made (“fix: patch parseVerdict…”, “fix: patch 3 critical security vulnerabilities…”). Ongoing iteration is also implied around chain-environment readiness (Sepolia with Anvil fallback) and the AI auditor pipeline as the system is exercised under real program workflows (“feat: migrate target network…to Sepolia with Anvil fallback”; “refactor: modularize auditor…”).


# gunz-ue

**GitHub**: [Link](https://github.com/tokamak-network/gunz-ue)


## Overview
gunz-ue is an Unreal Engine–based project focused on rebuilding core GunZ-style gameplay systems (movement, combat, animation, maps, UI, and networking) with supporting asset and tooling pipelines. For Tokamak Network stakeholders, this repository reflects tangible progress toward a playable prototype and a repeatable content pipeline—both prerequisites for reliable production execution and external testing.

## Statistics
| Metric | Value |
|--------|-------|
| Commits | 87 |
| Contributors | 2 |
| Lines Added | +27,486 |
| Lines Deleted | -10,443 |
| Net Change | +17,043 |


## Period Goals
During this period, the work concentrated on establishing end-to-end foundations for a GunZ-like Unreal project: character/animation pipelines, a first-pass K-style movement component, initial combat state handling, early UI structure, and a minimum viable multiplayer duel flow. In parallel, the team added verification and import scripts plus documentation and a regression harness to stabilize “handfeel” and support repeatable iteration.

## Key Accomplishments
* **Implemented a K-style movement component**: Added directional speed handling along with tumble, wall-run, and wall-jump behaviors to support the project’s core mobility loop and enable early playtesting of movement “handfeel” (commit: *feat(movement): K-style movement component — directional speed/tumble/wall-run/wall-jump*).
* **Built a character gameplay foundation for an OGZ character**: Introduced input handling, animation integration, a combat FSM, weapon swapping, and a demo mode to make the character controllable and showcaseable in-engine (commit: *feat(character): OGZ character — input, animation, combat FSM, weapon swap, demo mode*).
* **Established a Mixamo character mesh pipeline**: Added a pipeline for bringing Mixamo character meshes into the project, supporting faster iteration on rigs/characters and reducing friction in content setup (commit: *feat(character): Mixamo character mesh pipeline*).
* **Validated and refined IK retargeting for GunZ-style weapon grips**: Performed a UE5 retargeting validation spike and then implemented “exact GunZ weapon grips on Manny,” directly targeting animation authenticity and consistent weapon-hand alignment (commits: *feat(retarget): Mannequin spike — GunZ→UE5 IK retargeting validated*; *feat(retarget): exact GunZ weapon grips on Manny*).
* **Adjusted animation behavior back toward GunZ reference**: Reverted sword idle/run/dash behavior to align with GunZ expectations and introduced AnimInstance crossfading, improving motion continuity and helping reduce animation “drift” during rapid state changes (commit: *refactor(anim): revert sword idle/run/dash to GunZ; crossfade AnimInstance*).
* **Added a Phase 0 “handfeel” regression harness with golden trace**: Implemented a test harness that records/compares a golden trace, enabling repeatable checks for movement/combat feel changes and reducing the risk of untracked gameplay regressions (commit: *test(handfeel): add Phase 0 regression harness with golden trace*).
* **Delivered an initial listen-server duel replication MVP**: Implemented a first multiplayer replication milestone (“stage 4”) for a listen-server duel, establishing a baseline for networked play and future iteration on synchronization and gameplay rules (commit: *feat(net): listen-server duel — replication MVP (stage 4)*).
* **Created early frontend structure and UI system**: Added a main menu and lobby skeleton and introduced a “Blur” design system for menu/lobby UI, laying the groundwork for a navigable experience flow beyond in-editor testing (commits: *feat(frontend): main menu and lobby skeleton*; *feat(frontend): Blur design system for menu/lobby*).
* **Replaced debug visuals with procedural billboard combat effects**: Introduced VFX to replace debug drawing, improving readability for playtests and making combat interactions easier to evaluate without developer overlays (commit: *feat(vfx): procedural billboard combat effects replace debug draws*).
* **Expanded playable/editor map coverage and defaults**: Added the Charles Bridge map as the editor default and introduced the Monserrate pilgrimage map, increasing environment variety for testing traversal, combat, and camera/visibility behavior (commits: *feat(map): add Charles Bridge map as editor default*; *feat(maps): add Monserrate pilgrimage map*).
* **Implemented an initial synthesized audio set and import pipeline**: Added a v0 sound set and an import pipeline, enabling consistent audio asset ingestion and supporting faster iteration on feedback cues (commit: *feat(sound): synthesized v0 sound set and import pipeline*).
* **Added asset diagnostics, verification, and import automation**: Delivered scripts for FBX/skeleton/mesh diagnostics and a FBX→UAsset import pipeline plus demo launcher tooling, improving repeatability and reducing manual content setup errors (commits: *chore(scripts): FBX/skeleton/mesh diagnostic and verification scripts*; *chore(scripts): FBX->UAsset import pipeline and demo launcher*).
* **Attempted and then rolled back an Unreal Editor plugin integration**: Added an “MCPUnreal editor plugin” and subsequently reverted it, indicating active evaluation of tooling while keeping the mainline stable when the integration was not ready (commits: *feat(tooling): add MCPUnreal editor plugin*; *revert(tooling): remove MCPUnreal editor plugin*).

## Code Analysis
The +27,486 lines added largely reflect new gameplay and production-capability surface area: a dedicated K-style movement component (directional speed/tumble/wall-run/wall-jump), substantial character gameplay scaffolding (input, animation, combat FSM, weapon swap, demo mode), initial UI flows (menu/lobby skeleton plus a design system), and a first networked duel replication MVP. Significant additions also include content and pipeline support—new maps, a synthesized audio set with import pipeline, and multiple automation/diagnostic scripts for FBX/skeleton/mesh verification and FBX→UAsset imports—indicating an emphasis on repeatable asset ingestion rather than one-off manual setup.

The -10,443 lines deleted are consistent with active iteration and stabilization rather than simple accumulation. The clearest example is the add-and-revert cycle of the MCPUnreal editor plugin (added ~9.7k lines, then removed ~9.7k), which suggests the team tested an integration path and chose to revert to maintain stability. Additional deletions align with refinement work such as animation adjustments and crossfading changes (*refactor(anim): revert sword idle/run/dash to GunZ; crossfade AnimInstance*) and incremental updates in retargeting and UI design system work, reflecting ongoing tuning toward a desired reference feel.

Overall, the net +17,043 lines indicates the repository is in an expansion phase: building core systems (movement, character, network, UI) while simultaneously introducing tooling, tests, and documentation (K-style spec, wall behavior audit, Phase 0 handfeel spec and migration plan) that typically support more disciplined iteration as complexity grows.

## Next Steps
Near-term work implied by the current foundations includes iterating beyond the existing “skeleton”/“MVP” implementations—expanding the menu/lobby flow, advancing the listen-server duel replication beyond the current stage, and continuing to use the Phase 0 regression harness and “handfeel” specifications to guide controlled gameplay tuning.


# hr-automation-process

**GitHub**: [Link](https://github.com/tokamak-network/hr-automation-process)


## Overview
This repository supports internal HR and finance automation processes, covering workflows such as expense settlement, payroll administration, tax deadline tracking, and candidate evaluation utilities. For Tokamak Network, these capabilities matter because they reduce operational overhead, improve auditability of approvals and payouts, and standardize time-sensitive compliance activities (e.g., tax calendars) that affect organizational execution.

## Statistics
| Metric | Value |
|--------|-------|
| Commits | 10 |
| Contributors | 1 |
| Lines Added | +2,924 |
| Lines Deleted | -493 |
| Net Change | +2,431 |


## Period Goals
During this period, the primary focus was to implement persistent, system-integrated expense settlement workflows, including database/API support, approval screens, and automated scheduling. In parallel, the repository expanded adjacent HR operations tooling—tax deadline management with calendar integration, payroll bulk operations, and candidate benchmark evaluation—while tightening security posture around Supabase access.

## Key Accomplishments
* **Implemented persistent expense settlement end-to-end**: Added expense settlement persistence across database and API layers, built an approval UI, and introduced scheduler support to automate parts of the settlement workflow (commit: “feat: 경비 정산 영속화 (§0-§5) — DB/API/승인화면/스케줄러”).
* **Integrated expense settlement with Supabase and approval-to-settlement linkage**: Connected settlement data flows to Supabase, implemented mapping between approval and settlement records, and introduced USDT unit handling to standardize settlement denomination where applicable (commit: “feat: 경비 정산 Supabase 통합 (A-2) — 승인→정산 연계, 매핑, USDT 단위”).
* **Expanded payroll administration tooling**: Implemented bulk payroll deletion and recalculation capabilities to support corrective operations and faster iteration when payroll inputs change (commit: “feat: 급여 벌크 삭제/재계산, Candidates 벤치마크 비교 평가, 발표 자료”).
* **Added candidate benchmark comparison evaluation and quality-metric fixes**: Introduced benchmark comparison evaluation for candidates and subsequently corrected issues by switching benchmark comparison categories to a “quality density” basis and fixing quality metric save/load bugs while increasing AI timeout thresholds (commits: “feat: … Candidates 벤치마크 비교 평가…”, “fix: 벤치마크 비교 카테고리를 품질 밀도 기반으로 교체”, “fix: 벤치마크 품질 메트릭 저장/로드 버그 + AI 타임아웃 증가”).
* **Delivered a tax calendar feature with Google Calendar integration**: Implemented management of Singapore tax deadlines and integrated with Google Calendar to improve visibility and reduce missed compliance dates (commit: “feat: Tax Calendar — 싱가포르 세금 마감일 관리 + Google Calendar 연동”).
* **Standardized exchange-rate sourcing for expense decisions**: Unified the exchange rate source to the ECB API and removed reliance on ECOS USD/KRW, improving consistency in FX-dependent expense decisioning (commit: “fix: 경비 결정 환율을 ECB API로 통일 (ECOS USD/KRW 제거)”).
* **Hardened Supabase security configuration**: Removed hardcoded Supabase keys and enabled Row Level Security (RLS) across all tables, reducing exposure risk and aligning data access with least-privilege principles (commit: “security: Supabase 키 하드코딩 제거 + RLS 전테이블 활성화”).
* **Maintained stakeholder documentation and presentation assets**: Updated presentation materials to include benchmark comparison evaluation content, adjusted dates, and standardized styling for consistency (commits: “docs: 발표 자료에 벤치마크 비교 평가 내용 추가”, “docs: 발표 자료 날짜 6/10으로 변경 + 배경색 5/20 스타일 통일”).

## Code Analysis
The net increase of **+2,431 lines** reflects substantial feature delivery rather than small incremental changes, driven primarily by the expense settlement persistence work that explicitly spans **DB/API/approval UI/scheduler** components and represents the single largest addition in the period (commit: “경비 정산 영속화…”). Additional material code growth came from Supabase integration for settlement flows (approval→settlement linkage, mapping, and USDT unit handling) and the tax calendar implementation with Google Calendar integration, each indicating expansion of operational tooling into connected services (commits: “경비 정산 Supabase 통합…”, “Tax Calendar…”).

The **-493 lines deleted** aligns with targeted cleanup and standardization: removal of ECOS USD/KRW usage when consolidating FX sourcing to the ECB API and refactoring/security remediation associated with eliminating hardcoded Supabase keys (commits: “경비 결정 환율… 제거”, “Supabase 키 하드코딩 제거…”). The presence of multiple “fix” commits—addressing benchmark evaluation categorization, quality metric persistence, and timeout configuration—suggests the repository is moving from initial feature rollout into stabilization and correctness hardening, particularly for evaluation workflows and integrated services.

## Next Steps
Continue iterating on the newly implemented expense settlement and payroll operational flows by refining integration points (Supabase, scheduling) and addressing follow-on fixes as usage surfaces edge cases. Maintain security and compliance alignment by extending the current Supabase hardening approach (RLS-enabled tables, non-hardcoded secrets) as new tables and features are added.


# rivai

**GitHub**: [Link](https://github.com/tokamak-network/rivai)


## Overview
rivai is a game-focused codebase that, in this period, evolved into a monorepo incorporating platform-specific work (notably macOS) alongside core gameplay, content, and launcher functionality. The repository matters to stakeholders because it covers the end-to-end player experience—launcher access, authentication handoff, gameplay systems, and stability fixes—which collectively determine usability, testability, and readiness for broader distribution.

## Statistics
| Metric | Value |
|--------|-------|
| Commits | 13 |
| Contributors | 1 |
| Lines Added | +20,892 |
| Lines Deleted | -247 |
| Net Change | +20,645 |


## Period Goals
The primary goal for this period appears to have been consolidating previously separate project work into a unified monorepo while expanding player-facing functionality across authentication, launcher UX, and content. In parallel, the team iterated on gameplay systems (combat authority separation), added new maps/character assets/animations, and addressed stability and test coverage (audio GC crash prevention and network verification tests).

## Key Accomplishments
* **Consolidated macOS project work into the main monorepo**: Absorbed the standalone “gunz-mac” project into the repository, reducing fragmentation and simplifying cross-platform development and release management (*feat(gunz-mac): absorb standalone gunz-mac project into monorepo*).
* **Implemented account and login capabilities**: Added an account API and launcher login flow, establishing a foundation for controlled access, user sessions, and integration with the launcher experience (*feat(auth): account API and launcher login*).
* **Enabled initial launcher-to-game authentication handoff**: Passed a development launch ticket to the game via the `OGZ_AUTH_TOKEN` environment variable (“stage 0”), which supports early end-to-end validation of authenticated launches (*feat(launcher): pass dev launch ticket to game via OGZ_AUTH_TOKEN env (stage 0)*).
* **Improved launcher UI and branding behaviors**: Added frameless, “LoL-style” window controls and updated launcher visuals (yellow accent, brand logo, hero video) tied to version 0.0.9, improving usability and presenting a more cohesive entry point for users (*feat(launcher): frameless LoL-style window controls*; *feat(launcher): yellow accent, brand logo, new hero video (0.0.9)*).
* **Expanded playable content with new character and map assets**: Added a “cybernetic combat suit” mesh and introduced a Dotonbori map with a procedural builder, increasing available content for gameplay testing and demonstrations (*feat(character): cybernetic combat suit mesh*; *feat(maps): Dotonbori map with procedural builder*).
* **Advanced movement/combat feel via animation work—and iterated on transition approach**: Added outsourced sword dash animations with pose-aligned playback and attempted “seamless idle<->dash transitions,” then reverted that specific transition approach, indicating active tuning for responsiveness and visual continuity (*feat(anim): outsourced sword dash animations with pose-aligned playback*; *fix(anim): seamless idle<->dash transitions via windup catch-up*; *Revert "fix(anim): seamless idle<->dash transitions via windup catch-up"*).
* **Refined combat architecture for clearer authority boundaries**: Split “shot authority” from cosmetic handling, which supports more maintainable combat code and can reduce ambiguity between gameplay-critical decisions and presentation (*refactor(combat): split shot authority from cosmetics*).
* **Improved reliability through targeted test and crash fixes**: Added a network test for rotating-screenshot duel verification and fixed an audio crash by marking `SoundMap` as `UPROPERTY` to prevent garbage-collection use-after-free, reducing runtime instability during play and test sessions (*test(net): -OGZNetShot rotating-screenshot duel verification*; *fix(audio): mark SoundMap UPROPERTY to prevent GC use-after-free crash*).

## Code Analysis
The +20,892 lines added are dominated by repository consolidation and feature expansion. The largest single change—absorbing the standalone “gunz-mac” project into the monorepo (+17,657)—suggests substantial code and/or build/system integration work landed in one step (*feat(gunz-mac): absorb standalone gunz-mac project into monorepo*). Additional sizable additions align with building product surface area: authentication/account API and launcher login (+1,102) (*feat(auth): account API and launcher login*), new character content (+873) (*feat(character): cybernetic combat suit mesh*), new animations (+494) (*feat(anim): outsourced sword dash animations with pose-aligned playback*), and a new map with a procedural builder (+358) (*feat(maps): Dotonbori map with procedural builder*).

The -247 lines deleted are consistent with iterative engineering rather than broad cleanup. Notably, a combat refactor removed and reorganized code while adding new structure (+140/-50), indicating an effort to separate core gameplay authority from cosmetics for clearer responsibilities (*refactor(combat): split shot authority from cosmetics*). The animation transition change was introduced and then reverted (+97/-16 followed by +16/-97), signaling rapid experimentation and rollback when a specific approach did not meet requirements, which is typical during feel/performance tuning (*fix(anim)...* and its *Revert*). Small, surgical fixes and tests (audio GC prevention, network verification test) indicate attention to stability and validation as feature work progresses (*fix(audio)...*; *test(net)...*).

Overall, the net change (+20,645) indicates a period primarily focused on bringing significant code into a single repository and extending user-critical pathways (launcher, login, authenticated launch), with early signs of maturing discipline through targeted refactors, tests, and crash fixes.

## Next Steps
Continue building out the authenticated launcher-to-game flow beyond the current “stage 0” ticket handoff and further stabilize gameplay feel, particularly around dash/idle transition behavior that was recently experimented with and reverted. Ongoing work is also likely to deepen content and systems added this period (map tooling, character assets, combat separation) while expanding validation through additional tests and runtime stability fixes.


# scatter-dex

**GitHub**: [Link](https://github.com/tokamak-network/scatter-dex)


## Overview
scatter-dex is a codebase supporting Scatter’s decentralized exchange and associated operator/admin tooling, including an orderbook backend, relayer/operator registry workflows, and a user-facing SDK used by related applications. During this period, the repository advanced multi-network readiness, strengthened operator/KYC and certificate authority flows, and improved reliability of note/claim UX—areas that directly affect operational integrity, compliance workflows, and end-user transaction outcomes.

## Statistics
| Metric | Value |
|--------|-------|
| Commits | 331 |
| Contributors | 1 |
| Lines Added | +31,847 |
| Lines Deleted | -14,608 |
| Net Change | +17,239 |


## Period Goals
Work in this period focused on shipping operational primitives required for a production-grade exchange environment: operator onboarding (KYC + certificates), admin controls for treasury/revenue handling, and backend indexers/endpoints needed for observability and settlement history. In parallel, the team aimed to reduce duplication across admin/operator surfaces and improve SDK/client reliability for note synchronization and gasless claim flows (as reflected in multiple bug-fix PRs).

## Key Accomplishments
* **Implemented operator leaf-certificate issuance end-to-end**: Added backend support for issuing operator leaf certificates with CSR intake and signing records (*feat(orderbook): operator leaf-cert issuance backend (CSR + signing record)*), provided an operator self-service UI for certificate issuance (*feat(operators): self-service operator certificate issuance screen*), and enabled admin-side CSR signing with authoritative subject gating (*feat(admin): CA signs operator CSR → leaf cert with authoritative subject gate*), establishing a clearer operational control path for operator identity credentials.
* **Structured certificate authority hierarchy and tightened CA configuration**: Introduced “Root CA under Operator CA” as part of KYC review workflows (*feat(admin): KYC review + Root CA under Operator CA (PR2-B)*) and removed a self-issued certificate line from operator CA configuration (*refactor(operator-ca): remove self-issued cert line; identity = zk-X509 + KYC*), reducing ambiguity in issuance paths and aligning CA handling with intended identity requirements.
* **Delivered initial KYC onboarding backend for relayer operators**: Added Stage 1 backend support for relayer operator KYC onboarding (*feat(orderbook): add relayer operator KYC onboarding backend (Stage 1)*), extending administrative and compliance-related workflows needed to onboard and manage market infrastructure participants.
* **Added SIWE-based authentication for admin/KYC endpoints and centralized shared auth logic**: Implemented SIWE wallet-signature authentication to protect admin/KYC endpoints (*feat(orderbook): SIWE wallet-signature auth for admin/KYC endpoints*) and refactored shared SIWE admin-auth core into a shared package (*refactor(auth): hoist shared SIWE admin-auth core into @scatter-dex/types*), improving consistency across services and reducing duplicated authentication logic.
* **Expanded orderbook transparency via commitment history indexing and API access**: Implemented a commitment-history indexer and exposed it through a dedicated API endpoint (*feat(orderbook): commitment-history indexer + GET /api/commitments*), enabling programmatic access to operational history that supports monitoring, debugging, and audits.
* **Advanced admin treasury and token control features**: Added treasury revenue split, treasury withdrawals, and a token whitelist list in the admin surface (*feat(admin): treasury revenue split + Treasury withdraw + token whitelist list*), improving operational control over funds movement and approved assets.
* **Shifted token metadata and address resolution to on-chain sources**: Updated frontend SDK behavior to source token lists from an on-chain whitelist (*feat(sdk/frontend): source token list from on-chain whitelist*) and aligned pay/pro flows to resolve token addresses and decimals from the same on-chain whitelist (*feat(pay,pro): resolve token addresses+decimals from on-chain whitelist*), reducing reliance on static/off-chain token configuration.
* **Strengthened SDK execution model using wallet-node reads/writes with Multicall batching**: Enabled SDK reads and writes to run on the user’s wallet node and batch via Multicall3 (*feat(sdk): run reads & writes on the user's wallet node, batched via Multicall3*), improving request efficiency and consolidating on-chain operations into fewer calls where applicable.
* **Improved multi-network readiness and deployment governance**: Added backend multi-network (chainId) support (*feat(orderbook): multi-network (chainId) support — backend*), parameterized launch scripts for Sepolia team setup (*feat(scripts): network-parameterized launch scripts for Sepolia team setup*), and updated deployment architecture to use a single shared ProxyAdmin plus a full deployment ledger (*feat(deploy): single shared ProxyAdmin for all proxies + full deployment ledger*), increasing repeatability and traceability of deployments across environments.
* **Made relayer registry configuration more flexible**: Introduced an admin-configurable, global, switchable bond token in the relayer registry (*feat(relayer-registry): admin-configurable bond token (global, switchable)*), enabling operational changes to collateral/bond parameters without code duplication across networks.
* **Reduced repository bloat and removed duplicated UI surfaces**: Deleted operator “platform-admin” pages duplicated by the admin app (*chore(operators): remove platform-admin pages duplicated by the admin app*), simplifying maintenance and minimizing the risk of divergent behaviors across two admin interfaces.
* **Improved reliability of note synchronization and gasless claim UX across apps**: Landed multiple fixes affecting note reconciliation and claim handling, including bounding a self-heal poll to prevent infinite polling (*PR#1023*), self-healing pending notes by polling tree refresh until reconciled (*PR#1017*), and addressing false timeout failures and nullifier backstops on gasless claim surfaces (*PR#1019, PR#1021*), improving end-user consistency for claims and reducing support/debug overhead.

## Code Analysis
The +31,847 / -14,608 change profile reflects substantial feature delivery alongside targeted cleanup and consolidation. Major additions correspond to new operational and administrative capabilities: certificate issuance workflows (operator CSR handling, signing records, self-service issuance UI, and admin signing with subject gating) (*feat(orderbook): operator leaf-cert issuance backend (CSR + signing record)*; *feat(operators): self-service operator certificate issuance screen*; *feat(admin): CA signs operator CSR → leaf cert with authoritative subject gate*), treasury controls and token whitelist management (*feat(admin): treasury revenue split + Treasury withdraw + token whitelist list*), commitment history indexing and an API endpoint (*feat(orderbook): commitment-history indexer + GET /api/commitments*), and multi-network backend support plus deployment/launch improvements (*feat(orderbook): multi-network (chainId) support — backend*; *feat(deploy): single shared ProxyAdmin for all proxies + full deployment ledger*; *feat(scripts): network-parameterized launch scripts for Sepolia team setup*).

Significant deletions indicate deliberate reduction of duplication and tighter configuration: removal of duplicated “platform-admin” pages (*chore(operators): remove platform-admin pages duplicated by the admin app*) and cleanup of operator CA configuration (*refactor(operator-ca): remove self-issued cert line; identity = zk-X509 + KYC*). Large-scale documentation changes (*docs(circuit-split): rewrite design.md to match the shipped Half-proof implementation*) suggest alignment of written design with shipped behavior, which is typical as systems stabilize. Separately, moving canonical prover zkeys distribution to a GCS manifest rather than Git (*feat(zk-assets): distribute canonical prover zkeys via GCS manifest, not git*) indicates the codebase is shedding large binary artifacts and shifting toward more maintainable release/asset distribution practices.

Overall, the pattern—new admin/operator infrastructure, security/auth consolidation, multi-network/deployment rigor, and reliability bug-fixes through PRs—suggests the repository is transitioning from feature build-out toward operational hardening and maintainability, with deliberate removal of redundant surfaces and clearer ownership of critical workflows (auth, CA, treasury, and on-chain configuration sources).

## Next Steps
Continue iterating on operator onboarding and KYC workflows beyond the current “Stage 1” backend work (*feat(orderbook): add relayer operator KYC onboarding backend (Stage 1)*) and further harden client reliability paths around note reconciliation and gasless claim handling as surfaced by the recent fix PRs (PR#1017–PR#1023).


# Tokagentos-monorepo

**GitHub**: [Link](https://github.com/tokamak-network/Tokagentos-monorepo)


## Overview
Tokagentos-monorepo is a monorepo that aggregates Tokagentos application packages and operator-facing tooling, including an “operator console” and billing-related surfaces. During this period, work concentrated on making on-chain credit/billing flows and gateway pages functional against live data, while improving multi-chain support and stabilizing builds—areas that directly affect user onboarding, payment reliability, and operational visibility.

## Statistics
| Metric | Value |
|--------|-------|
| Commits | 57 |
| Contributors | 1 |
| Lines Added | +38,209 |
| Lines Deleted | -8,290 |
| Net Change | +29,919 |


## Period Goals
The primary objective was to deliver a redesigned operator console centered on “x402” billing/credits functionality, with self-contained, inline on-chain flows (top-up, bridging, swapping) and reliable live-data wiring across gateway pages. A second goal was to extend billing to be chain-aware and multi-chain (including specific bridge routes) while ensuring the monorepo builds cleanly and documentation is easier for new contributors.

## Key Accomplishments
* **Implemented inline, self-contained x402 on-chain flows**: Added on-chain sequences for “get-PTON, bridge, swap” as part of the operator x402 experience, enabling a more direct path from credits UI to actual on-chain actions (**feat(operator): x402 on-chain flows — get-PTON, bridge, swap (inline, self-contained)**).
* **Ported the redesigned operator console into scaffolded applications**: Moved the x402 redesign and operator console into scaffolded apps to standardize delivery and reduce duplication across app targets (**feat(scaffold): port operator console (x402 redesign) into scaffolded apps**).
* **Restructured the x402 tab into a real-data billing surface**: Reworked the x402 UI to be inline and tied to real billing data rather than a separate/isolated surface, improving accuracy and reducing context switching for operators (**feat(operator): restructure x402 tab into inline real-data billing surface**).
* **Added a consolidated operator console spanning credits and network visibility**: Introduced an operator console that covers x402 credits and “A2A network” visibility, expanding the administrative surface area for monitoring and management (**feat(app-core): add operator console (x402 credits + A2A network)**).
* **Enabled chain-aware, per-chain billing and settlement behaviors**: Delivered chain-aware credits, a credit-level bridge, a global network switcher, and per-chain billing so spend/settlement can occur on the selected network—supporting multi-network operations without a single-chain assumption (**feat(tokagentos@2.0.64): chain-aware credits + credit-level bridge + global network switcher**, **feat(tokagentos@2.0.69): per-chain billing — spend & settle on the selected network**).
* **Expanded top-up and bridging options across networks**: Added multi-chain PTON top-up support for Ethereum and Base, and implemented a canonical TON bridge on Base (Route A) using the OP Standard Bridge for “real TON” bridging pathways (**feat(billing): multi-chain PTON top-up — Ethereum + Base**, **feat(tokagentos@2.0.65): canonical TON bridge on Base (Route A) — real TON via OP Standard Bridge**).
* **Integrated a native top-up mechanism using EIP-3009**: Implemented native EIP-3009 top-up and removed a specific BillingPageView “borrow” dependency, simplifying the billing UI’s internal coupling while enabling a standardized authorization pattern for value transfer (**feat(operator): native EIP-3009 top-up — sever the BillingPageView borrow**).
* **Completed key x402 operational UI elements for usage and credential management**: Finalized x402 page functionality including API-key reveal and usage tables with reserved/accrued tracking, improving transparency and auditability for billing operations (**feat(operator): finish x402 page — api-key reveal, usage tables, reserved/accrued**).
* **Added SIWE-based sign-in to support authenticated deposit/read widgets**: Implemented SIWE sign-in with bearer authentication to ensure deposit and read widgets function under authenticated contexts, improving operational security and reliability of billing widgets (**feat(operator): SIWE sign-in (bearer auth) so the deposit + read widgets work**).
* **Wired gateway pages and chat to live data with streaming behavior**: Connected “full gateway” pages (Chat/Wallet/Automations/Plugins/Settings) to live data and updated chat to stream and use real data like the global chat, reducing discrepancies between UI and backend state (**feat(operator): wire full gateway (Chat/Wallet/Automations/Plugins/Settings) to live data**, **feat(operator): chat tab streams + uses real data like the global chat**).
* **Introduced user-selectable LLM model controls tied to billing UX**: Added the ability for users to select an LLM model from the billing page and improved chat UI to display the active model per agent turn, aligning cost/billing awareness with model usage behavior (**feat(tokagentos@2.0.72): user-selectable LLM model from the billing page**, **feat(operator): right-align user chat bubbles + show active model per agent turn**).
* **Stabilized monorepo build and improved contributor onboarding documentation**: Achieved a fully green monorepo build via turbo (15/15 packages) and repaired the @tokagentos/agent build (including renaming and dependency/stub adjustments), while simplifying the root README for first-time contributors (**fix(build): complete monorepo build (turbo run build now 15/15 green)**, **fix(build): repair @tokagentos/agent build (Eliza→Tokagent rename, telegram stubs, viem)**, **docs(readme): simplify root README for first-time contributors**).

## Code Analysis
The +38,209 lines added largely reflect substantial new UI and application-surface implementation around the operator console and x402 billing workflows, including self-contained on-chain flows (get-PTON/bridge/swap) and fully-featured billing pages with API-key reveal and usage accounting (**feat(operator): x402 on-chain flows — get-PTON, bridge, swap**, **feat(operator): finish x402 page — api-key reveal, usage tables, reserved/accrued**). Significant additions also came from porting and mirroring the operator console into scaffolded apps and making gateway pages self-contained, which typically involves duplicating/standardizing page composition and data wiring across multiple app entry points (**feat(scaffold): port operator console (x402 redesign) into scaffolded apps**, **refactor(operator): make full-gateway pages self-contained + mirror to scaffold**).

The -8,290 lines deleted indicate meaningful restructuring and cleanup alongside feature delivery. The x402 tab was explicitly “restructured,” and the full-gateway pages were refactored to be self-contained, which commonly results in removal of older, coupled implementations in favor of consolidated components (**feat(operator): restructure x402 tab into inline real-data billing surface**, **refactor(operator): make full-gateway pages self-contained + mirror to scaffold**). Additional deletions are consistent with the simplified root README and build repairs that likely removed obsolete configuration or legacy references (e.g., renaming and stub updates) (**docs(readme): simplify root README for first-time contributors**, **fix(build): repair @tokagentos/agent build**).

Overall, the pattern—large feature additions paired with targeted refactors and build stabilization—suggests the repository is moving from prototype-like surfaces toward operational readiness: live-data wiring, authenticated flows (SIWE), multi-chain billing/top-ups, and repeatable builds provide a foundation for predictable releases and lower integration risk (**feat(operator): SIWE sign-in...**, **feat(tokagentos@2.0.64)...**, **fix(build): complete monorepo build...**).

## Next Steps
Continue iterating on the operator console and x402 billing surface to further consolidate self-contained gateway pages and scaffold parity, building on the recent refactors and ports (**refactor(operator): make full-gateway pages self-contained + mirror to scaffold**, **feat(scaffold): port operator console (x402 redesign) into scaffolded apps**). Further enhancements are also implied around multi-chain billing and on-chain credit flows, extending the current Ethereum/Base and bridge-route work (**feat(billing): multi-chain PTON top-up — Ethereum + Base**, **feat(tokagentos@2.0.69): per-chain billing — spend & settle on the selected network**).


# tokamak-ai-access

**GitHub**: [Link](https://github.com/tokamak-network/tokamak-ai-access)


## Overview
tokamak-ai-access appears to focus on access control and key management mechanisms for applications interacting with Tokamak services, with an emphasis on Ethereum-based authentication patterns. During this period, development centered on enabling delegated key issuance using SIWE (Sign-In With Ethereum), a capability relevant for partner application onboarding and controlled access provisioning. This matters to users and investors because delegated issuance can reduce friction for integrations while maintaining clearer authorization boundaries between Tokamak systems and third-party apps.

## Statistics
| Metric | Value |
|--------|-------|
| Commits | 1 |
| Contributors | 1 |
| Lines Added | +182 |
| Lines Deleted | -0 |
| Net Change | +182 |


## Period Goals
The primary objective for this reporting period was to add delegated SIWE key issuance functionality intended for partner applications. With only one feature-focused commit, the period’s scope appears concentrated on introducing the initial implementation needed to support that delegated issuance flow.

## Key Accomplishments
* **Implemented delegated SIWE key issuance for partner apps**: Added functionality to issue SIWE-associated keys via a delegated mechanism (“feat(keys): delegated SIWE key issuance for partner apps”), supporting partner application access provisioning without requiring the same direct issuance path as first-party applications.
* **Expanded key-management capabilities to support partner integration requirements**: Introduced new code required for partner-oriented issuance flows (same commit), which can enable clearer separation of responsibilities between Tokamak-operated components and external application issuers/consumers.

## Code Analysis
The net change of **+182 lines** with **no deletions** indicates a straightforward feature addition rather than refactoring or optimization. The added code corresponds to the new capability described in the commit—**delegated SIWE key issuance for partner apps**—suggesting new logic and/or supporting structures were introduced to enable delegated issuance. The absence of removed code implies the repository is in an additive stage for this area of functionality, with the period focused on introducing baseline capabilities rather than iterating on or consolidating existing implementations.

## Next Steps
Next steps are likely to focus on validating the delegated SIWE key issuance flow in real partner integrations and adding supporting test coverage and documentation to operationalize the feature for broader use.


# tokamak-landing-page

**GitHub**: [Link](https://github.com/tokamak-network/tokamak-landing-page)


## Overview
This repository contains the main Tokamak Network public website, serving as the primary entry point for users seeking ecosystem information and key product narratives. As the first-touch surface for many users, changes here directly affect discoverability (SEO), perceived product clarity, and web performance—factors that influence acquisition and stakeholder confidence.

## Statistics
| Metric | Value |
|--------|-------|
| Commits | 6 |
| Contributors | 1 |
| Lines Added | +152 |
| Lines Deleted | -29 |
| Net Change | +123 |


## Period Goals
This period focused on synchronizing a broader landing-page overhaul from development to production, covering SEO/AI discovery improvements, subpage work, performance tuning, and cleanup of legacy elements (PR#26). In parallel, the team aimed to improve media behavior on the homepage (correct playback and better mobile loading) and update site messaging/metadata assets to align with current positioning.

## Key Accomplishments
* **Merged a consolidated landing overhaul into main**: Synced development work to production to deliver a packaged set of updates spanning landing changes, SEO/AI discovery, subpages, performance work, and legacy cleanup (PR#26), reducing drift between branches and enabling stakeholders to reference a single canonical site state.
* **Corrected showcase video playback behavior**: Adjusted showcase clips to play to full length instead of auto-skipping (commit: “fix: play showcase clips to full length instead of auto-skipping”), improving content comprehension and preventing users from missing key segments of the on-page product narrative.
* **Improved mobile loading performance for hero media**: Deferred loading/playing the hero clip on mobile until after first paint (commit: “perf: defer hero clip on mobile until after first paint”), reducing render-blocking behavior and improving perceived load responsiveness on constrained devices.
* **Updated public-facing metadata, messaging, and robustness**: Updated the Open Graph image and rewrote the home description around “privacy-focused custom L2” messaging (commits: “chore: update OG image…”, “chore: rewrite home description…”), refreshed a showcase video cut (commit: “chore: update Tonnel showcase video…”), and added a guard against an undefined FX rate in `/api/price/candles` (commit: “fix: guard against undefined FX rate…”), improving share-preview consistency and reducing the chance of runtime errors in the pricing API endpoint.

## Code Analysis
The net +123 lines reflect targeted additions primarily in two areas: (1) homepage/media logic and performance controls, and (2) small reliability and content/metadata updates. The largest functional change was the adjustment to video playback so showcase clips run to completion (+87/-16), indicating code changes around clip timing or playback control rather than simple content edits. Performance-oriented additions for mobile hero behavior (+36/-3) suggest new conditional loading or deferred execution paths designed to improve first paint.

The -29 lines deleted are consistent with small cleanups and replacing prior behavior (e.g., removing earlier playback/auto-skip logic and minor adjustments accompanying OG/home copy updates). Combined with the merged “legacy cleanup” noted in PR#26, the overall change pattern indicates incremental maturation: tightening user-visible behavior (media), improving performance characteristics (mobile first paint), and reducing edge-case failures (undefined FX rate) while keeping scope controlled.

## Next Steps
Continue iterative refinement of the landing overhaul introduced in PR#26 by monitoring real-user performance on mobile media and adjusting loading thresholds as needed. Maintain alignment between public messaging assets (OG images, homepage copy, showcase videos) and ongoing ecosystem updates, while extending defensive checks for API routes similar to the `/api/price/candles` fix.

---


# tokamak-network-gitbook

**GitHub**: [Link](https://github.com/tokamak-network/tokamak-network-gitbook)


## Overview
This repository maintains Tokamak Network’s GitBook-based documentation, covering user- and developer-facing guides across core topics such as staking, DAO information, rollup hub references, and testnet details. Accurate, navigable documentation reduces onboarding friction, lowers support burden, and improves trust by ensuring stakeholders can verify processes (e.g., withdrawals, staking access) against current network behavior.

## Statistics
| Metric | Value |
|--------|-------|
| Commits | 11 |
| Contributors | 1 |
| Lines Added | +1,885 |
| Lines Deleted | -283 |
| Net Change | +1,602 |


## Period Goals
During this period, work focused on expanding and correcting documentation content, including migrating previously dead links into GitBook pages and bringing key guides (staking, DAO/info, Rollup Hub) up to date. A second emphasis was improving discoverability and usability through SEO meta descriptions, link hygiene, and language consistency between English and Korean documentation.

## Key Accomplishments
* **Migrated dead Notion content into GitBook pages for TRH documentation**: Replaced unavailable Notion references by porting TRH SDK/Platform content into GitBook pages, improving long-term accessibility and reducing the risk of user drop-off due to dead external links (docs: migrate dead Notion links into GitBook pages (TRH SDK/Platform); docs: fix review findings in migrated TRH guides).
* **Updated staking documentation to reflect current access paths and tooling references**: Revised staking docs to account for Etherscan-related guidance and “community edition access,” aligning instructions with the current user flow and reducing confusion during staking and verification (docs: update staking docs for Etherscan & community edition access; docs(ko): port PR #1 staking rewrite + info/DAO link fixes + testnet chain ID).
* **Improved cross-language consistency and navigation for Korean documentation**: Ported a staking rewrite into Korean, corrected info/DAO link targets, and replaced a stale Korean Rollup Hub stub with navigation that points to the English Rollup Hub content, reducing divergence between locales and preventing users from relying on outdated pages (docs(ko): port PR #1 staking rewrite + info/DAO link fixes + testnet chain ID; docs(ko): replace stale rollup-hub stub with English-link nav to Tokamak Rollup Hub).
* **Expanded SEO metadata coverage across documentation pages**: Added SEO meta descriptions to key entry pages and then extended those descriptions to remaining pages, increasing clarity in search results and improving content discoverability for new users and developers (docs: add SEO meta descriptions to key entry pages; docs: expand SEO descriptions to remaining pages + fix withdrawal eligibility wording).
* **Corrected withdrawal eligibility wording to match intended semantics**: Refined language around withdrawal eligibility—specifically clarifying the “at or below current block” condition—reducing the likelihood of misinterpretation in user operational steps (docs: expand SEO descriptions to remaining pages + fix withdrawal eligibility wording; docs: fix withdrawal eligibility wording (at or below current block); docs(ko): fix withdrawal eligibility wording per review).
* **Fixed broken links and stale references across core informational areas**: Addressed link rot and outdated references in DAO/staking/info pages, improving navigation integrity and lowering support overhead caused by users encountering dead ends (docs: fix broken links and stale references in DAO/staking/info pages).
* **Refreshed Thanos Sepolia testnet reference details**: Updated testnet documentation to reflect current chain ID and L1 contract details and noted Chainlist status, helping developers avoid configuration errors when connecting tools and deploying/testing (docs: update Thanos Sepolia testnet info (chain ID, L1 contracts, Chainlist status)).

## Code Analysis
The net addition of **+1,602 lines** primarily reflects substantive documentation growth rather than code changes, driven by content migrations and expanded guides. The largest increase came from migrating dead Notion links into first-party GitBook pages for TRH SDK/Platform documentation (**+763/-18**), indicating a deliberate move toward consolidating critical knowledge into a maintained documentation system; follow-up edits addressed review findings in the migrated TRH guides (**+6/-10**), suggesting iteration and quality control after the migration.

Additional large additions were associated with staking documentation updates in both English and Korean (**+376/-10** and **+376/-25**), consistent with a broader effort to keep operational user guidance aligned with current access pathways (including Etherscan and “community edition access”). The deletion volume (**-283**) is notably influenced by removing a stale Korean Rollup Hub stub (**+15/-206**), which indicates cleanup of outdated or redundant content rather than loss of functional documentation; this is complemented by smaller link-fix commits that removed/adjusted incorrect references without large net changes.

The SEO-focused commits (**+136/-0** and **+200/-1**) show structured improvements to metadata coverage across documentation pages, suggesting increasing maturity in how documentation is managed—not only for correctness but also for discoverability and maintainability. Overall, the pattern of migrations, cleanup of stale pages, and precision edits to eligibility wording indicates the repository is being managed as a living operational resource where accuracy and navigability are treated as ongoing maintenance concerns.

## Next Steps
Continue replacing or consolidating remaining legacy/stale documentation fragments to reduce reliance on external sources and minimize duplication across languages. Further incremental reviews are likely needed to keep staking, testnet, and TRH-related pages aligned with evolving network parameters and to prevent link and terminology drift over time.


# tokamak-thanos

**GitHub**: [Link](https://github.com/tokamak-network/tokamak-thanos)


## Overview
tokamak-thanos is Tokamak Network’s optimistic rollup stack implementation intended to support Ethereum scaling by enabling off-chain execution with on-chain security guarantees. As a rollup stack, it is a core infrastructure component that can affect throughput, transaction costs, and the operational tooling available to rollup operators and application teams. For users and investors, progress in this repository is relevant because it can translate into improved scalability characteristics and a clearer path to production deployment and maintenance of rollup-based services.

## Statistics
| Metric | Value |
|--------|-------|
| Commits | 0 |
| Contributors | 0 |
| Lines Added | +0 |
| Lines Deleted | -0 |
| Net Change | +0 |


## Period Goals
No commit activity or merged PRs were recorded for this reporting period, so specific engineering goals cannot be substantiated from repository change history. The absence of changes suggests the period did not include tracked implementation, refactoring, or documentation updates within this repository.

## Key Accomplishments
No accomplishments can be evidenced for this period because there were no commits or merged PRs recorded.

## Code Analysis
With **+0 lines added** and **-0 lines deleted**, there is no code-level signal in this period indicating new features, optimizations, refactors, or maintenance work landed in the repository. From a maturity and delivery perspective, this period should be interpreted as **no measurable repository evolution** (no incremental implementation progress, no visible cleanup, and no documented changes) rather than as a positive or negative change in quality.

## Next Steps
To re-establish measurable progress, the next period should include repository-tracked updates (commits and/or PRs) that clearly document implemented changes and their rationale. Stakeholders should rely on future commit/PR history in this repository to confirm scope, delivery cadence, and technical direction.

---


# toki

**GitHub**: [Link](https://github.com/tokamak-network/toki)


## Overview
`toki` is a Tokamak Network repository that, during this period, focused on integrating an extension codebase into the main repository and expanding an “hub” application experience, including login-home functionality, an ecosystem mini-hub, and workspace-oriented features. It matters because these changes consolidate development into a single codebase and add user-facing flows that can reduce friction in onboarding and improve navigation across applications and services.

## Statistics
| Metric | Value |
|--------|-------|
| Commits | 7 |
| Contributors | 1 |
| Lines Added | +18,294 |
| Lines Deleted | -185 |
| Net Change | +18,109 |


## Period Goals
This period prioritized consolidating code by integrating `toki-extension` into the main repository and shipping multiple hub-oriented UI/UX upgrades (login-home hub, app launcher, ecosystem mini-hub, and additional dashboard experiences). A secondary goal was to improve reliability of user progression through onboarding and to add infrastructure capabilities for deterministic paymaster deployment, alongside targeted documentation updates for private-transfer verification and handoff.

## Key Accomplishments
* **Integrated extension code into the main repository**: Consolidated `toki-extension` into the primary repo to reduce fragmentation and simplify ongoing development and maintenance efforts (*chore: integrate toki-extension into main repo*).
* **Expanded hub functionality with ecosystem and workspace capabilities**: Added an “ecosystem mini-hub” and introduced “native AI Access issuance” plus an “Agent Workspace,” increasing the hub’s scope beyond a dashboard into a broader feature surface for users (*feat(hub): ecosystem mini-hub + native AI Access issuance & Agent Workspace*).
* **Reworked the hub entry experience into a login-home and app launcher**: Converted the dashboard into a login-home hub and added an app-launcher flow (track A), improving how users discover and access applications from a central entry point (*feat(hub): turn dashboard into login-home hub + app launcher (track A)*).
* **Added a gacha-lobby dashboard with image-card menu collage**: Implemented an additional dashboard experience with an image-card based menu collage, broadening UI options for navigation and engagement within the hub surface (*feat(hub): gacha-lobby dashboard with image-card MENU collage*).
* **Hardened onboarding progression for resumed users**: Made onboarding completion “durable” so returning/resumed users reliably reach staking, reducing drop-off and support burden caused by inconsistent state or incomplete handoffs (*fix: make onboarding completion durable so resumed users reach staking*; PR#15).

## Code Analysis
The net change of **+18,109 lines** is primarily explained by large feature integration and new hub capabilities rather than small incremental tweaks. The dominant addition is the consolidation work to integrate `toki-extension` into the main repository (*chore: integrate toki-extension into main repo*), which accounts for the bulk of new code and indicates a structural shift toward a unified codebase.

A meaningful portion of additions also reflects multiple hub feature implementations—ecosystem mini-hub, AI Access issuance, Agent Workspace, login-home conversion, app launcher, and a gacha-lobby dashboard (*feat(hub)…* commits). These changes suggest active expansion of user-facing surfaces and navigation flows, consistent with a product area still evolving in scope and UX.

The **-185 lines deleted** aligns with smaller cleanups and adjustments that accompany feature work and bug fixes (e.g., dashboard refactoring while converting to login-home hub, and onboarding durability changes). The inclusion of deterministic CREATE3 deployment configuration for a paymaster (*feat(paymaster): deterministic CREATE3 deployment with v4 config*) indicates infrastructure-level capability being added alongside front-end or hub work, while targeted documentation additions for private-transfer verification and resume handoff (*docs(private-transfer): M0 verification + constants + resume handoff*) suggest parallel efforts to formalize operational/verification details as features evolve.

## Next Steps
Next work is expected to focus on stabilizing and iterating on the newly integrated codebase (post-`toki-extension` consolidation) and refining the hub’s new flows (login-home, app launcher, ecosystem mini-hub, and workspace-related features) based on integration and user progression requirements. Further follow-through on deterministic deployment and private-transfer documentation is also likely as these capabilities are exercised in real environments.


# TON-total-supply

**GitHub**: [Link](https://github.com/tokamak-network/TON-total-supply)


## Overview
TON-total-supply appears to track and publish data related to the TON token’s total supply, serving as a reference point for supply transparency within the Tokamak ecosystem. Maintaining current, auditable supply records is relevant to users and investors because supply figures affect token economics analysis, reporting, and stakeholder communications. This repository’s value is primarily in keeping those records current and consistent over time.

## Statistics
| Metric | Value |
|--------|-------|
| Commits | 1 |
| Contributors | 1 |
| Lines Added | +12 |
| Lines Deleted | -6 |
| Net Change | +6 |


## Period Goals
During this reporting period, the primary goal was to refresh and extend the repository’s supply tracking materials to reflect the latest date-specific snapshot. Based on the single commit message, the team focused on updating the repository’s data sheet for the 2026.6.1 reporting point.

## Key Accomplishments
* **Updated the 2026.6.1 data sheet**: Adjusted the repository’s recorded supply data for the 2026.6.1 snapshot (“update the data sheet for 2026.6.1”), helping ensure stakeholders rely on up-to-date figures when reviewing token supply information.
* **Refined existing recorded entries while adding new ones**: Introduced incremental additions (+12) and removed outdated or superseded content (-6) as part of the 2026.6.1 update, improving the accuracy and internal consistency of the published data sheet for downstream use (analysis, reporting, and verification).

## Code Analysis
The net change of +6 lines reflects a targeted maintenance update rather than a broad functional expansion. Specifically, the additions (+12) align with incorporating updated data for the 2026.6.1 snapshot, while the deletions (-6) indicate the removal or replacement of prior entries as part of keeping the data sheet current (“update the data sheet for 2026.6.1”). This pattern is consistent with a repository that is primarily data-maintenance oriented: small, periodic edits that prioritize correctness and traceable updates over new code functionality.

## Next Steps
Continue periodic updates to the data sheet as new reporting dates occur, ensuring the repository remains a timely reference for token supply figures. Where applicable, maintain clear versioning or date-based entries so stakeholders can track changes across reporting periods.


# zk-X509

**GitHub**: [Link](https://github.com/tokamak-network/zk-X509)


## Overview
zk-X509 is a Tokamak Network repository focused on enabling integration workflows around zk-X509, including a registry/CMS layer, a prover-server, and client-facing tooling. During this period, the repository expanded its operational backend and developer-facing surfaces (SDK/CLI, portal) while adding security controls for registry writes, which directly affects how integrators publish and manage compliance-related metadata.

## Statistics
| Metric | Value |
|--------|-------|
| Commits | 48 |
| Contributors | 1 |
| Lines Added | +13,446 |
| Lines Deleted | -1,271 |
| Net Change | +12,175 |


## Period Goals
The work in this reporting period centered on making zk-X509 easier to integrate and operate by shipping a publishable SDK/CLI and a developer portal, alongside documentation for Sepolia testing and prover-server operations. In parallel, the team tightened registry/CMS security (signature-based authorization, anti-replay, and hardening) and improved backend scalability/operations by migrating CMS metadata storage to Firestore and optimizing frontend reads.

## Key Accomplishments
* **Migrated CMS metadata storage to Firestore**: Moved the backend CMS metadata store to Firestore (Firebase serverless) to simplify operations and provide a managed persistence layer for metadata used by the registry/CMS workflows (commit: “migrate CMS metadata store to Firestore (Firebase serverless)”).
* **Delivered a developer portal and publishable SDK/CLI**: Added a developer portal plus a publishable SDK/CLI to support third-party integration and standardized usage patterns for zk-X509 integration (commit/PR: “developer portal + publishable SDK/CLI for zk-X509 integration”, PR#142).
* **Introduced chain-specific scoping for CMS metadata**: Implemented network-scoped CMS metadata keyed by chainId to reduce cross-network ambiguity and improve correctness for multi-chain deployments (commit: “network-scope CMS metadata by chainId”).
* **Strengthened registry CMS write authorization**: Added owner-signature authentication for registry CMS writes, tightening who can modify registry-related metadata and reducing risk of unauthorized changes (commit/PR: “owner-signature auth for registry CMS writes”, PR#143).
* **Added anti-replay protections for CA-registry signatures**: Implemented a single-use signature guard to prevent replay of signatures when interacting with the CA-registry, improving integrity of signature-gated operations (commit/PR: “single-use signature guard for CA-registry (anti-replay)”, PR#145).
* **Hardened registry CMS against common web abuse patterns**: Applied security hardening measures including XSS and injection protections, size caps, and deduplicated reads to reduce attack surface and improve resilience under malformed inputs (commit/PR: “harden registry CMS — XSS, size caps, injection, dedup read”, PR#144).
* **Improved frontend performance via batched reads**: Optimized frontend data access by batching reads through Multicall3, reducing RPC round-trips and improving responsiveness for users interacting with on-chain data (commit: “batch reads via Multicall3…”).
* **Ensured node access is routed through connected wallets**: Updated the frontend so node access goes through the user’s connected wallet (MetaMask), aligning interactions with wallet-mediated permissions and user expectations (commit/PR: “route all node access through the connected wallet (MetaMask)”, PR#141).
* **Expanded ecosystem visibility with a project listing**: Added a “Built with zk-X509” project listing to highlight integrations and provide a discovery surface for users evaluating adoption and examples (commit/PR: “add ‘Built with zk-X509’ project listing”, PR#146).
* **Added an AI assistant chatbot for developer support**: Integrated a zk-X509 AI assistant chatbot using Tokamak AI / LiteLLM to provide in-product guidance and reduce friction for developers navigating setup and integration (commit/PR: “add zk-X509 AI assistant chatbot (Tokamak AI / LiteLLM)”, PR#147).
* **Extended prover-server capabilities for compliance workflows**: Added a compliance query API intended for admin KYC reconciliation, supporting administrative review and matching of compliance-related data flows (commit: “add compliance query API for admin KYC reconciliation”).
* **Improved documentation for testing and operations**: Updated the README with a Sepolia testing guide and aligned stale docs with current code, and added an operator guide plus delegated-proving FAQ to support ongoing operations and troubleshooting (commits/PRs: “add Sepolia testing guide…”, PR#139; “add local frontend setup against Sepolia…”, PR#140; “add prover-server operator guide and delegated-proving FAQ”).

## Code Analysis
The net +12,175 lines reflects substantial feature delivery across backend, frontend, and developer enablement. Major additions include the Firestore-backed CMS metadata migration (commit: “migrate CMS metadata store to Firestore”), the developer portal and publishable SDK/CLI (PR#142), and new user-facing surfaces such as the “Built with zk-X509” listing (PR#146) and the AI assistant chatbot integration (PR#147). Security-oriented additions are also prominent—owner-signature authorization for CMS writes (PR#143), a single-use signature guard to prevent replay (PR#145), and CMS hardening for XSS/injection and input constraints (PR#144)—indicating a shift toward operational readiness where data integrity and authorization controls are enforced.

The -1,271 lines deleted appear consistent with iterative refinement and cleanup following large feature merges, including addressing Copilot/accuracy fixes and review-driven adjustments (e.g., “address Copilot + accuracy fixes”, “review(pr#145): fix Firestore init/selection + sig casing + sweep throttle”, “refactor: simplify pass — centralize dev addresses + tighten SDK”). Performance work (batched Multicall3 reads) and correctness fixes (stamping chainId on admin save; bypassing cache for admin reads) suggest the codebase is being tuned for real usage scenarios rather than remaining purely experimental.

## Next Steps
Next work is likely to focus on stabilizing and iterating on the newly introduced Firestore-backed CMS path, signature-based security controls, and the developer-facing SDK/CLI and portal based on integration feedback. Continued refinement of prover-server compliance endpoints and operational documentation would be a natural continuation of the operator and admin workflow improvements added this period.


# zk-x509-ca-registry

**GitHub**: [Link](https://github.com/tokamak-network/zk-x509-ca-registry)


## Overview
`zk-x509-ca-registry` appears to serve as a registry of X.509 certificate authority (CA) artifacts and related service metadata used by Tokamak Network components that rely on CA-based trust. During this period, activity focused on registering and updating CA entries tied to specific chains and on-chain addresses, supporting operational correctness for services such as zkScatter users and relayers. For stakeholders, this repository matters because it is part of the trust and configuration surface area that enables dependent services to validate identities and route to the correct on-chain endpoints.

## Statistics
| Metric | Value |
|--------|-------|
| Commits | 12 |
| Contributors | 1 |
| Lines Added | +746 |
| Lines Deleted | -17 |
| Net Change | +729 |


## Period Goals
The primary goal this period was to expand and refresh the repository’s CA certificate set and associated service metadata, as reflected by repeated “Add/update CA certs + service metadata” commits. A second goal was to register specific CA/service entries for zkScatter user and relayer components across multiple environments (notably chain IDs 31337 and 11155111) with explicit on-chain addresses, as shown in the merged PRs.

## Key Accomplishments
* **Registered zkScatter relayer service metadata on Sepolia**: Added a registry entry for chain ID `11155111` at address `0x9fde6182b1fd10f2edfe15b704fe95787c170914` labeled “zkScatter Relayers,” improving clarity and alignment of environment-specific service configuration (PR#51; commit “Add/update CA certs + service metadata (#51)”).
* **Registered zkScatter user service metadata on Sepolia**: Added a registry entry for chain ID `11155111` at address `0x3cf6a96f1970053ffdf957074f988ad53d13ada3` labeled “zkScatter Users,” supporting correct referencing of the user-facing service endpoint/configuration for that network (PR#50; commit “Add/update CA certs + service metadata (#50)”).
* **Added CA material for zkScatter users in a local/dev environment**: Introduced a CA entry on chain ID `31337` for address `0x7f01274221ba4a8edbb7255b01fdc8c3f51cff9e` (“zkScatter_users”), strengthening the repository’s ability to support controlled testing and local deployments with explicit trust anchors (PR#49; commit “Add/update CA certs + service metadata (#49)”).
* **Added CA material for a relayer CA in a local/dev environment**: Added CA data on chain ID `31337` for address `0x05052c7ae7e15bcfe983506b2eebd691895fe8bc` (“Relayer CA”), enabling relayer-related flows to reference an explicit CA entry for the local/dev network (PR#48 and PR#46; commits “Add/update CA certs + service metadata (#48)” and “(#46)”).
* **Registered zkScatter users on a local/dev environment**: Registered chain ID `31337` at address `0x7f01274221ba4a8edbb7255b01fdc8c3f51cff9e` (“zkScatter-users”), improving consistency of registry-based lookups for zkScatter user components during testing (PR#47; commit “Add/update CA certs + service metadata (#47)”).
* **Registered multiple relayer-related entries on a local/dev environment**: Registered chain ID `31337` relayer entries, including `0x93b87e23ae6f5345ecc1ff20323a2def3351f579` (“Relayer CA”) and `0x05052c7ae7e15bcfe983506b2eebd691895fe8bc` (“Relayer CA”), indicating iterative alignment of relayer CA/service metadata for the same environment (PR#45, PR#44; commits “Add/update CA certs + service metadata (#45)” and “(#44)”).
* **Registered an additional relayer entry variant in a local/dev environment**: Registered chain ID `31337` at address `0x3008c1e01962fbfb8df578bf5b881d5ab9ae49b1` labeled “zlkScatter_relayers,” expanding the set of relayer-related registry entries (PR#43; commit “Add/update CA certs + service metadata (#43)”).
* **Registered a delegated no-disclosure entry in a local/dev environment**: Registered chain ID `31337` at address `0x0d3aa1ff33792cd98b966846b0f661276e8ea4e1` labeled “delegated-no-disclosure-1,” reflecting additional service/CA metadata tracked by the registry for privacy- or disclosure-scoped use cases (PR#42; commit “Add/update CA certs + service metadata (#42)”).

## Code Analysis
The +746/-17 net change is dominated by repeated additions of CA certificates and associated service metadata, as evidenced by nine commits titled “Add/update CA certs + service metadata” with large additions (+81 each for #40–#45, #47, #50, #51). This pattern is consistent with appending or expanding a structured registry (e.g., additional CA entries, chain/address records, and metadata blocks) rather than algorithmic code changes. Smaller update commits (#46, #48, #49 with +5/-5 and +7/-7) indicate iterative corrections or normalization of existing entries—likely adjusting previously added certificate/metadata records—suggesting operational tuning to keep registry data accurate. Overall, the work reflects a data-maintenance phase focused on completeness and correctness of trust/configuration records across environments, which is typical for a registry repository’s maturity progression.

## Next Steps
Continue registering and updating CA certificates and service metadata as additional services, environments, or on-chain addresses are introduced or rotated. Follow-on work should prioritize consistency checks across similarly named entries (e.g., zkScatter users/relayers variants) to minimize ambiguity in downstream lookups.