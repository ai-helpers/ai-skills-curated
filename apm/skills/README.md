# Short introduction to Microsoft Agent Package Manager (APM)

## Table of Contents (ToC)

* [Short introduction to Microsoft Agent Package Manager (APM)](#short-introduction-to-microsoft-agent-package-manager-apm)
  * [Table of Contents (ToC)](#table-of-contents-toc)
  * [Overview](#overview)
  * [References](#references)
  * [Examples of AI Helpers curated skills](#examples-of-ai-helpers-curated-skills)
    * [Managing Python projects with uv](#managing-python-projects-with-uv)
  * [Agent life\-cycle with APM](#agent-life-cycle-with-apm)
    * [Initial agent/skill creation](#initial-agentskill-creation)
    * [Day to day workflow with APM](#day-to-day-workflow-with-apm)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc.go)

## Overview

[This section of the AI Helpers curated skills](https://github.com/ai-helpers/ai-skills-curated/blob/main/apm/skills/README.md)
is a short reference about Microsoft Agent Package Manager (APM).

## References

* [Microsoft - Agent Package Manager (APM) home page](https://microsoft.github.io/apm/)
* [GitHub - Microsoft - Agent Package Manager (APM)](https://github.com/microsoft/apm)
  * [Microsoft docs - APM - Getting Started](https://microsoft.github.io/apm/getting-started/quick-start/)
  * [Microsoft docs - APM - Your first package](https://microsoft.github.io/apm/getting-started/first-package/)
  * [Microsoft - APM - Dependency management](https://microsoft.github.io/apm/guides/dependencies/)
  * [Microsoft - APM - CLI commands](https://microsoft.github.io/apm/reference/cli-commands/)

## Examples of AI Helpers curated skills

### Managing Python projects with uv

* Original curated skill:
  [GitHub - AI Helpers - Curated agent skills - managing-python-projects-with-uv skill](https://github.com/ai-helpers/ai-skills-curated/blob/main/agents/skills/managing-python-projects-with-uv/)
  * The same skill, packaged with APM:
  [GitHub - AI Helpers - Curated agent skills - APMed version of managing-python-projects-with-uv](https://github.com/ai-helpers/ai-skills-curated/blob/main/apm/skills/managing-python-projects-with-uv/)

## Agent life-cycle with APM

### Initial agent/skill creation

* Create an empty project and go into the created directory:

```bash
apm init managing-python-projects-with-uv && cd managing-python-projects-with-uv
```

* Add the `apm.yml` file to Git:

```bash
git add apm.yml
```

* Install a runtime:

```bash
apm runtime setup copilot
```

* Add the dependency on the actual skill:

```bash
apm install --verbose https://github.com/ai-helpers/ai-skills-curated
```

* Add missing assets (for some reasons, the assets are not installed) and
  do some cleanup:

```bash
cp ../../../agents/skills/managing-python-projects-with-uv/assets managing-python-projects-with-uv/
git add managing-python-projects-with-uv/assets
git rm -f managing-python-projects-with-uv/.github/agents/README.agent.md
```

* Compile the skill:

```bash
apm compile
```

### Day to day workflow with APM

* Reference:
  [Microsoft docs - APM - Quick start - Day-to-day workflow](https://microsoft.github.io/apm/getting-started/quick-start/#day-to-day-workflow)

* When a new developer joins the team:

```bash
git clone <your-repo>
cd <your-repo>
apm install
```

* The lockfile ensures everyone gets the same agent configuration. Same as
  `npm install` after cloning a Node project.

* Add more packages as your project evolves:

```bash
apm install github/awesome-copilot/skills/review-and-refactor
```

* What to commit:

* `apm.yml` and `apm.lock.yaml` — version-controlled, shared with the team
* `.github/` deployed files (`prompts/`, `agents/`, `instructions/`, `skills/`,
  `hooks/`) — commit them so every contributor (and Copilot on github.com) gets
  agent context immediately after cloning, before they run apm install to sync
  and regenerate files.
* `.claude/` deployed files (`agents/`, `commands/`, `skills/`, `hooks/`) — same
  rationale for Claude Code users: committed files give instant context on
  clone, while `apm install` remains the way to refresh them from `apm.yml`
* `.cursor/` deployed files (`rules/`, `agents/`, `skills/`, `hooks/`) — same
  rationale for Cursor users.
* `apm_modules/` — add to `.gitignore`. Rebuilt from the lockfile on install

!**Keeping deployed files in sync**
> When you update `apm.yml`, re-run `apm install` and commit the changed
> `.github/`, `.claude/`, and `.cursor/` files. A CI drift check catches stale
> files automatically

!**Using Codex or Gemini?**
> These tools use different configuration formats. Run `apm compile` after
> installing to generate their native files.
> See the [Compilation guide](https://microsoft.github.io/apm/guides/compilation/)
> for details.
