# cargiantscrape
pythonised scraping car giant for models and prices. Sends a report via telegram.

[![Build and push multi tag as branch name](https://github.com/warshoot3r/cargiantscrape/actions/workflows/build-master.yml/badge.svg)](https://github.com/warshoot3r/cargiantscrape/actions/workflows/build-master.yml)
[![Build master as single tags and push as latest](https://github.com/warshoot3r/cargiantscrape/actions/workflows/build-master-singletags.yml/badge.svg)](https://github.com/warshoot3r/cargiantscrape/actions/workflows/build-master-singletags.yml)
[![Manual Build and push](https://github.com/warshoot3r/cargiantscrape/actions/workflows/build-feature-branch.yml/badge.svg)](https://github.com/warshoot3r/cargiantscrape/actions/workflows/build-feature-branch.yml)
[![Test Containers - Build and push multi tag as branch name](https://github.com/warshoot3r/cargiantscrape/actions/workflows/test-master.yml/badge.svg)](https://github.com/warshoot3r/cargiantscrape/actions/workflows/test-master.yml)
# Compatibility 
Should run on anything. Run in a docker isolated env
tested on:
ubuntu amd64
pi4 aarch64


# Container Install

install docker and docker-compose on linux distro

clone the git repo
```
git clone https://github.com/warshoot3r/cargiantscrape.git
```
cd folder
```
cd cargiantscrape
```
Create a credentials.py
```
echo 'api_token = "" \nchat_id = ""' >> credentials.py
```

create an empty used_cars.db file
```
touch used_cars.db
```
Run the docker container
```
docker compose pull && docker compose up -d 
```


# Manually Running
Run chatbot_autorun.py for terminal output of car scrape and telegram sending the report


# Todo:
scheduled telegram webhook which requires https ssl and code so that bot runs forever

Grabbing the MOT history of cars

telegram chat commands for on-demand scrape. eg. on demand spec search for a specific reg

tidy up the dockerfile and speed up the build. pandas take a long time to build

Delete old cars from DB if not being pulled when scraped

# updating requirements.txt
`
pip install pip-tools
pip-compile packages.txt 
`