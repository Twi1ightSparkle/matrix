# Miscellaneous scripts for Matrix

Securely backup synapse to Jottacloud. A cheap cloud storage provider with unlimited (upload speed reduced after 5 TB) storage.  
https://www.jottacloud.com/en/  
https://docs.jottacloud.com/en/articles/3271114-reduced-upload-speed

## Setup

### Install Jottacloud
https://docs.jottacloud.com/en/articles/1436855-jottacloud-cli-for-linux-debian-packages  
jotta-cli login

### Create PGP keys
On your PC:  
`gpg --full-generate-key`  
`1`  
`4096`  
`0`  
`y`  
`<your name>`  
`<some email address>  # Does not have to be a real email. Only used for selecting the right key when automatically encrypting.`  
`<no comment>`  
`o`  
`<pass phrase>`  
`gpg --list-keys`  
`gpg --output matrix-backup-public.gpg --armor --export <key ID>`  
`gpg --output matrix-backup-private.gpg --armor --export-secret-key <key ID>`  

Copy matrix-backup-public.gpg to the Synapse server  
Save both keys somewhere secure, then delete them from tour local machine.

On server:  
`gpg --import matrix-backup-public.gpg`  
`gpg --list-keys`  
`rm matrix-backup-public.gpg`

Other useful commands:  
`gpg --decrypt-files /path/to/file`  
`gpg --delete-key ID`  
`gpg --delete-secret-key ID`  
`gpg --delete-secret-and-public-key ID`

Import secret key and trust ultimate:  
`gpg --import private.key`  
`gpg --edit-key {KEY ID} trust quit`  
`5`  
`y`  
`gpg --list-keys`

# backup_db_to_jotta.sh
Export, encrypt and back up the PostgreSQL database to Jottacloud.

# backup_media_to_jotta.sh
Encrypt and back all media files to Jottacloud.  
By default it take all files created the last 65 minutes. The extra five minutes to make sure no files are missed.  
The first time you want to run the script manuallt with the -f option. This backs up all media files, not just the last hour.
