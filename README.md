# BDSO-sentiment-analysis
Single post sentiment analysis


### Preparing Deployment environment

To deploy lambda function we use docker container. Check out the docker
project from github: https://github.com/agilebeat-inc/BDSO-docker-serverless

Follow instructions in the Readme.md file for the docker project

### Prepering serverless environment on the docker container

Before we deploy lambda function to the aws we need to execute few preparation
steps. First will be creating virtual environment for python 3.7 where we will
install all packages necessary for the lambda function. Then we will install
serverless plugins necessary for deployment (plugins are extensions allowing more granular
control over aws). Finally we will deploy lambda function.

At this point we are assuming that you have executed the steps listed in the
Readme.md for the BDSO-docker-serverless project. You should have running
docker container and have shell terminal: `root@<IMAGE-ID>:/root/bdso/BDSO-sentiment-analysis#`

#### Step 1. Set pu virtual python environment

1. Run: `python3 -m venv python.venv`
   This comman will create python virtual environment which is a folder `python.venv`
   insde the project. Please don't check in that folder to the github.

2. Activate python virtual environment. Run command:

   `source python.venv/bin/activate`

   You should see:

   `(python.venv) root@<IMAGE-ID>:~/root/bdso/BDSO-sentiment-analysis#`

3. Install packages necessary for lambda in the virtual environment:

   `pip install vaderSentiment requests nltk gensim pandas matplotlib seaborn`


4. Capture python packages in a file so that serverless will know which
   python packages should be included in zip file containing lambda function

   `pip freeze > requirements.txt`

5. Install necessary plugins for serverless. Run:

   `serverless plugin install -n serverless-python-requirements`

   `serverless plugin install -n serverless-reqvalidator-plugin`

   `serverless plugin install -n serverless-aws-documentation`

   `serverless plugin install -n serverless-plugin-custom-roles`

   *Comment: Serverless plugins are extensions for serverless allowing to get more granula
   control for different cloud providers: aws, asure ...*


6. Finally run deploy command:

   `serverless deploy -v`



The lamada function returns "post content", "polarity" (positive/negative/neutral), and sentiment "score".
When the request is provided, for example,   
  '{  
 "post_content": "I love icecream, so yammy!"  
   }'

the function returns
  '{
     "post": "I love icecream, so yammy!",
     "polarity": "positive",
     "score": 0.6696
  }'
