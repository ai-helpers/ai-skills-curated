.PHONY: init convert convert-main convert-notebooks tabs-sync snapshots-sync base-md-sync wiki-ingest

init:
	uv sync

convert:
	@test -n "$(NOTEBOOK)" || (echo "NOTEBOOK is required" && exit 1)
	uv run python scripts/ipynb-to-md.py "$(NOTEBOOK)" --name-mode exact
	@paths_file=$$(mktemp); \
	printf '%s\n' "memory/bookmarks/md/$$(basename "$(NOTEBOOK)" .ipynb).md" > "$$paths_file"; \
	$(MAKE) base-md-sync PATHS_FILE="$$paths_file"; \
	rm -f "$$paths_file"

convert-main:
	uv run python scripts/ipynb-to-md.py "notebooks/05 - Main.ipynb" --output-dir memory/bookmarks/md --name-mode exact
	@paths_file=$$(mktemp); \
	printf '%s\n' "memory/bookmarks/md/05 - Main.md" > "$$paths_file"; \
	$(MAKE) base-md-sync PATHS_FILE="$$paths_file"; \
	rm -f "$$paths_file"

convert-notebooks:
	uv run python scripts/ipynb-to-md.py notebooks --output-dir memory/bookmarks/md --name-mode exact
	$(MAKE) base-md-sync

tabs-sync:
	@test -n "$(NOTEBOOK)" || (echo "NOTEBOOK is required" && exit 1)
	python3 scripts/chrome_tabs_sync.py "$(NOTEBOOK)"

snapshots-sync:
	python3 scripts/snapshots_sync.py

base-md-sync:
	uv run python scripts/base_md_sync.py $(if $(PATHS_FILE),--paths-file "$(PATHS_FILE)",) $(PATHS)
	$(MAKE) wiki-ingest

wiki-ingest:
	uv run python scripts/wiki-ingest.py scan
