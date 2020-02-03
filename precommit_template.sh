source .venv/bin/activate
pytest tests/
flake8
black -S --check --config=pyproject.toml .