<div align="center">

<img src="./docs/logo.png" alt="Wand" width="300"/>

**Wand is yet another open-source ActivityPub relay, in Python. 😘**

----

[![codecov](https://codecov.io/github/mattholy/wand/graph/badge.svg?token=E9FLI822U9)](https://codecov.io/github/mattholy/wand)

----

[🇬🇧English](README.md) | [🇨🇳中文](README_zh-CN.md)

----

<img src="./docs/fedi.png" height="100"/>

</div>

----

<div>

## Philosophy & Features

### Connecting through the Fediverse



</div>



<div style="clear: both;"></div>

## Getting Start
ActivityPUB **need** to connect through https while Wand is a naive python ASGI.

So you have to deploy a [TLS Termination Proxy](https://en.wikipedia.org/wiki/TLS_termination_proxy) server in front of Wand. There are several choice:
- Traefik
- Caddy
- Nginx
- HAProxy
- Cloudflare Tunnel

### Docker Compose (Recommended)
Use a `docker-compose.yml` to deploy wand, recommended file as follow (**Change environment for your own !**) :
```yaml
version: "3.8"
services:
  wand:
    image: mattholy/wand:latest
    hostname: wand
    container_name: Wand
    # ports:
    #   - 80:80
    # We don't need ports forwarding this time
    volumes:
      - /etc/timezone:/etc/timezone:ro
      - /etc/localtime:/etc/localtime:ro
    environment:
      - WD_SERVER_URL=your.domain.name # Change this for your own
      - WD_REDIS_SERVER=redis
      - WD_REDIS_PORT=6379 # Optional, default is 6379
      - WD_REDIS_PWD=redis # Optional, default is None
      - WD_POSTGRES_SERVER=wand-postgres
      - WD_POSTGRES_PORT=5432 # Optional, default is 5432
      - WD_POSTGRES_DBNAME=wand # Change this for your own
      - WD_POSTGRES_USER=wand # Change this for your own
      - WD_POSTGRES_PWD=wand # Change this for your own
    restart: always
    depends_on:
      - wand-redis
      - wand-postgres

  wand-redis:
    image: redis
    hostname: wand-redis
    container_name: Wand-Redis
    volumes:
      - /etc/timezone:/etc/timezone:ro
      - /etc/localtime:/etc/localtime:ro
      - ./data/redis:/data # This is where your data stored
      - ./data/redis.conf:/usr/local/etc/redis/redis.conf
    command: ["redis-server","/usr/local/etc/redis/redis.conf"]
    # ports:
    #   - 6379:6379
    # We don't need ports forwarding this time
    restart: always

  wand-postgres:
    image: postgres
    hostname: wand-postgres
    container_name: Wand-Postgres
    volumes:
      - /etc/timezone:/etc/timezone:ro
      - /etc/localtime:/etc/localtime:ro
      - ./data/db:/var/lib/postgresql/data # This is where your data stored
    environment:
      POSTGRES_USER: wand # Change this for your own
      POSTGRES_DB: wand # Change this for your own
      POSTGRES_PASSWORD: wand # Change this for your own
    # ports:
    #   - 5432:5432
    # We don't need ports forwarding this time
    restart: always
```
And my `./data/redis.conf` looks like :
```
appendonly yes
```

Then run `docker compsoe up -d` to start your service.

Finally, access `https://your.domain.name` to configure further options.
#### GPG Key
*You can pass this section if you know this already.*

Wand uses GPG instead of username/password to identify you as the server administrator.
GPG is a modern identity verify system, to learn more about it see this [link](https://gnupg.org/)

For the green hand, there is a short guide.

- Install GPG from [https://gnupg.org/download/index.html](https://gnupg.org/download/index.html)
- Generate your GPG key by running command `gpg --full-gen-key` and follow the instructions promoted
- [Optinal] Send your GPG public key to a keyserver `gpg --send-keys [your key id]`
- Export your public key `gpg --export -a [your key id] > publickey.asc`
- The `publickey.asc` is your gpg public key. It is safe to share with Wand and anywhere else you like (e.g. Github)
- Be make sure to store your private key in a safe place (e.g. YubiKey)

## Dev & Contribute
Just clone this repo.

### Frontend
- `cd service/frontend/wand-zero`
- `npm install`
- `npm run dev`
### Backend
- `cd service/backend`
- `pip install -r requirements.txt`
- `python run_dev.py`

## Future Plan & Request
- See to Issues

