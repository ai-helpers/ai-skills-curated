---
name: opentrep
description: Understand, build, index, and operate OpenTREP (Open Travel Request Parser), a C++/Python travel-request interpretation and geographical point-of-reference (POR) search library built on Xapian and OpenTravelData (OPTD). Use for OpenTREP development, indexing, database backend (SQLite3/MySQL-MariaDB/PostgreSQL) work, and OPTD-driven index refreshes.
license: MIT
compatibility: "Requires: C++17 toolchain, CMake, Boost, Xapian, SOCI, Python 3 (bindings)"
metadata:
  author: ai-helpers
  version: "0.1.0"
  keywords:
    - opentrep
    - opentraveldata
    - xapian
    - travel-search
    - postgresql
    - sqlite
    - mysql
    - geolocation
---

# OpenTREP

## Overview

[OpenTREP](https://github.com/trep/opentrep) (Open Travel Request Parser) is a C++
transport-search library, with Python bindings, that interprets free-text travel
requests and resolves geographical points of reference (POR) — airports, cities,
train stations, ports, _etc._ It exposes a clean, object-oriented API
(`OPENTREP::interpretTravelRequest()`) that takes a character string containing the
travel request and yields the list of recognized terms along with their types.

For instance, the request
`Washington DC Beijing Monday a/r +AA -UA 1 week 2 adults 1 dog` yields:

* Origin airport: Washington, DC, United States (US)
* Destination airport: Beijing, China (CN)
* Date of travel: next Monday / Date of return: 1 week after next Monday
* Preferred airline: American Airlines (AA); non-preferred: United Airlines
* Number of travelers: 2 adults and a dog

OpenTREP uses [Xapian](https://www.xapian.org) for the information-retrieval part, and
indexes geographical/travel reference data (country names/codes, city names/codes,
airline names/codes, _etc._) primarily sourced from the
[OpenTravelData (OPTD) project](https://github.com/opentraveldata/opentraveldata), a
separate open-source repository maintaining reference POR (Points Of Reference) data
as CSV files. It can also maintain a relational lookup database alongside the Xapian
index; SQLite3,
MySQL/MariaDB, and PostgreSQL are supported.

OpenTREP powers the public search demo at
[transport-search.org](https://transport-search.org/).

## When to Use This Skill

Use this skill when:

* Building, testing, or packaging OpenTREP (CMake, RPM/`fedpkg`, Docker) on macOS or
  Linux (Fedora/CentOS/RHEL/Debian/Ubuntu).
* Adding or extending relational-database backend support (SQLite3, MySQL/MariaDB,
  PostgreSQL) in the database manager (`opentrep-dbmgr`), indexer, or searcher.
* Diagnosing full-scale indexing issues against the real OPTD POR data set (as opposed
  to the small test fixtures), e.g. parser edge cases, Xapian limits, or SQL
  constraint violations only visible at scale (~125k records).
* Designing or fixing the procedure that refreshes OpenTREP's Xapian index and
  relational database whenever the upstream OPTD data set changes.
* Using the Python bindings (`pyopentrep`) or the FastAPI-based web search front end.

## Architecture

| Component | Source path | Technology | Role |
|---|---|---|---|
| C++ core | `opentrep/` | C++ | Travel-request interpretation, indexing, relational persistence, and search engine |
| Python wrapper | `opentrep/python/` | Boost.Python and Protobuf | Exposes the C++ core to Python and exchanges `Travel` objects defined in `opentrep/bom/Travel.proto` |
| Web application | `gui/fastapi/` | FastAPI | Serves a travel-search experience over HTTP |

OpenTREP maintains two complementary state layers that must both be regenerated from
the same OPTD data whenever it is refreshed:

1. A Xapian full-text index.
2. Relational tables backed by SQLite3, MySQL/MariaDB, or PostgreSQL.

A common production pattern is to keep two deployment slots so a replacement Xapian
index and relational state can be prepared and validated before activation (a
green/blue-like deployment), using scripts such as `gui/fastapi/bin/trep-*.sh`.

## Data-sync tooling

`opentrep/ui/cmdline/opentrep-datasync` (Python 3, stdlib-only) downloads the OPTD POR
CSV directly from the `opentraveldata` GitHub repository, mimicking `opentrep-dbmgr`'s
CLI conventions: `-n/--noniata {0,1}` selects `optd_por_public.csv` (default) or
`optd_por_public_all.csv`; `-p/--porpath PATH` sets the destination directory (default:
cwd). It performs an atomic download (tempfile + `os.replace()`) with a header sanity
check, to support OPTD-refresh workflows.

## Relational-database backends

OpenTREP supports SQLite3, MySQL/MariaDB, and PostgreSQL as an optional relational
lookup layer alongside the Xapian index. When adding or extending support for a given
backend, mirror the existing MySQL/MariaDB integration across:

* Build/dependency configuration (CMake, SOCI backend selection).
* `opentrep-dbmgr` (database manager CLI): connection-string parsing, `create_user`,
  `create_tables`, `create_indexes`, and interactive/non-interactive (`-c`) commands.
* The indexer and searcher (POR writes and code/Geonames-ID lookups).
* The Python bindings, which sit on top of the same C++ core paths.

Practical lessons learned from adding PostgreSQL support alongside the pre-existing
SQLite3/MySQL-MariaDB backends:

* Generalize connection-string parsing to a key=value parser (rather than a fixed
  positional format) so that options like `host=`/`port=` are accepted for every
  backend, not just the one it was first written for.
* Database manager commands that assume an SQL backend is configured (e.g. list/lookup
  commands) should guard against being invoked with no SQL database at all, rather than
  crashing on an unchecked null session.
* Wrap database creation/initialization calls (`create_user`/`create_tables`/
  `create_indexes`) in backend-agnostic exception handling so a missing pre-provisioned
  database, or insufficient privileges, produces a clear error instead of aborting the
  process. Deployment-slot databases (e.g. `trep0`, `trep1`, ...) are expected to be
  pre-created by a database admin/superuser before the manager runs.
* Verify the built-in default connection string (e.g. a `DEFAULT_OPENTREP_PG_CONN_STRING`
  constant) actually matches the naming convention used by the rest of the tooling
  (deployment-slot suffixing in particular) — a stale default silently targets the
  wrong database name.
* Validate at full scale (the real, ~125k-row `optd_por_public_all.csv`), not just
  against small test fixtures. Full-scale runs can surface issues invisible at small
  scale, for example:
  * Parser edge cases in alternate-name fields (e.g. an embedded `=` character that a
    naive lookahead heuristic misclassifies as a field separator). Prefer an
    unambiguous delimiter-based grammar (stop only at the real field separators) over
    heuristics that "guess" based on surrounding characters.
  * Fixed-size key limits in the search engine (for instance Xapian's 255-byte spelling
    key limit) that only trigger on POR values long enough to exceed them.
  * A single whole-run transaction that is too large to commit atomically at full
    scale; switch to incremental commits.
  * Duplicate primary keys in the upstream data set itself (a data-quality issue, not a
    code bug) that violate a unique index; dedup (e.g. keep the last-inserted row)
    rather than aborting the whole index build.
* Once a backend works end-to-end (schema init, writes, lookups, full-scale indexing),
  flipping it to be the default is a separate, lower-risk step from adding the support
  itself — do not conflate the two milestones.

### Setting up a PostgreSQL database and user for OpenTREP

Deployment-slot databases (`trep0`, `trep1`, ...) must be pre-created, together with a
dedicated role/schema, before `opentrep-dbmgr` can run
`create_user`/`create_tables`/`create_indexes` against them:

```bash
PG_SVR="localhost"; PG_ADM_USR="$USER"

psql -h $PG_SVR -U $PG_ADM_USR -d postgres -c "create database trep0; create database trep1;"
psql -h $PG_SVR -U $PG_ADM_USR -d postgres -c "create user trep with encrypted password '<trep-pass>'; grant all privileges on database trep0 to trep; grant all privileges on database trep1 to trep;"
psql -h $PG_SVR -U $PG_ADM_USR -d trep0 -c "grant all on schema public to trep;"
psql -h $PG_SVR -U $PG_ADM_USR -d trep0 -c "create schema trep; grant all on schema trep to trep; grant all privileges on all tables in schema trep to trep;"
psql -h $PG_SVR -U $PG_ADM_USR -d trep1 -c "grant all on schema public to trep;"
psql -h $PG_SVR -U $PG_ADM_USR -d trep1 -c "create schema trep; grant all on schema trep to trep; grant all privileges on all tables in schema trep to trep;"

# Check that the access works
psql -h $PG_SVR -U trep -d trep0 -c "select 42 as nb;"
psql -h $PG_SVR -U trep -d trep1 -c "select 42 as nb;"
```

See also the
[OpenTREP database and user section](https://github.com/data-engineering-helpers/ks-cheat-sheets/blob/main/db/postgresql/README.md#opentrep-database-and-user)
of the public PostgreSQL cheat sheet, which OpenTREP's own README links to.

## Refreshing the index after an OpenTravelData (OPTD) update

OpenTREP's Xapian index and relational database are only as fresh as the OPTD POR data
they were built from. A robust refresh procedure should:

1. Identify the required OPTD POR data version and record the source revision/release
   used for each rebuild (`opentrep-datasync` can fetch the current data file, but the
   exact upstream revision/commit should still be tracked).
2. Fetch and validate the updated POR data before any active OpenTREP index is
   replaced.
3. Rebuild the Xapian index and the configured relational-database index from the same
   validated OPTD data set.
4. On a failed download, validation, or build, leave the previously active index
   usable and return a clear failure signal — do not partially overwrite a working
   deployment.
5. After a successful rebuild, activate the new index predictably (for example via a
   deployment-slot swap) and run a smoke test to verify OpenTREP can search it.
6. Document how OPTD updates trigger or initiate refreshes, and how operators can run
   the procedure manually.

Using two deployment slots (an active one and a staging one) makes steps 3-5 safe: the
staging slot's Xapian index and relational database are rebuilt and validated first,
and only then does the deployment switch to it, leaving the previous slot as an instant
rollback target.

## Development and release workflow

1. Develop and validate the C++ core, Python wrapper, and any web front end on a
   development machine.
2. Package stable changes as standard RPMs (Fedora/EPEL) or through the project's other
   supported distribution channels.
3. When targeting a Fedora/EPEL package, test new versions in the corresponding
   `*-testing`/candidate repository when available; promotion to the stable release
   mirrors typically follows the distribution's normal update-testing cadence (roughly
   a week for Fedora/EPEL Bodhi karma-based promotion).
4. Upgrade a running deployment using a green/blue-like procedure: build and validate a
   new index/database in the inactive deployment slot, then switch traffic to it.

## Troubleshooting notes

* When both a distribution package (RPM) and a from-source build are present on the
  same host, make sure the from-source binaries are actually the ones being executed —
  a bare command name on `PATH`, or the dynamic linker cache (`ldconfig`), can silently
  keep resolving to the packaged (older) version even after a fresh `make install`.
* A systemd service that appears "active" can still be crash-looping at the
  application level (for example on a Python `ModuleNotFoundError` after removing a
  package that used to provide `site-packages` content); check the application's own
  log file, not just `systemctl status`/`journalctl`, when a web front end silently
  stops responding correctly after a package change.
* When reproducing a production-only crash locally fails, compare the exact toolchain
  versions (compiler, and especially library versions such as Boost) between the
  reproduction environment and production before concluding the code is fine — but
  also keep looking for a genuine, toolchain-independent bug in ambiguous parsing
  heuristics; a heuristic that merely happens to work on one toolchain's standard
  library implementation is itself a latent bug worth fixing outright.

## Resources

* **Project**: [github.com/trep/opentrep](https://github.com/trep/opentrep)
* **Upstream data**: [OpenTravelData (OPTD)](https://github.com/opentraveldata/opentraveldata)
* **Public search demo**: [transport-search.org](https://transport-search.org/)
* **PostgreSQL cheat sheet** (OpenTREP database/user section):
  [ks-cheat-sheets/db/postgresql](https://github.com/data-engineering-helpers/ks-cheat-sheets/blob/main/db/postgresql/README.md#opentrep-database-and-user)
* **Xapian**: [xapian.org](https://www.xapian.org)
* **SOCI**: [soci.sourceforge.net](http://soci.sourceforge.net)
