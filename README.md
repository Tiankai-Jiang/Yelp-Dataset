# Yelp-Dataset

A project to 

- build relational database of yelp dataset using MySQL

- build a simple server-client using Flask

- perform data mining on the dataset

# Dependencies

- Python3

- mysql-connector-python

- Flask

- prettytable

- numpy

- seaborn

- pandas

- geopandas

- sklearn

- wordcloud

# Usage

- 01 and 02: Data preprocessing and extraction

- 03: Dump data to mysql

- 04: Flask server and client

- 05: Data mining

# Demo

Detailed implementation and analysis can be found in 06_report/report.pdf

## ER Diagram
![ER_Diagram](06_report/ER_Diagram.png)

## Commandline Client
![client1](04_serverAndClient/client1.png)
![client2](04_serverAndClient/client2.png)
![client3](04_serverAndClient/client3.png)

## Some plots
![Distribution_Restaurants](05_dataMining/distributionRestaurants.png)

![Distribution_Locations](05_dataMining/distributionBusinessGeo.png)

![Distribution_CheckinTime](05_dataMining/checkinTimeVSDay.png)

![Confusion_Matrix](05_dataMining/Logistic%20Regression%20Confusion%20Matrix.png)

![Word_Cloud](05_dataMining/Random%20Forest%20Top%20Words.png)