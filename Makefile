init::
	git init
	uv sync
	uv run pre-commit install

upgrade::
	uv lock --upgrade
	uv sync
