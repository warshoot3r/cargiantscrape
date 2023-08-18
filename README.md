# cargiantscrape
pythonised scraping car giant for models and prices. Sends a report via telegram.

[![Pull and run images from Docker Hub Workflow](https://github.com/warshoot3r/cargiantscrape/actions/workflows/pullandtestdockerimages.yml/badge.svg)](https://github.com/warshoot3r/cargiantscrape/actions/workflows/pullandtestdockerimages.yml)
[![Build and Push Cross-Platform Images](https://github.com/warshoot3r/cargiantscrape/actions/workflows/buildcrossplatform.yml/badge.svg)](https://github.com/warshoot3r/cargiantscrape/actions/workflows/buildcrossplatform.yml)

# Compatibility 
Should run on anything. Run in a docker isolated env
tested on:
ubuntu amd64
pi4 aarch64


# install
install docker and docker-compose on linux distro

clone the git repo

cd folder


Create a credentials.py

create a used_cars.db file

./run_container.sh



# Manually Running
Run main.py for terminal output of car scrape and telegram sending the report


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