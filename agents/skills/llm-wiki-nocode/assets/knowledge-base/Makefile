.PHONY: init convert convert-main convert-notebooks tabs-sync snapshots-sync base-md-sync wiki-ingest rename fix-home

init:
	uv sync

convert:
	@test -n "$(NOTEBOOK)" || (echo "NOTEBOOK is required" && exit 1)
	uv run python scripts/ipynb-to-md.py "$(NOTEBOOK)" --name-mode exact
	@paths_file=$$(mktemp); \
	printf '%s\n' "memory/kb/md/$$(basename "$(NOTEBOOK)" .ipynb).md" > "$$paths_file"; \
	$(MAKE) base-md-sync PATHS_FILE="$$paths_file"; \
	rm -f "$$paths_file"

convert-main:
	uv run python scripts/ipynb-to-md.py "notebooks/05 - DKT - Main.ipynb" --output-dir memory/kb/md --name-mode exact
	@paths_file=$$(mktemp); \
	printf '%s\n' "memory/kb/md/05 - DKT - Main.md" > "$$paths_file"; \
	$(MAKE) base-md-sync PATHS_FILE="$$paths_file"; \
	rm -f "$$paths_file"

convert-notebooks:
	uv run python scripts/ipynb-to-md.py notebooks --output-dir memory/kb/md --name-mode exact
	$(MAKE) base-md-sync

tabs-sync:
	@test -n "$(NOTEBOOK)" || (echo "NOTEBOOK is required" && exit 1)
	python3 scripts/chrome_tabs_sync.py "$(NOTEBOOK)"
	$(MAKE) snapshots-sync

rename:
	@test -n "$(SRC)" || (echo "SRC is required" && exit 1)
	@test -n "$(DST)" || (echo "DST is required" && exit 1)
	python3 scripts/rename_md.py "$(SRC)" "$(DST)"
	@paths_file=$$(mktemp); \
	printf '%s\n' "$(DST)" > "$$paths_file"; \
	$(MAKE) base-md-sync PATHS_FILE="$$paths_file"; \
	rm -f "$$paths_file"
	$(MAKE) snapshots-sync

fix-home:
	@test -n "$(SRC)" || (echo "SRC is required" && exit 1)
	@test -n "$(HOME_REPO)" || (echo "HOME_REPO is required" && exit 1)
	python3 scripts/fix_home_md.py "$(SRC)" "$(HOME_REPO)"
	@paths_file=$$(mktemp); \
	printf '%s\n' "$(SRC)" > "$$paths_file"; \
	$(MAKE) base-md-sync PATHS_FILE="$$paths_file"; \
	rm -f "$$paths_file"
	$(MAKE) snapshots-sync

snapshots-sync:
	python3 scripts/snapshots_sync.py

base-md-sync:
	uv run python scripts/base_md_sync.py $(if $(PATHS_FILE),--paths-file "$(PATHS_FILE)",) $(PATHS)
	$(MAKE) wiki-ingest

wiki-ingest:
	uv run python scripts/wiki-ingest.py scan
