# opentrep — OpenTREP Development, Indexing, and Operations Skill

## What this skill does

Helps you build, index, extend, and operate
[OpenTREP](https://github.com/trep/opentrep) (Open Travel Request Parser), a
C++/Python library that interprets free-text travel requests and resolves
geographical points of reference (airports, cities, train stations, ports, _etc._)
using [Xapian](https://www.xapian.org) and reference data from
[OpenTravelData (OPTD)](https://github.com/opentraveldata/opentraveldata).

## When to use it

- You are building, testing, or packaging OpenTREP (CMake, `fedpkg`/RPM, Docker).
- You are adding or extending a relational-database backend (SQLite3, MySQL/MariaDB,
  PostgreSQL) in the database manager, indexer, or searcher.
- You are diagnosing an indexing issue that only shows up at full scale against the
  real ~125k-row OPTD POR data set (parser edge cases, Xapian key limits, SQL
  constraint violations, _etc._).
- You are designing or fixing the procedure that refreshes OpenTREP's Xapian index and
  relational database after the upstream OPTD data set changes.
- You are using the Python bindings (`pyopentrep`) or the FastAPI web search front end.

## Quick start (for humans)

1. Open Copilot CLI (or another skill-aware agent) in an OpenTREP project session.
2. Ask the agent to use the `opentrep` skill, or mention OpenTREP, Xapian indexing,
   or one of the relational-database backends — the skill's `description` should
   trigger automatic discovery.
3. Describe your task, for example:
   - "Add PostgreSQL support to OpenTREP, mirroring the MySQL/MariaDB backend."
   - "Diagnose why full-scale indexing aborts on this POR record."
   - "Design the OPTD-triggered index-refresh procedure."
4. The agent follows the guidance in [`SKILL.md`](SKILL.md): architecture overview,
   database-backend implementation lessons, the PostgreSQL database/user setup
   snippet, the index-refresh procedure checklist, and the release/deployment
   workflow.

## What's inside

- **Architecture** — the C++ core, Python wrapper, and FastAPI web front end, plus the
  two state layers (Xapian index + relational database) kept in sync.
- **Data-sync tooling** — `opentrep-datasync`, which fetches the OPTD POR CSV directly
  from GitHub.
- **Relational-database backends** — practical lessons learned from adding a new
  backend (connection-string parsing, exception-safe initialization, full-scale-only
  bugs) plus a ready-to-use PostgreSQL database/user provisioning snippet.
- **Index refresh after an OPTD update** — a procedure checklist covering data
  validation, atomic rebuilds, and safe activation (deployment-slot swap).
- **Development and release workflow** — Fedora/EPEL packaging and green/blue-style
  deployment upgrades.
- **Troubleshooting notes** — stale-binary/`ldconfig` pitfalls, silently crash-looping
  services, and toolchain-version mismatches when reproducing production issues
  locally.

## Related resources

- [OpenTREP](https://github.com/trep/opentrep) — the project itself.
- [OpenTravelData (OPTD)](https://github.com/opentraveldata/opentraveldata) — the
  upstream reference POR data set OpenTREP indexes.
- [transport-search.org](https://transport-search.org/) — public search demo.
- [PostgreSQL cheat sheet](https://github.com/data-engineering-helpers/ks-cheat-sheets/blob/main/db/postgresql/README.md#opentrep-database-and-user) —
  OpenTREP database/user provisioning section.
