This will describe the steps to create a serverless jupyter notebook deployment on Google App Engine, use a serverless Spark cluster with DataProc, and use that Spark backend to process the multi-million row Kaggle MQTTset dataset and conduct an analysis of various machine learning models used to train the dataset 

The following will assume the use of environment variables as follows

## Google Cloud SQL
1. Create the instance
```
gcloud sql instances create projectdb \
    --database-version=POSTGRES_15 \
    --tier=db-custom-2-4096 \
    --region=us-east1 \
    --storage-type=SSD \
    --storage-size=20GB \
    --availability-type=zonal
```
2. Create a user for your postgres instance

3. Get connection details
- Look for connectionName toward the top, and ipAddresses a few properties below
```
gcloud sql instances describe projectdb
```
Example: 
connectionName: systool-436201:us-east1:projectdb
ipAddresses:
- ipAddress: 104.196.99.150
  type: PRIMARY
- ipAddress: 34.73.209.232
  type: OUTGOING
4. Create Database
CloudSQL does not have a default database like a local postgres instance so you must create one
```
gcloud sql databases create mqttdb --instance=projectdb
```
- Optional: And you can also connect to the database from the terminal as you should already be logged into the gcloud CLI
```
gcloud sql connect my-postgres-instance --user=my-user
```

## Google Cloud DataProc
Given the limitations of the Google Cloud Education quota, you need to limit the storage and each worker has it's own storage so here I'm taking up 300GB of the quota. Additionally, I'm using some lower-powered E2-standard compute type nodes. 

**Very Important** You must point Spark in the DataProc cluster to the requisite JAR files and if you want a secure connection rather than over the internet, use the cloud-sql-proxy.sh from the documentation [here](https://github.com/GoogleCloudDataproc/initialization-actions/tree/master/cloud-sql-proxy)

In addition to the Cloud SQL Proxy, you'll need the JARs, which for PostgreSQL 15 are:
postgresql-42.3.1.jar $JARS_DIR
jdbc-socket-factory-core-1.20.1.jar $JARS_DIR
google-auth-library-oauth2-http-1.24.1.jar

And the cloud-sql-proxy.sh has the JAR copy command for initialization in the shell, but you still need to add them to the bucket which you can do by downloading them yourself into your current directory and add via the `gsutil cp` command

Finally, the command to create your Spark Cluster
```
gcloud dataproc clusters create project-cluster \
    --region=us-east1 \
    --project=systool-436201 \
    --subnet=default \
    --scopes=cloud-platform \
    --master-machine-type=e2-standard-4 \
    --master-boot-disk-size=100GB \
    --num-workers=2 \
    --worker-machine-type=e2-standard-4 \
    --worker-boot-disk-size=100GB \
    --optional-components=JUPYTER,DOCKER,FLINK \
    --enable-component-gateway \
    --initialization-actions=gs://dataproc-staging-us-central1-353241962082-fj6qfu9g/cloud-sql-proxy.sh \
    --metadata=additional-cloud-sql-instances=systool-436201:us-east1:projectdb=tcp:5432 \
    --metadata=google-cloud-project=systool-436201 \
    --properties=spark.jars=gs://dataproc-staging-us-central1-353241962082-fj6qfu9g/postgresql-42.3.1.jar,gs://dataproc-staging-us-central1-353241962082-fj6qfu9g/jdbc-socket-factory-core-1.20.1.jar,gs://dataproc-staging-us-central1-353241962082-fj6qfu9g/google-auth-library-oauth2-http-1.24.1.jar
```
Test connection
```
gcloud dataproc jobs submit pyspark gs://dataproc-staging-us-east1-353241962082-k4mrauce/test_cloud_sql_connection.py     --cluster=project-cluster     --region=us-east1     --jars=gs://dataproc-staging-us-central1-353241962082-fj6qfu9g/postgresql-42.3.1.jar,gs://dataproc-staging-us-central1-353241962082-fj6qfu9g/google-http-client-1.42.2.jar,gs://dataproc-staging-us-central1-353241962082-fj6qfu9g/cloud-sql-connector-jdbc-sqlserver-1.20.1.jar,gs://dataproc-staging-us-central1-353241962082-fj6qfu9g/postgres-socket-factory-1.20.1.jar,gs://dataproc-staging-us-central1-353241962082-fj6qfu9g/google-auth-library-oauth2-http-1.24.1.jar,gs://dataproc-staging-us-central1-353241962082-fj6qfu9g/google-auth-library-credentials-1.24.1.jar,gs://dataproc-staging-us-central1-353241962082-fj6qfu9g/jdbc-socket-factory-core-1.20.1.jar    
```