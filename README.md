# ArtificialWormBlast
There's something special in the Monster.
### New Note: before viewing Monster's Ink Page, in your browser go to settings>advanced>clear browsing history>clear cached data and then refresh the page
## Markdown Cheatsheet
Markdown is quite useful for making quick documentation in GitHub. This is useful for You can find it [here](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)

## Setting Up Your Development Environment
There are a few prereqs which you'll need to access 

### LogMeIn Hamachi
Download it [here](https://www.vpn.net/).

This VPN service is free to download and use. You shouldn't need a password (at least for Linux users), though Windows users may be asked to login with their LogMeIn account before being used. We can find a workaround so we don't need LogMeIn accounts.

Free users are granted:
1. Unlimited networks
2. Max of 5 connections per network

#### New Connection to 'happy-box-2' Network
For Mac/Windows GUI Users:
1. Press the power/login button to come online. You should see your computer will try to connect to all networks you belong to.
2. Either press the **Join New Network** button, or use the menubar and click **Networks**/**Join New Network**.
3. Enter the networkid **'happy-box-2'** and the network password (ask Sean).

For Linux Users:
1. You can install a frontend GUI called **Haguichi** which provides a near-identical experience to the Mac/Windows clients.
2. Or TBD

Now you have network access to all computers logged in to the network. You can now see the IPv4/IPv6 addresses for each computer on the network, including 'happy-box'. Go ahead and `ping <IP for happy-box>` and make sure everything is working.


### MySQL Database
We can use MySQL, which is currently supported by Oracle, to handle our databasing needs. It supports most basic SQL syntax you may have seen, but also features it's own custom syntax for some specific operations.

Sean is currently running a MySQL database server on his home machine named 'happy-box'. He can set you up with an account and grant the neccessary access to the development database. 

**The development database is currently not setup and its schema is TBD.**

#### What You'll Need
1. [Logmein Hamachi](https://www.vpn.net/)
2. [MySQL Workbench](https://dev.mysql.com/downloads/workbench/)

#### Loggin Into Database -- MySQL Workbench
1. Find the IP address assigned by the Hamachi for the machine 'happy-box'.
2. Select **Connect to Database** in MySQL Workbench.
3. Enter the IP address for 'happy-box' into the **Hostname** field. Leave the port alone (default 3306).
4. Enter user login credentials (if you leave **Password** field empty you will be prompted to enter it).
