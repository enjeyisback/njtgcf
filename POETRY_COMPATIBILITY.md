# Poetry Version Compatibility Guide

## Overview

This project uses Poetry for dependency management and is configured to be compatible with **Poetry 1.1.12 and above**, including the latest Poetry 2.x versions.

## Current Configuration

The `pyproject.toml` file is written in **Poetry 1.x format** using the `[tool.poetry]` section, which ensures maximum compatibility across different Poetry versions:

- ✅ **Poetry 1.1.12+**: Full support (native format)
- ✅ **Poetry 2.x**: Full support (backward compatible)

## Why Poetry 1.x Format?

While Poetry 2.x introduced support for the newer PEP 621 format with `[project]` sections, we deliberately use the Poetry 1.x format for several reasons:

1. **Backward Compatibility**: Poetry 1.1.12 and earlier versions only support `[tool.poetry]` format
2. **Wider Audience**: Many users still have Poetry 1.x installed
3. **Stability**: The Poetry 1.x format is mature and well-tested
4. **Forward Compatible**: Poetry 2.x fully supports the older format

## Expected Warnings in Poetry 2.x

If you're using Poetry 2.x, you may see deprecation warnings when running `poetry check`:

```
Warning: [tool.poetry.name] is deprecated. Use [project.name] instead.
Warning: [tool.poetry.version] is set but 'version' is not in [project.dynamic]...
Warning: [tool.poetry.description] is deprecated. Use [project.description] instead.
...
```

**These warnings are safe to ignore.** The configuration is fully functional and will work correctly with both Poetry 1.x and 2.x.

## Version Requirements

### Minimum Poetry Version: 1.1.12

To check your Poetry version:

```bash
poetry --version
```

### Upgrading Poetry

If you need to upgrade Poetry, you can do so using:

```bash
# For pipx installations (recommended)
pipx upgrade poetry

# For pip installations
pip install --upgrade poetry

# For official installer
curl -sSL https://install.python-poetry.org | python3 -
```

## Migrating to PEP 621 Format (Optional)

If you want to use the newer PEP 621 format with `[project]` sections:

1. **Requirement**: Poetry 1.2.0 or above
2. **Consider**: Breaking compatibility with Poetry versions < 1.2.0
3. **Documentation**: See [Poetry's migration guide](https://python-poetry.org/docs/pyproject/)

We recommend staying with the current format unless you have specific reasons to migrate and all team members are using Poetry 2.x.

## Dependency Version Constraints

The project uses the following version constraints:

- **Python**: `^3.10` (3.10 or above, but below 4.0)
- **Streamlit**: `^1.52.0` (1.52.0 or above, but below 2.0)
- **Telethon**: `^1.42.0` (1.42.0 or above, but below 2.0)

These constraints ensure compatibility while allowing automatic minor and patch updates.

## Troubleshooting

### Issue: "The Poetry configuration is invalid"

**Solution**: Ensure you're using Poetry 1.1.12 or above. The current `pyproject.toml` format is not compatible with older versions.

### Issue: Deprecation warnings in Poetry 2.x

**Solution**: These are informational warnings. The configuration works correctly. You can:
- Ignore them (recommended)
- Upgrade to PEP 621 format if you're sure all users have Poetry 2.x

### Issue: Lock file out of sync

**Solution**: Regenerate the lock file:

```bash
poetry lock
```

## Testing the Configuration

To verify your Poetry setup works correctly:

```bash
# 1. Check configuration validity
poetry check

# 2. Show resolved dependencies (dry run)
poetry install --dry-run

# 3. Install dependencies
poetry install

# 4. Run the application
poetry run tgcf-web
```

## Additional Resources

- [Poetry Documentation](https://python-poetry.org/docs/)
- [PEP 621 Specification](https://peps.python.org/pep-0621/)
- [Poetry 2.x Migration Guide](https://python-poetry.org/docs/pyproject/)

## Questions?

If you encounter issues with Poetry compatibility, please:
1. Check your Poetry version: `poetry --version`
2. Ensure you have at least Poetry 1.1.12
3. Review the troubleshooting section above
4. Open an issue on GitHub with your Poetry version and error message
