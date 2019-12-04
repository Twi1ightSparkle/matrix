# Miscellaneous scripts for Matrix

Securely backup synapse to Jottacloud. A cheap cloud storage provider with unlimited (upload speed reduced after 5 TB) storage.  
https://www.jottacloud.com/en/

## Setup
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
enter 5<RETURN>  
enter y<RETURN>  
`gpg --list-keys`
