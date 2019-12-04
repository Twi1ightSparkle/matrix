#!/bin/bash
now=$(date +"%Y.%m.%d-%H.%M.%S-%Z")
month=$(date +"%Y.%m")

sudo -u postgres pg_dump -U postgres synapse > /mnt/matrix-data/postgres/postgres_backup.bak

GZIP=-9 tar -czf /mnt/matrix-data/postgres/synapse.db_$now.tar.gz /mnt/matrix-data/postgres/postgres_backup.bak
gpg --encrypt --yes --no-tty --trust-model always --recipient user@domain.com /mnt/matrix-data/postgres/synapse.db_$now.tar.gz
mv /mnt/matrix-data/postgres/synapse.db_$now.tar.gz.gpg /tmp/

jotta-cli archive /tmp/synapse.db_$now.tar.gz.gpg --remote /matrix/postgres/$month/ --nogui

rm /mnt/matrix-data/postgres/postgres_backup.bak
rm /mnt/matrix-data/postgres/synapse.db_$now.tar.gz
rm /tmp/synapse.db_$now.tar.gz.gpg