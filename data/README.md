# TGCF Data Directory

This directory is used for persistent storage of TGCF data.

## Contents

- **Session files**: Telegram session files (*.session) are stored here to maintain authentication across restarts
- **Temporary files**: Any temporary files created during operation
- **Logs**: Additional log files if needed

## Permissions

This directory should be owned by the `ubuntu` user with 755 permissions to ensure the service can read and write data.

## Backup

It's recommended to backup this directory regularly, especially the session files, to avoid losing authentication.
