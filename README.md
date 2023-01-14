# BestBuy PS5 Scraper

Best Buy Canada website scraper to scrape website for PS5 stocks at nearby locations (based on the postal code provided) and notify in email when stock becomes available so you could quickly get your hands on them.

### To run and get updated on your email follow these instructions

#### Clone repo and move to its directory
```
git clone [http/ssh repo url]
cd [repo/location/]
```

#### *Recommended*: Create environment using [venv](https://docs.python.org/3/library/venv.html) or [conda](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)
```
conda create -n [env-name] python="3.10"
conda activate [env-name]
```

#### Save email credentials as env variables:
```
export $email=[your-email]
export $password=[email-password]
```
#### Install required packages and run command:
```
pip install -r requirements.txt
python main.py --postal_code [your-postal-code]
```

### To schedule scraping to *run at a frequency* you can use [cron](https://code.tutsplus.com/tutorials/scheduling-tasks-with-cron-jobs--net-8800)



*P.S a bug with chromedriver causes it to not work on linux right now, working on a fix.*
