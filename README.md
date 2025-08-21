 # cargiantscrape .
pythonised scraping car giant for models and prices. Sends a report via telegram.1
 

Production branch: [![Automatic - Build and push as branch name and Test](https://github.com/warshoot3r/cargiantscrape/actions/workflows/build-test-master.yml/badge.svg?branch=master)](https://github.com/warshoot3r/cargiantscrape/actions/workflows/build-test-master.yml)  
Recent Run Production branch: [![Daily run and send messages via Telegram](https://github.com/warshoot3r/cargiantscrape/actions/workflows/run-master-branch.yml/badge.svg?branch=master)](https://github.com/warshoot3r/cargiantscrape/actions/workflows/run-master-branch.yml)  

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
echo -e 'api_token = "" \nchat_id = ""' >> credentials.py
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
