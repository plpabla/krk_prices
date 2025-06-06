# Status

[![Node](https://github.com/plpabla/krk_prices/actions/workflows/frontent-build.yml/badge.svg)](https://github.com/plpabla/krk_prices/actions/workflows/frontent-build.yml)

# Setup

Note: this procedure describe how to build all artifacts on the server. In the future we might want to use docker images from the registry, not to build them locally

## Prerequisite

- Linux server
- Package manager
- Installed Docker with docker-compose (for Mikrus server you can run `/root/noobs/scripts/chce_dockera.sh` script :)
  )

## Repo setup

- add SSH key to be able to pull the repo

```
$ ssh-keygen -t ed25519 -C "email"
$ eval "$(ssh-agent -s)"
$ ssh-add ~/.ssh/key
$ cat key.pub
```

Next, add it to a github

- clone repo

```
$ git clone git@github.com:plpabla/krk_prices.git
```

- install required tools

```
# apt install python3-pip
# pip install uv
```

- create `uv` project - to choose correct Python platform - use `uv python list` to get available ones

```
# uv python install cpython-3.12.10-linux-x86_64-gnu
# uv init -p 3.12
```

- activate virtual environment

```
# source .venv/bin/activate
```

- install all required files

```
# uv add -r requirements.txt
# uv sync
```

Note: we need to use `uv init` as the project was initially created with `venv` (I was not aware that `uv` exists)

## Use scrapper

```
# cd scrapper
# uv run scrapper.py --output ../model/data/krakow.csv --pages 100
```

## Build ML model

In the future we will download the model from remote repository.

- preprocess data (in repo, you have `krakow.csv` file)

```
# cd model/src
# uv run python preprocessing_pipeline.py krakow
# uv run python train_model.py
# uv run python train_model.py krakow
```

## Docker

- build images

```
# docker-compose build
```

- run

```
# docker-compose up -d
```

## nginx

We need a reverse proxy as our app is exposed on port `8080`.

If you are lazy though (and don't care about security) you can always edit `docker-compose.yaml` to route for port 80.

- install

```
# apt install nginx
```

- setup `/etc/nginx/sites-available/default`

```
server {
        listen 80 default_server;
        listen [::]:80 default_server;
        server_name wycenappka.pl;

        location / {
                proxy_set_header Host $host;
                proxy_set_header X-Forwarded-For $remote_addr;
                proxy_pass http://localhost:8080;
        }
}
```

- restart service

```
# systemctl reload nginx
```

# Connect domain for Mikrus

Mikrus doesn't provide fixed IPv4 so we need to use e.g. Cloudflare to route from IPv6

## Get IP

- Log in into your server - you'll get info about currently asssigned IPv4 (ephernal) and fixe IPv6

```
Welcome to Ubuntu 22.04.5 LTS (GNU/Linux 5.15.158-2-pve x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

           _ _
 _ __ ___ (_) | ___ __ _   _ ___
| '_ ` _ \| | |/ / '__| | | / __|
| | | | | | |   <| |  | |_| \__ \  Serwery dla ludzi z pasją.
|_| |_| |_|_|_|\_\_|   \__,_|___/


Twoje porty TCP/UDP:
 -  :20277 = <ipv4>:<port1>
 -  :30277 = <ipv4>:<port2>

Twoj adres IPv6: <ipv6>
```

## Check

Note: to check if you site is available without a domain (to make sure that you set up nginx and app correctly)

- modify `docker-compose.yaml` to be exposed at the port you have assigned (see baner above), e.g. `20277`
- connect over `https://<ipv4>:<port1>`

## Setup

Domain should be already on Cloudflare

- go to DNS/Records
- add following records
  - `AAAA` for `www` with IPv6 of your server and proxy enabled
  - `AAAA` for `wycenappka.pl` with IPv6 of your server and proxy enabled

# Remote development

Manual so far:

- clone repo

- prepare env

  $ pip install -r requirements.txt
  $ cd model/src
  $ python preprocessing_pipeline.py krakow
  $ python train_model.py krakow

Alternatively, use scp

$ scp -P 10277 krakow_model.pkl <remote>

- prepare container

  $ docker compose build
  $ docker compose up

If no errors are in console, kill it (Ctrl+C) and run in detached mode

    $ docker compose up -d
