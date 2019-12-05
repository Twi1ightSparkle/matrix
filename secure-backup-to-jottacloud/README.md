# Secure backup of Synapse database and media to Jottacloud

**I take no responsibility if this in any way breaks your stuff or restore does not work. Test thoroughly to make sure it works in your environment.**

Securely backup Synapse to Jottacloud. A cheap cloud storage provider with unlimited (upload speed reduced after 5 TB) storage.  
https://www.jottacloud.com/en/  
https://docs.jottacloud.com/en/articles/3271114-reduced-upload-speed

## Setup

### Install Jottacloud
https://docs.jottacloud.com/en/articles/1436855-jottacloud-cli-for-linux-debian-packages  
jotta-cli login

### Create PGP keys
#### On your PC:
```
gpg --full-generate-key
1
4096
0
y
<your name>
<some email address>  # Does not have to be a real email. Only used for selecting the right key when automatically encrypting.  
<no comment>
o
<pass phrase>
gpg --list-keys
gpg --output matrix-backup-public.gpg --armor --export <key ID>
gpg --output matrix-backup-private.gpg --armor --export-secret-key <key ID>
```

Copy `matrix-backup-public.gpg` to the Synapse server.  
Save both keys and the password somewhere secure, then delete them from your local machine. Don't lose them as your backup will be impossible to access without the password and private key.

#### On server:
```
gpg --import matrix-backup-public.gpg
gpg --list-keys
rm matrix-backup-public.gpg
```

#### Other useful commands:
```
gpg --decrypt-files /path/to/file
gpg --delete-key ID
gpg --delete-secret-key ID
gpg --delete-secret-and-public-key ID
```

#### Import secret key and trust ultimate:
For importing the private key if you get a new machine. Need to be done before decrypting.
```
gpg --import private.key
gpg --edit-key {KEY ID} trust quit
5
y
gpg --list-keys
```

## backup_db_to_jotta.sh
Export, encrypt and back up the PostgreSQL database to Jottacloud.  
Change paths to reflect your setup.

## backup_media_to_jotta.sh
Encrypt and back all media files to Jottacloud.  
By default it takes all files created in the last 65 minutes. The extra five minutes are to make sure no files are missed.  
The first time you'll want to run the script manually with the -f option. This backs up all media files, not just those create in the last hour.  
Change paths to reflect your setup.

## Schedule things
As root: `crontab -e`  
Add  
```
0  *	* * *	/root/backup_db_to_jotta.sh  # Backup Synapse database every hour on the dot.
10  *	* * *	/root/backup_media_to_jotta.sh  # Backup new Synapse media files since last backup ten minutes past every hour.
```  

Media is backed up ten past every hour to lessen the resource use by not doing both simultaneously.

## Restore
Create user with same name as before  
`psql -U <username> -f /path/to/postgres_backup.bak`
