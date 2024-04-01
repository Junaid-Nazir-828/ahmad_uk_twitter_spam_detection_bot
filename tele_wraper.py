import re
import joblib
from Telegram.send_message import send
from malicious_urls.preprocess import main

async def check_tele_messages(message):    
    # check if there is any url in text
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4})(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url_check = re.findall(regex, message)
    urls =  [x[0] for x in url_check]

    # in case there is no url
    if len(urls) == 0:
        model = joblib.load('./Fake_News/pipeline.sav')
        result = model.predict([message])
        print('result',str(result))
        if result[0] == 0:
            await send(f'RE : {message}\n\n*** Fake News Detected ***')
        else:
            await send(f'RE : {message}\n\n*** No Spam Detected ***')

    # in case url/s is/are present
    else:
        model = joblib.load('./malicious_urls/malicious_url.sav')
        url_status = []
        for i in urls:
            result = model.predict(main(i))
            url_status.append(result[0])
        
        result_message = f'RE : {message}\n\n'
        for url, stat in zip(urls, url_status):
            if stat == 0:
                result_message += f'{url} **clear**\n'
            else:
                result_message += f'{url} **malicious**\n'

        await send(result_message)
        print(url_status)




