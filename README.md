# django-auth

A minimal django example for native user authentication.

```
# Install dependencies
sudo apt install -y python3-pip python3-venv

# Clone project
git clone https://github.com/nikhiljohn10/django-auth && cd django-auth

# Create Python virtial environment and activate it
python3 -m venv venv && . venv/bin/activate

# Install python dependencies
pip install -r requirements.txt

# Edit your changes in the project

# Start your postgresql server and configure settings.py accordingly

# Create migrations for django models
./manage.py migrate

# Create super user
./manage.py createsuperuser --username admin --email admin@localhost

# Run server
./manage.py runserver 0.0.0.0:8000
```

## Developing

To initialise `. ./init`

* `djr` - Run server
* `dje` - Reset project database
* `djp` - Dump data from database in to db.json
* `djm` - Migrate data
* `djx` - Deactivate virtual environment

## PostgreSQL

#### Setup PostgreSQL

Run PostgreSQL server on your system or use Docker (Instructions given in next section)

Uncomment `psycopg2==2.8.6` in `requirements.txt`

Uncomment `DATABASES` variable in `config/settings/custom.py` and edit the
username and password accordingly

Install dependencies using following commands:

```
# Update system
sudo apt update && sudo apt upgrade -y && sudo apt autoremove

# Install dependencies
sudo apt install -y libpq-dev python3-dev
pip install -r requirements.txt
```

#### DB on Docker

If you want a test database, best option is a docker container of postgresql.

Install Docker Engine using the guide in this [link](https://docs.docker.com/get-docker/)

Add the following code at the bottom of `~/.bashrc` if you are using Ubuntu or
`~/.zshrc` if you are using MacOS
```
function pg {
  case $1 in
  start )
    docker run \
      --name postgres_12_4 \
      -e POSTGRES_PASSWORD=postgres \
      -p 5432:5432 \
      -d postgres:12.4-alpine 2>/dev/null && \
    echo "PostgreSQL Container started" || \
    (docker restart postgres_12_4 && echo "PostgreSQL Container restarted")
    ;;
  stop )
    docker stop postgres_12_4 && \
    echo "PostgreSQL Container stopped"
    ;;
  kill )
    docker stop postgres_12_4 && \
    docker rm postgres_12_4 && \
    echo "PostgreSQL Container killed"
    ;;
  stats )
    docker stats postgres_12_4
    ;;
  * )
    echo "Invalid option. Available options: start|stop|kill|stats"
    ;;
  esac
}
complete -W 'start stop kill stats' pg 2>/dev/null || \
echo "Auto competition not available"
```

Now open a new terminal window and use the command `pg start` to start a new container
