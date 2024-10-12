[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/aT5nFo9g)


## Project Checklist
### App Resources Checklist
- [Streamlit App](####Streamlit)
- [CloudSQL for Postgres Instance](####CloudSQL)
- [Google Dataproc](####Google-Dataproc)
- [Google Cloud Storage](####Google-Cloud-Storage)
- [Google Kubernetes Engine](####Google-Kubernetes-Engine)
- [Data Engineering](####Data-Engineering)

#### Streamlit
- [ ] Initialize Poetry App
- [ ] Create Home Page
- [ ] Create CloudSQL connection
- [ ] Create Dataproc connection
- [ ] Create and test Dockerfile

#### CloudSQL
- [x] Create CloudSQL for Postgres Instance
- [x] Create Dataproc cluster
- [ ] Connect to Streamlit

#### Google-Cloud-Storage
- [ ] Create Cloud Storage resource
- [ ] Connect Streamlit to GCS

#### Google-Dataproc-Cluster
- [ ] Properly initialize Dataproc cluster
    - Best initialization info can be found [here](https://github.com/GoogleCloudDataproc/initialization-actions/tree/master/cloud-sql-proxy)
    - If you don't use that, you need the jar files for the following dependencies all stored in the dataproc staging bucket: socket-factory-core, postgres-socket-factory, google oauth2 library http, google oauth2 credentials, google http client, and cloud sql connector jdbc sqlserver all 
- [ ] Connect Streamlit to GCS


#### Google-Kubernetes-Engine
- [x] Create Google Artifact Registry and Repo
- [ ] Create GKE Cluster
- [ ] Create VPC and add all Google necessary Google Resources, should have done this first
- [ ] Enable Public NAT 
- [x] Create Deployment and LoadBalancer Service Manifests
- [ ] Connect GKE to Dataproc
- [ ] Test Deployment and Communication 
