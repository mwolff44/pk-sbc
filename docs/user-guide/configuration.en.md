# Post Installation

Now that P-KISS-SBC is installed, we're going to connect our first SIP provider, our first IPBX and route calls from a DID to our IPBX and route calls from the IPBX to our SIP operator.

## Optional step

The *local* logging driver is recommended as it performs log-rotation by default, and uses a more efficient file format.
To configure the Docker daemon to default to a specific logging driver, set the value of log-driver to the name of the logging driver in the daemon.json /etc/docker/daemon.json

```bash
{
“log-driver”: “local”
}
```

Restart Docker for the changes to take effect

```bash
sudo systemctl restart docker.service
```

And to check

```bash
docker info --format '{{.LoggingDriver}}'
```

## Simple steps

    1. Create a SIP provider
    2. Route calls to our SIP provider
    2. Create an IPBX
    3. Add DIDs and route them to our IPBX