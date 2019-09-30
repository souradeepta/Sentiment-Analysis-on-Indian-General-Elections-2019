# Dashboards and Live Tweet Analysis

This project deals with setting up collected tweets data in [Elasticsearch](https://www.elastic.co/products/elasticsearch) database and viewing the results on [Kibana](https://www.elastic.co/products/kibana) dashboard.

It also contains code to query live data and update into elasticsearch. This is used to generate the live feed on the dashboard.

## Pre-Requisites ##

+ Install mysql database as instructed in the root ReadMe of this project.
+ Install Elasticsearch and Kibana. The easiest is to do this using [Docker](https://www.docker.com/products/docker-desktop).
    * Steps for Docker installation of these applications can be found in the  steps_for_docker_setup file (**recommended**). [Docker Installation Guide](https://docs.docker.com/docker-for-windows/install/)
    * Alternative is to follow the install instructions for [Elasticsearch](https://www.elastic.co/start) and [Kibana](https://www.elastic.co/start)


## Elasticsearch ##

+ Once installed ```POST``` the query mentioned in the file *code/es_tempate* to ```http://<elasticsearch_ip>:9200/sentiments``` (assuming default port)
+ This will setup the required indexing parameters required to load our tweets into this database.
+ Dump sql data to Elasticsearch:
    * Ensure that mysql has been setup correctly and has the tweets dump
    * Execute ```python code/json_loadsql.py```. This will create the required json file with records to load into elasticsearch.
    * Execute ```python code/es_datastore.py```. This will index data into elasticsearch


## Kibana ##

+ Ensure that Elasticsearch has been setup and running as described in above section.
+ Ensure that Kibana is up and running as described in the install guide. Launch kibana ```http://<kibana_ip>:5601``` (assuming deafult port)
+ Click on the ```Management``` tab from the side bar bar (cog icon). Go to ```Index patterns -> Create Index pattern```.
+ Enter ```Index pattern``` as ```sentiments``` and click ```Next Step```.
+ Select the ```Time Filter field name``` from dropdown as ```date_time```.
+ Click ```Create index pattern -> Saved Objects -> Import``` and upload the *code/kibana.json*
+ Click on the ```Dashboard``` tab from the side menu bar. Select the ```[Politics] Indian Elections 2019``` dashboard and you should be all set.

## Live Tweets ##
+ Ensure that Elasticsearch has been setup and running as described in above section.
+ Execute ```python code/live_capture.py```. This will index data into elasticsearch

