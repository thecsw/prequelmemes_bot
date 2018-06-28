
#!/bin/bash
_now=$(date +"%m_%d_%Y")
_file="/data/prequelmemes_bot/backups/backup_$_now.sql"
echo "Starting backup to $_file..."
docker-compose run --rm postgres pg_dump -h HOST_NAME -p PORT -d DATABASE_NAME -U USERNAME -W -f "$_file"
