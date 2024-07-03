<!---
# P-KISS-SBC documentation © 2007-2024 by Mathias WOLFF 
# is licensed under Attribution-NonCommercial-ShareAlike 4.0 International (see https://creativecommons.org/licenses/by-nc-sa/4.0/)
# SPDX-License-Identifier: CC-BY-NC-SA-4.0
--->

# Backup and Recovery

Thanks to the P-KISS-SBC architecture, backups are simple.
All the settings are held in one single file `.env` and the configuration in a single directory `/srv/db`.

!!! Warning

    If you are not using the default DB, PostgreSQL, you need to use specific tools for backup and recovery.

In vast majority of cases, this file and directory can be used to restore a system to a fully working state identical to what was running previously.

## Backup Strategies

The optimal backup strategy can be summarized in 3 points :

* Take frequent backup (automatic ones are the best)
* Keep multiple copies of backups in a safe location off the system
* Periodically test the backups

## Project layout

The root directory is /srv/pks .

    .env    # The configuration file.
    redis/  # The redis directory.
    db/     # The database directory.
