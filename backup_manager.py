import sys
import shutil
from pathlib import Path
from datetime import datetime

# Check arguments
if len(sys.argv) != 3:
    print("Usage: python backup_manager.py ./data ./backups")
    sys.exit(1)

source_dir = Path(sys.argv[1])
backup_dir = Path(sys.argv[2])

backup_dir.mkdir(parents=True, exist_ok=True)

# Supported file types
extensions = [".csv", ".json"]

log_file = Path("backup_log.txt")

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")


def log(message):
    with open(log_file, "a") as f:
        f.write(f"{datetime.now().isoformat()} - {message}\n")


for file in source_dir.iterdir():

    if file.suffix.lower() in extensions and file.is_file():

        new_name = f"{file.stem}_{timestamp}{file.suffix}"
        dest_file = backup_dir / new_name

        shutil.copy2(file, dest_file)

        log(f"BACKUP CREATED: {file.name} -> {new_name}")

        # Rotation logic
        pattern = f"{file.stem}_*{file.suffix}"
        backups = sorted(
            backup_dir.glob(pattern),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )

        if len(backups) > 5:
            for old_backup in backups[5:]:
                old_backup.unlink()
                log(f"OLD BACKUP DELETED: {old_backup.name}")

print("Backup completed successfully.")