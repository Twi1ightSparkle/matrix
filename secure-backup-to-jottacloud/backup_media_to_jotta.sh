#!/bin/bash
now=$(date +"%Y.%m.%d-%H.%M.%S-%Z")
month=$(date +"%Y.%m")
mkdir /mnt/matrix-data/media_backup/media/

if [ -n "$1" ]
then
	case "$1" in
		-f)
			find /mnt/matrix-data/synapse/media_store/ -type f -exec cp --parents {} /mnt/matrix-data/media_backup/media/ \;
			;;
		-h)
			echo "	-f		First run. Backups all media and not just the last 65 minutes.
	-h		Help."
			;;
		*)
			echo "Option $1 not recognized"
			;;
	esac
else
	find /mnt/matrix-data/synapse/media_store/ -mmin -65 -type f -exec cp --parents {} /mnt/matrix-data/media_backup/media/ \;
fi

GZIP=-9 tar -czf /mnt/matrix-data/media_backup/synapse_media_$now.tar.gz /mnt/matrix-data/media_backup/media/
gpg --encrypt --yes --no-tty --trust-model always --recipient user@domain.tld /mnt/matrix-data/media_backup/synapse_media_$now.tar.gz
mv /mnt/matrix-data/media_backup/synapse_media_$now.tar.gz.gpg /tmp/

jotta-cli archive /tmp/synapse_media_$now.tar.gz.gpg --remote /matrix/media/$month/ --nogui

rm -r /mnt/matrix-data/media_backup/*
rm /tmp/synapse_media_$now.tar.gz.gpg