# MQTTset, a new dataset for MQTT  

The proposed work aims to create a dataset linked to the IoT context, in particular on the MQTT communication protocol, in order to give to the research and industrial community an initial dataset to use in their application. The dataset is composed by IoT sensors based on MQTT where each aspect of a real network is defined. In particular, the MQTT broker is instantiated by using Eclipse Mosquitto and the network is composed by 8 sensors. The scenario is related to a smart home environment where sensors retrieve information about temperature, light, humidity, CO-Gas, motion, smoke, door and fan with different time interval since the behaviour of each sensor is different with the others.

## Getting Started

In order to user the dataset, simply download the github repository and start to work with the csv or PCAP file. Please if you use this dataset in a research work, please cite this article.

XXX


### MQTT network structure
As mentioned, the dataset isc composed by 8 MQTT sensors with different features. In table, the MQTT sensors are reported. Each sensor is associated with a data profile and a topic linked to the MQTT broker. The data profile consists of the type of data that the sensors communicate while the topic is defined by the sensor when sending the data to the broker. Finally, the sensors were conceptually divided into two rooms as if they were distributed in a smart house and the MQTT broker has 10.16.100.73 as IP address with 1883 as clear text communication port. In the table, the time could be periodic o random. This concept is important since a temperature sensor has a periodic behavior over time, i.e. cyclically sending information retrieved from the environment periodically (defined as P). Instead, a motion sensor has a more random behavior since it sends information only when a user passes in front of the sensor (defined as R)). By analyzing also this aspect, the dataset is even more valid as a real behavior of a home automation is simulated and implemented. 

Sensor | IP address | Room | Time (P:periodic, R:random) | Topic | Data Profile 
--- | --- | --- | --- |--- |--- 
Temperature | 192.168.0.151 | 1 | P, 60 s | Temperature| Temperature 
    Light intensity | 192.168.0.150 | 1 | P, 1800 s | Light intensity| Light intensity 
    Humidity | 192.168.0.152 | 1 | P, 60 s | Humidity| Humidity 
    Motion sensor | 192.168.0.154 | 1 | R, 1 h | Motion sensor | Motion sensor 
    CO-Gas | 192.168.0.155 | 1 | R, 1 h s |  CO-Gas|  CO-Gas 
    Smoke | 192.168.0.180 | 2 | R, 1 h | Smoke| Smoke 
    Fan speed controller | 192.168.0.173 | 2 | P, 120 s | Fan speed controller| Fan speed controller 
    Door lock | 192.168.0.176 | 2 |R, 1 h | Door lock| Door lock 
    Fan sensor | 192.168.0.178 | 2 | P, 60 s | Fan sensor| Fan sensor 
    Motion sensor | 192.168.0.174 | 2 | R, 1 h | Motion sensor | Motion sensor 


### Github repository organization

The repository is composed by 3 folder:

* PCAP raw data
    * Legitimate
    * SlowITe
    * Bruteforce
    * Malformed data
    * Flooding
    * DoS attack
* CSV file
    * Legitimate
    * SlowITe
    * Bruteforce
    * Malformed data
    * Flooding
    * DoS attack
* Final dataset
    * train70.csv, test30.csv
    * train70_reduced.csv, test30_reduced.csv
    * train70_augmented.csv, test30_augmented.csv

In the PCAP folder, there are the raw network data recovered directly from the sensors of the MQTT network and also the traffic related to the attacks. In the CSV folder instead, there are the data and features extracted from the PCAP file using the tshark tool. Finally, the FINAL_CSV folder contains the CSV files combined with each other and subsequently used for machine learning algorithms. In particular, CSV files are present in 3 different formats:

* train70.csv, test30.csv: in these files, the legitimate traffic was randomly combined with the different malicious traffic.
* train70_reduced.csv, test30_reduced.csv: the reduced form combines malicious traffic with legitimate traffic in the 50:50 form, so there will be less legitimate traffic than actually. The legitimate traffic will be equal to the sum of the malicious traffic
* train70_augmented.csv, test30_augmented.csv: in the augmented form, however, the malicious traffic has been increased so that the sum of the traffic related to the attacks is equal to the legitimate traffic.


## Built With

* [IoT-Flock](https://github.com/ThingzDefense/IoT-Flock) - Framework to generate IoT networks
* [MQTTSA](https://github.com/stfbk/mqttsa) - A security assessment tool for MQTT networks

## Authors

* **Ivan Vaccari** - *Concept, implementation, elaboration, paper writer* - [Profile](https://www.ieiit.cnr.it/people/Vaccari-Ivan)
* **Giovanni Chiola** - *Dataset approach and definitiom* - [Profile](https://www.dibris.unige.it/chiola-giovanni)
* **Maurizio Aiello** - *Supervisor, paper reviewer* - [Profile](https://www.ieiit.cnr.it/people/Aiello-Maurizio)
* **Maurizio Mongelli** - *Machine learning support and contribution* - [Profile](https://www.ieiit.cnr.it/people/Mongelli-Maurizio)
* **Enrico Cambiaso** - *Supervisor, elaboration, paper collaboration* - [Progile](https://www.ieiit.cnr.it/people/Cambiaso-Enrico)


## License

This project is licensed under the Apache License 2.0 - see the [LICENSE.md](LICENSE.md) file for details


