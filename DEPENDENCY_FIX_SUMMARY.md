# Dependency Conflicts and Installation Fixes

## Summary
This document describes the dependency conflicts that were resolved and the installation improvements made to the TGCF project.

## Issues Identified

### 1. Dependency Version Conflicts
The project had several dependency version conflicts that prevented proper installation:

- **typer version conflict**: `tg-login` (0.0.4) requires `typer` (>=0.7.0,<0.8.0), but pyproject.toml specified `typer` ^0.20.0
- **python-dotenv version conflict**: `tg-login` (0.0.4) requires `python-dotenv` (>=0.21.0,<0.22.0), but pyproject.toml specified `python-dotenv` ^1.2.0
- **PackageNotFoundError**: The tgcf/__init__.py file didn't handle missing package metadata gracefully during editable installations

### 2. Installation Method Issues
- The start script used `pip install -e .` which could cause conflicts with poetry-managed dependencies
- No proper cleanup of existing installations before installing new versions
- The script didn't properly utilize Poetry for dependency management

### 3. Service Execution Issues
- The tmux session command didn't use `poetry run` to ensure the correct virtual environment

## Fixes Applied

### 1. Resolved Dependency Conflicts (pyproject.toml)

**Changed:**
```toml
# Before
typer = "^0.20.0"
python-dotenv = "^1.2.0"

# After
typer = "^0.7.0"
python-dotenv = "^0.21.0"
```

**Fixed deprecation warning:**
```toml
# Before
[tool.poetry.dev-dependencies]
black = {version = "^25.1.0", allow-prereleases = true}
isort = "^5.13.0"
pre-commit = "^4.1.0"

# After (merged into existing group)
[tool.poetry.group.dev.dependencies]
black = {version = "^25.1.0", allow-prereleases = true}
isort = "^5.13.0"
pre-commit = "^4.1.0"
ipykernel = "^6.29.0"
pylint = "^3.3.0"
pytest = "^8.3.0"
pytest-asyncio = "^0.24.0"
```

### 2. Enhanced Installation Logic (start script)

**Added Poetry check and auto-installation:**
```bash
# Check poetry
if ! command -v poetry &> /dev/null; then
    echo -e "${YELLOW}  ! Poetry not found, installing...${NC}"
    curl -sSL https://install.python-poetry.org | python3 - > /dev/null 2>&1
    export PATH="$HOME/.local/bin:$PATH"
fi
```

**Improved tgcf installation with conflict resolution:**
```bash
# Remove any existing pip-installed tgcf to avoid conflicts
pip uninstall -y tgcf > /dev/null 2>&1 || true

# Install dependencies using poetry
poetry install --no-dev --no-interaction > /dev/null 2>&1

# Fallback to pip if poetry fails
if [ $? -ne 0 ]; then
    pip uninstall -y tgcf > /dev/null 2>&1 || true
    pip install -e . --no-deps > /dev/null 2>&1
    pip install -e . > /dev/null 2>&1
fi
```

**Updated service start command:**
```bash
# Before
tmux new-session -d -s "$SESSION_NAME" "set -a; source .env; set +a; tgcf-web 2>&1 | tee -a $LOG_FILE"

# After
tmux new-session -d -s "$SESSION_NAME" "cd $PROJECT_DIR && set -a; source .env; set +a; poetry run tgcf-web 2>&1 | tee -a $LOG_FILE"
```

### 3. Fixed Package Metadata Handling (tgcf/__init__.py)

**Added graceful fallback for missing metadata:**
```python
# Before
from importlib.metadata import version
__version__ = version(__package__)

# After
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version(__package__)
except PackageNotFoundError:
    # Fallback for development/editable installs where metadata might not be available
    __version__ = "1.1.8"  # Should match version in pyproject.toml
```

### 4. Updated Management Scripts

**Updated tgcf-start.sh:**
```bash
# Before
tmux new-session -d -s "$TMUX_SESSION" -c "$TGCF_DIR" "tgcf-web 2>&1 | tee -a $LOG_FILE"

# After
tmux new-session -d -s "$TMUX_SESSION" -c "$TGCF_DIR" "poetry run tgcf-web 2>&1 | tee -a $LOG_FILE"
```

## Testing Results

After applying all fixes:

1. ✅ Poetry lock file regenerated successfully without conflicts
2. ✅ Dependencies installed cleanly via `poetry install`
3. ✅ Service starts successfully using `./start`
4. ✅ No deprecation warnings in logs
5. ✅ Web interface accessible at http://localhost:8501
6. ✅ Service management scripts (status, stop, restart) work correctly

## Files Modified

1. `start` - Enhanced installation logic and error handling
2. `tgcf-start.sh` - Updated to use poetry run
3. `pyproject.toml` - Fixed dependency versions and deprecation warnings
4. `tgcf/__init__.py` - Added graceful handling of missing package metadata
5. `poetry.lock` - Regenerated with resolved dependencies

## Installation Instructions

To use the fixed installation:

1. Navigate to the project directory:
   ```bash
   cd /home/ubuntu/github_repos/tgcf
   ```

2. Run the start script:
   ```bash
   ./start
   ```

The script will automatically:
- Check for and install Poetry if needed
- Clean up conflicting installations
- Install all dependencies via Poetry
- Start the service in a tmux session
- Verify the service is running

## Recommendations

1. **Always use Poetry** for dependency management in this project
2. **Run commands with `poetry run`** to ensure the correct environment
3. **Update poetry.lock** after any changes to pyproject.toml:
   ```bash
   poetry lock
   poetry install
   ```
4. **Avoid mixing pip and poetry** installations to prevent conflicts

## Notes

- The fixes maintain backward compatibility with existing workflows
- All management scripts continue to work as documented
- The start script now includes comprehensive error handling and fallback mechanisms
- Users can still pull changes from GitHub and run locally without issues
