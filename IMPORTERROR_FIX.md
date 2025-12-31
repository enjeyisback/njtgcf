# ImportError Fix - switch_theme

## Issue
The TGCF web UI was showing an ImportError:
```
ImportError: cannot import name 'switch_theme' from 'tgcf.web_ui.utils'
```

This error occurred when trying to access the web UI at `http://localhost:8501`.

## Root Cause
The service was running from an old installation or location that didn't have the latest version of the code. The `switch_theme` function was present in the current codebase at `/home/ubuntu/github_repos/tgcf/tgcf/web_ui/utils.py` but the service was importing from an outdated package installation.

## Investigation
1. Verified that `switch_theme` function exists in `tgcf/web_ui/utils.py` (lines 58-71)
2. Confirmed the function is used in multiple files:
   - `0_👋_Hello.py`
   - All page files in `pages/` directory
3. Found that the service needed to be restarted from the correct location

## Solution
1. **Reinstalled the package** to ensure the latest code is used:
   ```bash
   cd /home/ubuntu/github_repos/tgcf
   poetry install
   ```

2. **Restarted the service** from the correct directory:
   ```bash
   ./tgcf-start.sh
   ```

3. **Verified the fix** by:
   - Checking service logs (no errors)
   - Opening the web UI in browser
   - Testing multiple pages (Hello, Telegram Login, Connections)
   - Confirming theme toggle (☀️/🌒) appears in sidebar

## Result
✅ The web UI is now fully functional and accessible at `http://localhost:8501`
✅ All pages load without ImportError
✅ Theme switching functionality works correctly
✅ No errors in service logs

## Files Involved
- `tgcf/web_ui/utils.py` - Contains `switch_theme()` function (lines 58-71)
- `tgcf/web_ui/0_👋_Hello.py` - Imports and uses `switch_theme()`
- All page files in `tgcf/web_ui/pages/` - Import and use `switch_theme()`

## Prevention
To avoid this issue in the future:
1. Always run the service from `/home/ubuntu/github_repos/tgcf/`
2. Use `poetry install` after pulling code updates
3. Use the provided service management scripts (`tgcf-start.sh`, `tgcf-stop.sh`)
4. Check logs immediately after starting service to catch any errors early

## Date
Fixed: December 31, 2025
