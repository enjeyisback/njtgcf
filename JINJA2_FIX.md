# Jinja2 Dependency Fix

## Problem
When running `tgcf-web` directly (not through poetry), the application failed with:
```
ImportError: Pandas requires version '3.1.2' or newer of 'jinja2' (version '3.0.3' currently installed)
```

## Root Cause
- Running `tgcf-web` directly uses the system pip installation
- The system pip had jinja2 3.0.3 installed
- Pandas requires jinja2 >= 3.1.2
- The poetry environment had the correct dependencies, but wasn't being used

## Solution Implemented

### 1. Added jinja2 to Dependencies
**File:** `pyproject.toml`
```toml
[tool.poetry.dependencies]
...
jinja2 = "^3.1.2"
```

This ensures that when poetry resolves dependencies, it will install jinja2 >= 3.1.2 to satisfy pandas requirements.

### 2. Verified Start Scripts Use Poetry
Both start scripts correctly use `poetry run`:
- `tgcf-start.sh`: Uses `poetry run tgcf-web`
- `start`: Uses `poetry run tgcf-web`

### 3. Updated Poetry Lock File
Regenerated `poetry.lock` with the new jinja2 requirement:
```bash
poetry lock
```

Result: jinja2 3.1.6 now installed in poetry environment

### 4. Updated Documentation
Added troubleshooting section in `USAGE_INSTRUCTIONS.md` explaining:
- The cause of dependency version errors
- Correct ways to run the application
- How to fix dependency issues

## How to Use

### Always Run Through Poetry
```bash
# Correct ways:
poetry run tgcf-web        # Direct execution
./tgcf-start.sh            # Start script
./start                    # Simple start script

# NEVER run directly:
tgcf-web                   # ❌ Uses system pip, may have wrong versions
```

### Fixing Dependency Issues
If you encounter dependency errors:
```bash
cd /home/ubuntu/github_repos/tgcf
poetry install             # Reinstall all dependencies
poetry lock                # Regenerate lock file if needed
```

## Testing Performed

1. ✅ Added jinja2 to pyproject.toml
2. ✅ Regenerated poetry.lock (jinja2 3.1.6 installed)
3. ✅ Verified jinja2 version in poetry environment
4. ✅ Confirmed pandas imports successfully
5. ✅ Tested `poetry run tgcf-web` - starts without errors
6. ✅ Tested `./tgcf-start.sh` - service starts correctly
7. ✅ Verified logs show no jinja2 import errors

## Prevention

To prevent similar issues in the future:
1. Always run TGCF through poetry: `poetry run tgcf-web`
2. Use the provided start scripts (`./start` or `./tgcf-start.sh`)
3. Don't install tgcf with system pip if using poetry
4. Keep poetry.lock file up to date

## Related Files
- `pyproject.toml` - Added jinja2 dependency
- `poetry.lock` - Updated with jinja2 3.1.6
- `USAGE_INSTRUCTIONS.md` - Added troubleshooting section
- `tgcf-start.sh` - Uses poetry run (already correct)
- `start` - Uses poetry run (already correct)

---
**Date:** December 31, 2025
**Status:** ✅ Fixed and Tested
