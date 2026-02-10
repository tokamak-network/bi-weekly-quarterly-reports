# Prompt

# Objective

- Based on the attached files, write the **Monthly Work Report** with high completeness.
- Output: Monthly Work Report (Markdown format).
- Success Criteria:
    1. **Format Consistency**: Must follow the exact same section structure, hierarchy, and formatting rules defined in the result format.
    2. **Content Completeness**: All activities, achievements, and work performed in monthly must be included without omission, and not only code development but also completed tasks in process such as testing completed (QA/Alpha/Beta/Non-dev), feedback analysis, major decision-making must be included in “Work” or “Key Achievement”.
    3. **Logical Structure**: Maintain a clear composition such as Deliverable / Work (by project) / Plan.
    4. **Style Consistency**: Follow the development organization writing style (concise, technical, commit/PR link usage).
    5. **Verifiability**: Write based on accurate links, work summaries, and commit/PR as much as possible for technical and factual work.

# Context

- Report format: structured by project with Deliverable → Work → Plan.
    - **Deliverable**: Artifacts with public URLs (Medium, X, Official Releases). Format: `[Full Title](URL)`.
    - **Work**: Monthly activities performed. Format: `Description ([Type](URL))`.
    - **Plan**: Deduce Next month plan based on the files attached. If
- The monthly report must follow the same structure, depth, and writing style.
- Each project categorizes the work content according to the subject, and if PR and commit exist in the same category at the same time, PR links are used in the report. (The PR often includes multiple commitments, which can lead to overlapping issues.) When using commit link, use only one commit that is key to each topic.

# Constraints

- Do not change the structural rules of the report.
- Adding any new sections is not allowed, and the project grouping (Tokamak Rollup Hub – SDK / Platform / Mainnet Launch / Cross Trade / DRB) must be kept.
- Categorize tasks not by *person* but by *project*.
- If Slack or meeting notes include expressions such as “completed”, “finished”, “done”, “tested”, “received feedback”, then even if no commit link exists, this must be written as a Work item.
- Only data with keywords derived from TRH, DRB, and Cross-Trade projects are used to prepare reports. (**Strictly** Exclude keywords such as "eco", "ooo", and "Tokamak-zk" among the data.)
- **Single-line Evidence Rule**: Do NOT create a separate bullet point for evidence links. The work description and its evidence link must be on the **same line**.
- **Link Text Convention**: The clickable text for the link must be the **Type of Source** only (e.g., `PR`, `Commit`, `Doc`, `Slide`, `Note`, `Thread`). Do not use the full title of the PR or Commit as the link text.
    - Correct: `Implemented shutdown logic ([PR](URL))`
    - Incorrect: `Implemented shutdown logic ([Feat: shutdown logic](URL))`
    - Incorrect: `Implemented shutdown logic (https://...)`
- **PR Priority & Aggressive Exclusion Rule:**
    - **Topic Clustering**: Before listing items, group all data (PRs and Commits) by specific "Feature Topics" (e.g., Shutdown, Backup, DRB, Cross Trade).
    - **PR Dominance**: If a PR exists within a "Feature Topic", assume **ALL** commits related to that topic (including sub-tasks like contracts, scripts, workflows, logic updates) are part of that PR.
    - **Exclude Sub-tasks**: Do NOT list commits that appear to be implementation details (e.g., "implemented logic", "added script", "updated contract", "fixed bug") of a feature if a PR for that feature is present.
    - **Author/Time Heuristic**: If a Commit and a PR share the same **Author** and **Project** within the same timeframe, and share keywords (even loosely, e.g., "Shutdown" PR vs "Force Withdrawal" Commit), treat the Commit as merged into the PR and **exclude it**.
    - **When in doubt, exclude the commit**: If you are unsure if a commit is standalone or part of a PR, prioritize the PR and omit the commit to keep the report concise.

# Procedure

1. **Format Analysis**: Analyze the entire structure, section title, and markdown format of the result output and use it as the standard.
2. **Work Information Collection**: Based on the attached files containing monthly work data, extract the achievements and activities. If missing data exists, request clarification. Especially if early of month Slack or Notion logs show test activities or feedback discussions, group them together as single Work items. If Medium.com or X.com URLs are shared, extract as Deliverable candidates.
3. **Data Processing (Filter Strategy)**:
    - **Step 1**: Extract all **PRs** first. These are the main items.
    - **Step 2: Semantic Filtering & Deduplication**
        - Identify the "Core Theme" of each PR (e.g., PR #383 is "Shutdown Helper").
        - Scan all Commits. If a commit describes a component necessary for that Core Theme (e.g., "contracts for withdrawal", "blocking scripts" are necessary components of a "Shutdown Helper"), mark them as **[Covered]**.
        - **Action**: Remove all items marked as **[Covered]** from the final list. Only list Commits that introduce a completely distinct feature unrelated to any listed PRs.
4. **Report Composition**: Apply monthly data to the same section structure (Deliverable → Work → by project / Plan). Classify based on work content, not persons. Make sure a non-developer can recognize core work easily.
5. **Formatting Work Items**:
    - Combine the activity description and the evidence link into a single bullet point.
    - Format: `Activity description ([Source Type](URL))`
    - If there are multiple links for one item, separate them with commas: `([PR](URL), [Commit](URL))`
6. **Draft Writing**: Write the monthly report in Markdown.
7. **Verification**: Check structure, tone, and placement. Verify links work and confirm that only Project TRH, DRB, Cross Trade information is included.

# Output Format

Final output must follow this exact Markdown structure:

```markdown
# Monthly Report - ${month} ${year}

## Deliverable
* Official Release Note v2.1.0[Release](https://github.com/...)
* Medium Article: New Feature Announcement[URL](https://medium.com/...)

## Work

### 1. Tokamak Rollup Hub – Deployment SDK

* Key Achievement (if necessary)
	* Successfully deployed the alpha version on testnet.

* **Topic 1**
	* Refactored deployment scripts for stability ([Commit](https://github.com/...))
  * Discussed and finalized the API specification ([Note](https://notion.so/...))

### 2. Tokamak Rollup Hub – Platform

…

### 3. Tokamak Rollup Hub – Mainnet Launch Preparation

…

### 4. Cross Trade

…

### 5. DRB

…

## Next Month Plan
* **Tokamak Rollup Hub - Deployment SDK**: Plan details...
```