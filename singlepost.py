try:
  import unzip_requirements
except ImportError:
  pass



import json
#import boto3

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re


def remove_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, '', input_txt)

    return input_txt


def clean_post(post):
    # remove @username & hash
    post_wo_usr = remove_pattern(post, "@[\w]*")
    post_wo_usr_hash = post_wo_usr.replace("#", "")

    ### Removing Punctuations, Numbers, and Special Characters / short word
    post_cleaned = post_wo_usr.replace("[^a-zA-Z#]", " ")
    post_cleaned = [w for w in post_cleaned.split() if len(w) > 3]

    return post_wo_usr, post_wo_usr_hash, post_cleaned


def sentiment_scores(post):
    analyser = SentimentIntensityAnalyzer()

    snt = analyser.polarity_scores(post)

    if snt['neg'] > 0 and snt['compound'] < 0:
        polarity = 'negative'
    elif snt['pos'] > 0 and snt['compound'] > 0:
        polarity = 'positive'
    else:
        polarity = 'neutral'

    snt_Score = snt['compound']

    return polarity, snt_Score


def analyze_post(post):
    post_wo_usr, post_wo_usr_hash, post_cleaned = clean_post(post)
    polarity, sen_Score = sentiment_scores(post_wo_usr_hash)

    return polarity, sen_Score


def singlepostHandler(event, context):
    body_txt = event['body']
    body_json = json.loads(body_txt)
    post = body_json["post_content"]

    polarity, sen_Score = analyze_post(post)

    response = {
        "statusCode": 200,
        "headers": {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
        "body": json.dumps({'post': post, 'polarity':polarity, 'score':sen_Score})
    }
    
    return response

