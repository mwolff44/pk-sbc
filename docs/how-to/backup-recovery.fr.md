<!---
# P-KISS-SBC documentation © 2007-2024 by Mathias WOLFF 
# is licensed under Attribution-NonCommercial-ShareAlike 4.0 International (see https://creativecommons.org/licenses/by-nc-sa/4.0/)
# SPDX-License-Identifier: CC-BY-NC-SA-4.0
--->

# Sauvegarde et Restauration

Grâce à l'architecture P-KISS-SBC, les sauvegardes sont simples.
Tous les paramètres sont conservés dans un seul fichier `.env` et la configuration dans un seul répertoire `/srv/db`.

!!! Warning

    Si vous n'utilisez pas la base de données par défaut, et que vous utilisez MySQL, MariaDB ou PostgreSQL, vous devez utiliser des outils spécifiques pour la sauvegarde et la restauration.

Dans la grande majorité des cas, ce fichier et ce répertoire peuvent être utilisés pour restaurer un système dans un état de fonctionnement identique à ce qui fonctionnait auparavant.

## Stratégies de sauvegarde

La stratégie de sauvegarde optimale peut être résumée en 3 points :

* Effectuer des sauvegardes fréquentes (les sauvegardes automatiques sont les meilleures).
* Conserver plusieurs copies des sauvegardes dans un endroit sûr en dehors du système.
* Tester périodiquement les sauvegardes

## Disposition des données du projet

Le répertoire principal est /srv/pks .

    .env    # Le fichier de configuration.
    redis/  # Le dossier redis.
    db/     # Le dossier de la base de données.
