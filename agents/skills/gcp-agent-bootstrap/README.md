# gcp-agent-bootstrap — GCP Project & MCP Server Bootstrap Skill

## What this skill does

Helps you **bootstrap a Google Cloud Platform (GCP) project** and set up a local
Python stdio MCP server that exposes GCP services (Vertex AI, Google Drive) to
Copilot CLI through the Model Context Protocol (MCP).

## When to use it

- You need to access GCP services (Vertex AI text generation, data extraction, Google
  Drive) from Copilot CLI.
- You are setting up a new GCP free-tier project from scratch.
- You are hitting OAuth credential-attachment issues with hosted MCP servers and want
  a local workaround.
- You need a reproducible GCP + MCP setup for development or demonstration purposes.

## Quick start (for humans)

1. Install prerequisites:

   ```bash
   brew install --cask google-cloud-sdk && brew install uv
   ```

2. Authenticate and set your GCP project:

   ```bash
   gcloud auth login
   gcloud auth application-default login --scopes=https://www.googleapis.com/auth/cloud-platform
   gcloud config set project YOUR-PROJECT-ID
   gcloud services enable aiplatform.googleapis.com drive.googleapis.com
   ```

3. Clone and run the showcase project:

   ```bash
   git clone https://github.com/data-engineering-helpers/gcp-agent-bootstrap-showcase.git
   cd gcp-agent-bootstrap-showcase
   make init
   make auth-adc
   make auth-drive
   make auth-verify
   make run
   ```

4. Open Copilot CLI in a project session and ask it to use the `gcp-agent-bootstrap`
   skill (or mention GCP/Vertex AI/MCP setup) — it will walk you through the two
   separate authentication flows (ADC for Vertex AI, OAuth token for Drive) and verify
   the setup.

## What's inside

- **Problem context** — why a local MCP server sidesteps a known Copilot CLI Drive
  MCP credential-attachment issue ([GitHub issue #3838](https://github.com/github/copilot-cli/issues/3838)).
- **Split-auth model** — ADC for Vertex AI vs. a separate OAuth client/token for
  Google Drive, including the first-time Drive OAuth client setup (test users,
  `Error 403: access_denied` troubleshooting).
- **Quick reference** — `make` targets for setup, authentication, verification, and
  running the MCP server, plus the tools it exposes (`generate_text`,
  `list_available_models`, `extract_structured_data`, `drive-list_recent_files`).

## Related resources

- [gcp-agent-bootstrap-showcase](https://github.com/data-engineering-helpers/gcp-agent-bootstrap-showcase) —
  the companion project implementing the MCP server.
- [GitHub issue #3838](https://github.com/github/copilot-cli/issues/3838) — the Drive
  MCP OAuth issue this skill works around.
- [Google Cloud free tier](https://cloud.google.com/free)
- [Model Context Protocol](https://spec.modelcontextprotocol.io/)
