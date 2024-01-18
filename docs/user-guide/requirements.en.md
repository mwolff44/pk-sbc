# Requirements

P-KISS-SBC uses __Docker containers__ to run and supports all infrastructures that support containers.

Automated deployment uses docker compose, but kubernetes will be supported in the near future.

So, the only thing you need to install P-KISS-SBC is a server with Docker and docker compose installed.

!!! Tip "HowTo install Docker ?"

    To install docker and docker compose on debian, follow this guide : [https://docs.docker.com/engine/install/debian/](https://docs.docker.com/engine/install/debian/)

The server must have a __CPU with x86_64__ and support for SSE 4.2 or equivalent NEON instructions.

We recommend using a minimum of 2 vcpu and 2GB of RAM but the requirements will depend on your VoIP traffic in terms of concurrent calls and new calls per second.
