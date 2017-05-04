pyfreebilling-install.sh
--------------------------------------

This install script that has been designed to be a simple way to to install PyFreeBilling. Start with a minimal install of Debian 8 with SSH enabled. Run the following commands under root. It installs PyFreeBilling release package and its dependencies, IPTables, Fail2ban, Apache, and PostgresQL.

```bash
wget https://raw.githubusercontent.com/mathias44w/pyfreebilling/master/install/install.sh -O install.sh && sh install.sh
```

At the end of the install it will instruct you to go to the ip address of the server in your web browser to finish the install. It will also provide a random database password for you to use during the web based phase of the install.

After you have completed the install you can login with the username and password you chose during the install.