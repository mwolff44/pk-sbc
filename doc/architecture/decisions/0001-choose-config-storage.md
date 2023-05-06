# 0001 - Choose Config storage backend

- 📅 Date: 2nd of April 2024
- 🚧 Status: Accepted
- 👷 Authors: Mathias WOLFF
- ❗ spdx-license: CC BY-SA 4.0


## Context

The management interface exploits APIs from the administration microservice. 
This microservice relies on a data source to store configuration items. 

We need to define which system to use to store this data.

Note that these APIs are not used for call routing decision but only for configuration management. 

Performance is not an important criterion. The configuration items do not represent large data volumes (call logs will not be stored).

The choice of storage should follow the principles of the project, be KISS!

Backup and restoration should be easy.

Finally, it must be compatible with the functioning of a container-based architecture like K8S!

## Considered options 💡

We will consider 2 popular free DBMS systems: PostgreSQL and SQLite.

1. PostgreSQL: 
    - ✅ **Advantage:** performance, high concurrency, high volume
    - 🚫 **Disadvantage:** more complex to deploy, administrate and upgrade. Need a specific container.
2. SQLite: 
    - ✅ **Advantage:** simpler to deply (a simple volume). Backup and restore are easy.
    - 🚫 **Disadvantage:** no server / client

 
## Advices 

Other DBMS systems exist that are both popular, free and relevant to this project. However, expertise is also a criterion of choice, as well as the support of the tools already chosen and used.
You can check this interesting page for a checklist for choosing the right database engine : https://sqlite.org/whentouse.html

## Decision 🏆

The choice was made to use SQLite because of the simplicity of deployment and administration. Despite the undeniable added value of PostgreSQL, given the complexity involved, the project has no interest in using it.
It should be noted that a future migration will still be possible, as the DBMS connection tool supports both solutions.

## Consequences 

SQLite will be used to store the configurations.

♻️ Update: nil.