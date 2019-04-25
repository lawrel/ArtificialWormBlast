# ArtificialWormBlast
There's something special in the Monster.
### New Note: before viewing Monster's Ink Page, in your browser go to settings>advanced>clear browsing history>clear cached data and then refresh the page
## Markdown Cheatsheet
Markdown is quite useful for making quick documentation in GitHub. This is useful for You can find it [here](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)

## Setting Up Your Development Environment
This project requires the following pieces to run:
- Python/Flask web-application
- MySQL database

### MySQL Database
The team utilized MySQL, to handle our account and card storage. To deploy your own install of Monsters Ink you will need a to install your own MySQL database.

1. Install mysql database.
2. Deploy the initial database schema. Run `database/schema/MonsterCards_Db_Schema.sql` on your database. This creates the MonsterCards database and the database tables. On linux we used:
```
mysql --user <admin> --host <ip-addr> -p < MonsterCards_Db_Schema.sql
```
3. Create the database-user accounts. Run `database/credentials/create_db_users.sql` on your database. This creates the MonsterCardsDev user. On linux we used:
```
mysql --user <admin> --host <ip-addr> -p < database/credentials/create_db_users.sql
```

### Python/Flask Web-Application
Requirements:
- Our [repo](https://github.com/lawrel/ArtificialWormBlast/)
- Python3.7
- Pip package manager(installed in your default python3.7 environment)

We're using Pipenv to manage our dependencies. Setting up a new pipenv environment is easy.
```
# Install pipenv
python -m pip install pipenv

# Navagate to the project folder
cd repos/ArtificialWormBlast/

# Create env and install packages in pipfile
pipenv install

# Enter env
pipenv shell

# Run application
python run.py
```

### Docker Container (Optional)
Requirements:
- Our [repo](https://github.com/lawrel/ArtificialWormBlast/)
- Docker

```
# Navagate to the project folder
cd repos/ArtificialWormBlast

# Create a docker network
docker network create mcnet

# Build docker image
docker build -t monstercards-dev:latest .

# Run docker image
docker run -d --net mcnet monstercards:latest

# Get your container name
docker ps

# Find the ip of your container
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' container_name
```
Once you have the ip address, use a browser to test your connection (i.e. http://<ip-addr>:8000).

#### What You'll Need
1. [Logmein Hamachi](https://www.vpn.net/)
2. [MySQL Workbench](https://dev.mysql.com/downloads/workbench/)

#### Loggin Into Database -- MySQL Workbench
1. Find the IP address assigned by the Hamachi for the machine 'happy-box'.
2. Select **Connect to Database** in MySQL Workbench.
3. Enter the IP address for 'happy-box' into the **Hostname** field. Leave the port alone (default 3306).
4. Enter user login credentials (if you leave **Password** field empty you will be prompted to enter it).
