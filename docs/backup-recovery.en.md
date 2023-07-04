# Backup and Recovery

Thanks to the P-KISS-SBC architecture, backups are simple.
All the settings are held in one single file `.env` and the configuration in a single directory `/srv/db`.

!!! Warning

    If you are not using the default DB, and using MySQL, MariaDB or PostgreSQL, you need to use specific tools for backup and recovery.

In vast majority of cases, this file and directory can be used to restore a system to a fully working state identical to what was running previously.

## Backup Strategies

The optimal backup strategy can be summarized in 3 points : 

* Take frequent backup (automatic ones are the best)
* Keep multiple copies of backups in a safe location off the system
* Periodically test the backups

