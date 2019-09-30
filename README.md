# Readme for this Project
## TOPIC: Sentiment Analysis on Indian General Elections 2019 

```
code
│   README.md    
│
└───db_dump
│      smdm_party_sentiment.sql
│      smdm_routines.sql
│ 
└───ipynb
│      1. Training the models.ipynb
│      2. Sentiment Analysis.ipynb
│      3. Textblob sentiment.ipynb 
|  
└───pickle
│      Bernoulli_NB.pickle
│      documents.pickle
│      Linear_SVC.pickle   
|      Logistic_Regression.pickle
|      Multinomial_NB.pickle
|      Naive_Bayes.pickle
|      Nu_SVC.pickle
|      SGD_Classifier.pickle
|      word_features.pickle
|  
└───py_code
│   │   json_loadsql.py 
|   |   live_capture.py
|   |   readme.md
|   |   sentiment_analyzer.py
|   |   tweet_cleanser.py
|   |   twitter_stream_handler.py
|   |   vote_classifier.py
|   |   live_capture.py
|   |   steps_for_docker_setup
|   |   kobana.json
|   |   es_datastore.py
|   |   es_template
|   |
|   |
│   └───screenshots
|   |
│   └───dump
|   |
│   └───pickle
│      Bernoulli_NB.pickle
│      documents.pickle
│      Linear_SVC.pickle   
|      Logistic_Regression.pickle
|      Multinomial_NB.pickle
|      Naive_Bayes.pickle
|      Nu_SVC.pickle
|      SGD_Classifier.pickle
|      word_features.pickle
|
└───short_reviews
│      negative.txt
│      positive.txt
|
└───sql_queries
│      analysis.sql
|      default.sql
|
```

**db_dump:**
contains the database dump the tweets crawled. Routines are optional
can be imported using MySQL CLI :

`
database_name < smdm_party_sentiment.sql
` 

or using Workbench recommended <https://www.mysql.com/products/workbench/>

**ipynb:**
THe order of files has been mentione in the file names. Code to be run on Jupyter notebook which can be downloaded from  <https://www.anaconda.com/distribution/>.
1. Training the models.ipynb - trains the models and pickles them.
2. Sentiment Analysis.ipynb - crawls twitter and runs tweets through loaded models and dumps into the mysql database.
3. Textblob sentiment.ipynb - appends textblob based sentiment to the crawled tweets

**pickle:** Contains the trained models from "1. Training the models.ipynb". 
This allows "2. Sentiment Analysis.ipynb" to be run directly

**py_code:** Refer to the readme inside the folder for detailed information about Elasticsearch dump and dashboard usage on Kibana

**short_reviews:** Contains the corpus used to train models. Used by "1. Training the models.ipynb"

**sql_queries:** Contains our analysis queries for elemenarty data insights and cleaning. Can be run on mysql CLI or Workbench
