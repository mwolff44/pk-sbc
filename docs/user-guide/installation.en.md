# One-Step Automated Install

Those who want to get started quickly and conveniently may install Pi-hole using the following command:

```bash
curl -sSL https://install.pyfreebilling.com | bash
```

<!-- markdownlint-disable code-block-style -->
!!! info
    Piping to `bash` is a controversial topic, as it prevents you from reading code that is about to run on your system.

    If you would prefer to review the code before installation, we provide these alternative installation methods.
<!-- markdownlint-enable code-block-style -->

## Alternative 1: Clone our repository and run

```bash
git clone --depth 1 https://github.com/mwolff44/pyfreebilling.git pyfreebilling
cd "src/"
bash basic-install.sh
```

## Alternative 2: Manually download the installer and run

```bash
wget -O basic-install.sh https://install.pyfreebilling.com
bash basic-install.sh
```
