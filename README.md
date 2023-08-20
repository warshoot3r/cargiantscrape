# cargiantscrape
pythonised scraping car giant for models and prices. Sends a report via telegram.

[![Build and Push as individual tags as *-latest](https://github.com/warshoot3r/cargiantscrape/actions/workflows/build-master-branch(individual).yml/badge.svg)](https://github.com/warshoot3r/cargiantscrape/actions/workflows/build-master-branch(individual).yml)
[![Build and Push as latest](https://github.com/warshoot3r/cargiantscrape/actions/workflows/build-master-branch(singletag).yml/badge.svg)](https://github.com/warshoot3r/cargiantscrape/actions/workflows/build-master-branch(singletag).yml)
[![Test Containers](https://github.com/warshoot3r/cargiantscrape/actions/workflows/test-master-branch.yml/badge.svg)](https://github.com/warshoot3r/cargiantscrape/actions/workflows/test-master-branch.yml)

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