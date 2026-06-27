.PHONY: init convert convert-main convert-notebooks tabs-sync wiki-ingest

init:
	uv sync

convert:
	@test -n "$(NOTEBOOK)" || (echo "NOTEBOOK is required" && exit 1)
	uv run python scripts/ipynb-to-md.py "$(NOTEBOOK)" --name-mode exact --clone-to memory/llm-wiki/raw && uv run python scripts/wiki-ingest.py scan

convert-main:
	uv run python scripts/ipynb-to-md.py "notebooks/05 - DKT - Main.ipynb" --output-dir memory/bookmarks/md

convert-notebooks:
	uv run python scripts/ipynb-to-md.py notebooks --output-dir memory/bookmarks/md

tabs-sync:
	@test -n "$(NOTEBOOK)" || (echo "NOTEBOOK is required" && exit 1)
	python3 scripts/chrome_tabs_sync.py "$(NOTEBOOK)"

wiki-ingest:
	uv run python scripts/wiki-ingest.py scan
