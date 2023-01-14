# BestBuy PS5 Scrapper
Best Buy website scrapper to scrap website for PS5 stocks at nearby locations and notify if stock becomes available

### To run and get updated on your email follow these instructions
```
git clone [http/ssh repo url]
cd [repo/location/]
conda create -n [env-name] python="3.10"
conda activate [env-name]
pip install -r requirements.txt
export $email=[your-email]
export $password=[email-password]
python main.py --postal_code [your-postal-code]
```