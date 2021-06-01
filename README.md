# facebook_to_telegram
A python script to read a post from Facebook and send it with a Telegram bot

## Usage
Add your bot's token and chat ID (to `tg_tokens.py` file):
```
bot_token = ''
bot_chatID = ''
```

Add the page you want to read:
```
PAGE_NAME = 'blabla'
```

Run it:
```
python3 fb_tg.py
```

## Run it from crontab
You can set up a crontab task that will check the page every X minutes and send only new posts.
