try:
  import unzip_requirements
except ImportError:
  pass

import json
import re

import matplotlib.pyplot as plt
from io import StringIO
import nltk
import pandas as pd
import seaborn as sns


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


def word_barchart(post_cleaned):
    word_freq = nltk.FreqDist(post_cleaned)
    word_freq_df = pd.DataFrame({'Key_Words': list(word_freq.keys()), 'Count': list(word_freq.values())})
    word_freq_df = word_freq_df.nlargest(columns="Count", n=10)
    plt.figure(figsize=(16, 5))
    ax = sns.barplot(data=word_freq_df, x="Key_Words", y="Count")
    ax.set_title('Top 10 Most Frequent Keywords')
    ax.set(ylabel='Count')

    output = StringIO()
    plt.savefig(output, dpi=None, facecolor='w', edgecolor='w',
                orientation='portrait', papertype=None, format="svg",
                transparent=False, bbox_inches=None, pad_inches=0.1,
                frameon=None, metadata=None)
    output.seek(0)
    response_body = output.read()
    return response_body


# content = "About one in four companies revealed personal information to a woman's partner, who had made a bogus demand for the data by citing an EU privacy law. The security expert contacted dozens of UK and US-based firms to test how they would handle a 'right of access' request made in someone else's name. In each case, he asked for all the data that they held on his fiancee. In one case, the response included the results of a criminal activity check. Other replies included credit card information, travel details, account logins and passwords, and the target's full US social security number. University of Oxford-based researcher James Pavur has presented his findings at the Black Ha"

def barplotHandler(event, context):
    body_txt = event['body']
    body_json = json.loads(body_txt)
    post = body_json["content"]

    post_wo_usr, post_wo_usr_hash, post_cleaned = clean_post(post)
    response_body = word_barchart(post_cleaned)

    response = {
        "statusCode": 200,
        "headers": {'Content-Type': 'image/svg+xml', 'Access-Control-Allow-Origin': '*'},
        "body": response_body
    }

    return response

