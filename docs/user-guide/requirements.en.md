# Requirements

P-KISS-SBC uses __Docker containers__ to run and supports all infrastructures that support containers.

Automated deployment uses docker compose, but kubernetes will be supported in the near future.

So, the only thing you need to install P-KISS-SBC is a server with Docker and docker compose installed.

!!! Tip "HowTo install Docker ?"

    To install docker and docker compose on debian, follow this guide : [https://docs.docker.com/engine/install/debian/](https://docs.docker.com/engine/install/debian/)

## Supported Operating Systems

The one-step automated install script can be used with limited operating system.

The following operating systems are __officially__ supported:

| Distribution | Release          | Architecture        |
| ------------ | ---------------- | ------------------- |
| DietPi   | v8.xx | x86_64 |
| Ubuntu | 22.04 | x86_64 |
| Debian | 12 | x86_64 |

!!! Note "Deploy to another OS
    It is perfectly possible to deploy PKS on another OS. The prerequisites will have to be installed manually!

## VM sizing

The server must have a __CPU with x86_64__ and support for SSE 4.2 or equivalent NEON instructions.

We recommend using a __minimum of 2 vcpu and 2GB of RAM__ but the requirements will depend on your VoIP traffic in terms of concurrent calls and new calls per second.

!!! warning "Dedicated resources"
    It is important not to forget that PKS will be processing pseudo-real-time flows (VoIP). It is therefore essential to __dedicate__ hardware resources__ (CPU and RAM) to PKS. Over-allocation must be avoided, as this will result in degraded audio quality.
    Even if writes are not critical, as PKS does not use a database, you must ensure that disk accesses are fast enough.

## Network

### Quality

VoIP requires a __network__ of good size and __quality__. Media flows must be __prioritised__ (by default `TOS 184` is defined).

!!! tip ""
    __Bandwidth reservation__ is also interesting to implement within your network equipment.

### IP addressing

PKS is deployed on a VM with __a single private IP address__. A __public IP address__ with the ports returned on this VM is __necessary__ (see list below).

!!! tip "2 public IP adresses"
    It is possible to have a different IP address for signalling than the media's public IP address.

### Network ports

PKS uses __2 different network ports__ for __signalling__ (UDP 5060 and UDP 5070) and a __range of predefined ports__ for __media__ (UDP 16384 to 16485).

These __parameters__ can be __modified__ to suit your needs, including the RTP port range to handle more concurrent calls.

!!! note "Web admin"
    In addition, if you are using PKS-Admin, the Web administration interface, TCP port 443 must be open.
