import re
import joblib
from malicious_urls.preprocess import main

def check_tweet(message):    
    # check if there is any url in text
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4})(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url_check = re.findall(regex, message)
    urls =  [x[0] for x in url_check]

    # in case there is no url
    if len(urls) == 0:
        print("DETECTING FAKE NEWS")
        model = joblib.load('./Fake_News/pipeline.sav')
        result = model.predict([message])
        print('result : ',str(result))
        if result[0] == 0:
            return '*** After analysis, this tweet has been flagged as potentially malicious. Please exercise caution and refrain from sharing.\nLink for more information: https://www.ncsc.gov.uk ***'
        else:
            return '*** This tweet has been reviewed and found not to be malicious.\nLink for more information: https://www.ncsc.gov.uk ***'

    # in case url/s is/are present
    else:
        print("DETECTING MALICIOUS URLS")
        model = joblib.load('./malicious_urls/malicious_url.sav')
        url_status = []
        for i in urls:
            result = model.predict(main(i))
            url_status.append(result[0])
        
        result_message = ''
        for url, stat in zip(urls, url_status):
            if stat == 0:
                result_message += f'{url} **clear**\n'
            else:
                result_message += f'{url} **malicious**\n'
        print("result : ",str(result_message))
        return result_message        




