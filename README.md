# Knowledge sharing - Curated AI Skills

## Table of Content (ToC)

* [Knowledge sharing \- Curated AI Skills](#knowledge-sharing---curated-ai-skills)
  * [Table of Content (ToC)](#table-of-content-toc)
  * [Overview](#overview)
  * [References](#references)
    * [AI skills](#ai-skills)
      * [Vercel labs](#vercel-labs)
      * [Agent skill formatting](#agent-skill-formatting)
      * [Skills related to dbt](#skills-related-to-dbt)
      * [AI helpers skill sets](#ai-helpers-skill-sets)
        * [Managing Python projects with uv](#managing-python-projects-with-uv)
    * [Data Engineering Helpers](#data-engineering-helpers)
  * [Getting started](#getting-started)
    * [List the skills already installed](#list-the-skills-already-installed)
    * [Install a skill locally](#install-a-skill-locally)
    * [Remove a skill](#remove-a-skill)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc.go)

## Overview

[This project](https://github.com/ai-engineering-helpers/ai-skills-curated)
aims at collecting so-called AI agent/assistant skills (and associated rules).
Each skill set may be installed either locally in a given project or in the user
space, for instance in the `~/.agents/skills/`, where typical assistants/agents
(_e.g._, Copilot, Gemini, Claude) will find them and will be able to use them.

Even though the members of the GitHub organization may be employed by
some companies, they speak on their personal behalf and do not represent
these companies.

## References

### AI skills

#### Vercel labs

* [Vercel labs - Skills homepage](https://skills.sh)
* [GitHub - Vercel labs - Skills](https://github.com/vercel-labs/skills)

#### Agent skill formatting

* [Agent Skills - Specification](https://agentskills.io/specification)

#### Skills related to dbt

* [dbt doc - dbt agent skills](https://docs.getdbt.com/blog/dbt-agent-skills)

#### AI helpers skill sets

* [GitHub - AI Helpers - AI skills curated (this Git repository)](https://github.com/ai-helpers/ai-skills-curated)
* [GitHub - AI Helpers - AI skills curated - Overview notebook](https://github.com/ai-helpers/ai-skills-curated/blob/main/notebooks/000%20-%20KS%20-%20Curated%20AI%20Skills%20-%20Overview.ipynb)

##### Managing Python projects with uv

* [GitHub - AI Helpers / AI Skills curated - `managing-python-projects-with-uv` skill set](https://github.com/ai-helpers/ai-skills-curated/tree/main/agents/skills/managing-python-projects-with-uv)
* [Skills.sh - AI Helpers / AI Skills curated - `managing-python-projects-with-uv` skill set](https://skills.sh/ai-helpers/ai-skills-curated/managing-python-projects-with-uv)

### Data Engineering Helpers

* [Data Engineering Helpers - Knowledge Sharing - AI Skills](https://github.com/data-engineering-helpers/ks-cheat-sheets/blob/main/ai/rules-skills/)
* [Data Engineering Helpers - Knowledge Sharing - Databricks AI Dev Kit](https://github.com/data-engineering-helpers/ks-cheat-sheets/blob/main/ai/rules-skills/)
* [Data Engineering Helpers - Knowledge Sharing - JavaScript (JS) world](https://github.com/data-engineering-helpers/ks-cheat-sheets/blob/main/programming/js-world/)

## Getting started

### List the skills already installed

* List the skills brought by the current project:

```bash
npx skills list
```

* List the skills installed globally (in the user directory, that is,
  in the `$HOME/.agents/skills/` directory):

```bash
npx skills list -g
```

### Install a skill locally

* The available skill sets may be browsed online: all the skill sets are in the
  [`agents/skills/` directory](https://github.com/ai-helpers/ai-skills-curated/blob/main/agents/skills/)

* In order to install a skill set for generic agents (the `--global` parameter
  will have the skill set installed in the `$HOME/.agents/skills/` global user
  directory):

```bash
npx skills add ai-helpers/ai-skills-curated <sill-set> --global
```

* For instance, for the
  [`managing-python-projects-with-uv`](https://github.com/ai-helpers/ai-skills-curated/tree/main/agents/skills/managing-python-projects-with-uv/)
  skill set:

```bash
npx skills add ai-helpers/ai-skills-curated managing-python-projects-with-uv --global
```

### Remove a skill

* In order to remove an installed skill set, use `npx skills remove <skill>`.
  For instance, to remove the `managing-python-projects-with-uv` skill set:

```bash
npx skills remove managing-python-projects-with-uv -g
```

### Update skills

* Upgrade the skills (it fetches potential new releases of the installed skills
  and installs those latest versions):

```bash
npx skills update
```
