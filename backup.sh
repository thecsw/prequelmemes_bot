
#!/bin/bash
_now=$(date +"%m_%d_%Y")
_file="/data/prequelmemes_bot/backups/backup_$_now.sql"
echo "Starting backup to $_file..."
docker-compose run --rm postgres pg_dump -h postgres -p 5432 -d prequelmemes_db -U prequelmemer -W -f "$_file"
