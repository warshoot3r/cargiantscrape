# cargiantscrape
Scraping car giant for models and prices

# set up 
python -m pip install -r requirements.txt
and if needed
python -m pip install -r requirements.txt --upgrade
create a credentials.py containing chatid and bot key


# Running
Run main.py for terminal output of car scrape and telegram sending the report


# Running in container on raspi4
clone the repo
docker compose build 
docker compose up -d

# Todo:
scheduled telegram webhook which requires https ssl and code so that bot runs forever

if car price changes, add the old price to a column and then add a column to say price changed in last 5 days


