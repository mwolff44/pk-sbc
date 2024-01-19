# Doc : Testing your changes

When working on the documentation, it is advised that you review your changes locally before committing them. The `mkdocs serve` command can be used to live preview your changes (as you type) on your local machine.

Please make sure you fork the repo and change the clone URL in the example below for your fork:

- Linux Mint / Ubuntu 18.04 LTS / 19.10 / 20.04 LTS / 22.04 LTS:
    - Preparations (only required once):

    ```bash
    git clone https://github.com/YOUR-USERNAME/docs
    cd docs
    sudo apt install python3-pip
    pip3 install -r requirements-docs.txt
    ```

    - Running the docs server:

    ```bash
    mkdocs serve --dev-addr 0.0.0.0:8000
    ```

- Fedora Linux instructions (tested on Fedora Linux 28):
    - Preparations (only required once):

    ```bash
    git clone https://github.com/YOUR-USERNAME/docs
    cd docs
    pip install --user -r requirements-docs.txt
    ```

    - Running the docs server:

    ```bash
    mkdocs serve --dev-addr 0.0.0.0:8000
    ```

- Docker instructions:
    - One-shot run:

    ```bash
    docker run -v `pwd`:/opt/app/ -w /opt/app/ -p 8000:8000 -it nikolaik/python-nodejs:python3.7-nodejs16 \
      sh -c "pip install --user -r requirements-docs.txt && \
      /root/.local/bin/mkdocs build && \
      npm ci && \
      npm test && \
      /root/.local/bin/mkdocs serve --dev-addr 0.0.0.0:8000"
    ```

After these commands, the current branch is accessible through your favorite browser at <http://localhost:8000>