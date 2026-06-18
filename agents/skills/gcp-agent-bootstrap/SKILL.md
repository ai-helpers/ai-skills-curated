---
name: gcp-agent-bootstrap
description: Bootstrap Google Cloud Platform (GCP) projects and set up Python stdio MCP servers to access Vertex AI and other GCP services. Use for GCP project initialization, API enablement, authentication setup, and MCP server configuration.
license: MIT
compatibility: "Requires: gcloud CLI, Python 3.10+, uv"
metadata:
  author: ai-helpers
  version: "0.1.0"
  keywords:
    - gcp
    - google-cloud
    - mcp
    - vertex-ai
    - authentication
    - copilot-cli
---

# GCP Agent Bootstrap

## Overview

This skill helps you **bootstrap Google Cloud Platform (GCP) projects** and set up a **local Python stdio MCP server** that provides access to GCP services (Vertex AI, Cloud Storage, Google Drive API) through the Model Context Protocol (MCP).

**Use this skill for:**

* Setting up a new GCP project from scratch
* Enabling required GCP APIs (Vertex AI, Cloud Storage, Drive API)
* Configuring Google Cloud authentication (gcloud, ADC)
* Creating a local Python MCP server that proxies GCP service access
* Configuring Copilot CLI to use the GCP MCP server
* Using GCP services (Vertex AI text generation, etc.) through Copilot CLI

## When to Use This Skill

Use this skill when:

* You need to access GCP services from Copilot CLI
* You're setting up a new GCP free-tier project
* You want to use Vertex AI (text generation, data extraction) through MCP
* You're experiencing OAuth credential-attachment issues with hosted MCPs
* You need a reproducible GCP + MCP setup for development or demonstration
* You want to extend the MCP server with additional GCP services
* The user asks about GCP authentication, MCP servers, or Vertex AI integration

## Problem Context

The Copilot CLI Drive MCP has a known issue where authentication credentials fail to attach after reauth. This skill provides a **workaround**: a local Python stdio MCP server that uses Google Cloud's Application Default Credentials (ADC) instead of OAuth tokens, eliminating credential-attachment issues entirely.

See [GitHub Issue #3838](https://github.com/github/copilot-cli/issues/3838) for details.

## Quick Start

```bash
# 1. Install: brew install --cask google-cloud-sdk && brew install uv

# 2. Authenticate
gcloud auth login
gcloud auth application-default login

# 3. Create/set GCP project
gcloud config set project YOUR-PROJECT-ID

# 4. Enable APIs
gcloud services enable aiplatform.googleapis.com

# 5. Clone and run
git clone https://github.com/data-engineering-helpers/gcp-agent-bootstrap-showcase.git
cd gcp-agent-bootstrap-showcase
make init && make run
```

## Setup Guide

See the [gcp-agent-bootstrap-showcase](https://github.com/data-engineering-helpers/gcp-agent-bootstrap-showcase) repository for complete, step-by-step instructions.

## Quick Reference

### Commands

```bash
make setup                                         # One-time setup
make run                                          # Start MCP server
make auth-verify                                  # Verify authentication
make gcp-verify                                   # Verify GCP setup
gcloud auth application-default login             # Refresh ADC
gcloud config set project YOUR-PROJECT-ID        # Set GCP project
gcloud services enable aiplatform.googleapis.com  # Enable Vertex AI API
```

### Tools Provided

* `generate_text` — Generate text via Vertex AI
* `list_available_models` — List available models
* `extract_structured_data` — Extract structured info from text

## Resources

* **Showcase Project**: [gcp-agent-bootstrap-showcase](https://github.com/data-engineering-helpers/gcp-agent-bootstrap-showcase)
* **GitHub Issue**: [#3838](https://github.com/github/copilot-cli/issues/3838) (Drive MCP OAuth issue)
* **Google Cloud Free Tier**: [cloud.google.com/free](https://cloud.google.com/free)
* **MCP Protocol**: [spec.modelcontextprotocol.io](https://spec.modelcontextprotocol.io/)
