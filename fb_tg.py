import requests
from facebook_scraper import get_posts
import io

try:
    from tg_tokens import bot_token, bot_chatID
except ImportError:
    #add here your data:
    bot_token = ''
    bot_chatID = ''

#change to your page
PAGE_NAME = 'GitHub'

#Handle not sending posts again...
last_send_post_id_file = 'last_send_post_id'

def set_last_send_post_id(post_id):
    with open(last_send_post_id_file, "w") as f:
        f.write(post_id)
    
def get_last_send_post_id():
    try:
    	with open(last_send_post_id_file, "r") as f: 
            last_send_post_id = f.readline()   
    	return last_send_post_id
    except:
        return 0

#Telegram APIs
def telegram_bot_sendtext(bot_message):
    url = "https://api.telegram.org/bot"+bot_token+"/sendMessage"    
    send_text = url + '?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    r = requests.get(send_text)
    print(r.status_code, r.reason, r.content)

def telegram_bot_sendImageRemoteFile(img_url,caption):
    url = "https://api.telegram.org/bot"+bot_token+"/sendPhoto"
    remote_image = requests.get(img_url)
    photo = io.BytesIO(remote_image.content)
    photo.name = 'img.png'
    files = {'photo': photo}
    data = {'chat_id' : bot_chatID, "caption" : caption}
    r = requests.post(url, files=files, data=data)
    print(r.status_code, r.reason, r.content)

#The main function
def get_my_posts(last_send_post_id):
    newest=True
    for post in get_posts(PAGE_NAME, pages=2):       
        print(post['post_id'] +' ' + str(post['text']) + " image: " + str(post['image']))
        if post['post_id']==last_send_post_id:
            print("already sent post...")
            break

        if post['image']:
            telegram_bot_sendImageRemoteFile(post['image'],post['text'])
        else:
            telegram_bot_sendtext(post['text'])

        if newest:
            newest=False
            set_last_send_post_id(post['post_id'])

if __name__ == "__main__":
    get_my_posts(get_last_send_post_id())
