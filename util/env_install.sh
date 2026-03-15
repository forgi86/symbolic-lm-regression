# 1. Install uv (if you haven't yet)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Install a managed CPython (e.g., 3.13)
uv python install 3.12

# 3. Create a project environment
uv venv --python 3.12
source .venv/bin/activate

uv pip install -r requirements.txt