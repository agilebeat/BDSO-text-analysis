try:
  import unzip_requirements
except ImportError:
  pass

import json
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords        # for stop words removal
nltk.download('stopwords')
from nltk.stem import WordNetLemmatizer  # for lemmatization
from gensim import corpora
import gensim


def clean_post(post):
    remove_spcecials = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", post).split())
    tokenized = remove_spcecials.split()

    stop_words = stopwords.words('english') + ['u', 'ur']
    stop_words_removed = [word for word in tokenized if word not in stop_words]

    lemmatizer = WordNetLemmatizer()
    lemmatized_post = [lemmatizer.lemmatize(word) for word in stop_words_removed]

    return lemmatized_post


def topic_modeling(text_data, n_topics=5, n_words=5):
    dictionary = corpora.Dictionary(text_data)
    corpus = [dictionary.doc2bow(text) for text in text_data]

    NUM_TOPICS = n_topics
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=NUM_TOPICS, id2word=dictionary, passes=5)
    ldamodel.save('model.gensim')
    topics = ldamodel.print_topics(num_words=n_words)

    topic_result = []
    for topic in topics:
        topic_num = topic[0]
        topic_dict = {}
        topic_splits = topic[1].split(" + ")

        for word in topic_splits:
            sp = word.split("*")
            weight = float(sp[0])
            keyword = sp[1].replace('"', '')
            topic_dict[keyword] = weight

        topic_result.append(topic_dict)
    return topic_result


def preprocess_docs(doc_list):
    df = pd.DataFrame(doc_list)
    df['cleaned'] = df['tweet'].apply(lambda x: clean_post(x))
    text_data = list(df['cleaned'])
    return text_data


def topicmodelingHandler(event, context):
    body_txt = event['body']
    body_json = json.loads(body_txt)
    topic_number = body_json['topic_number']
    words_number = body_json['words_number']
    post_documents = body_json['post_documents']
    docs = preprocess_docs(post_documents)

    topics = topic_modeling(docs, n_topics = topic_number , n_words = words_number)

    response_body = topics

    response = {
        "statusCode": 200,
        "headers": {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
        "body": response_body
    }

    return response

