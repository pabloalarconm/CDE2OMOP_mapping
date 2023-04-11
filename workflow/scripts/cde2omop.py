from SPARQLWrapper import SPARQLWrapper, JSON, POST, BASIC
import logging
import yaml
import os
import chevron
import pandas as pd
import csv, re
import sys
from perseo.main import get_files
from datetime import date, datetime

## Connect with GraphDB repo via SPARQL and send the query

# GraphDB connection:

with open("config.yaml") as file:
    configuration = yaml.load(file, Loader=yaml.FullLoader)

TRIPLESTORE_URL = configuration["TRIPLESTORE_URL"]
TRIPLESTORE_USERNAME = configuration["TRIPLESTORE_USERNAME"]
TRIPLESTORE_PASSWORD = configuration["TRIPLESTORE_PASSWORD"]


# Query configuration
ENDPOINT = SPARQLWrapper(TRIPLESTORE_URL)
ENDPOINT.setHTTPAuth(BASIC)
ENDPOINT.setCredentials(TRIPLESTORE_USERNAME, TRIPLESTORE_PASSWORD)
ENDPOINT.setMethod(POST)


#Import queries:
pathfile = "../queries/"
all_files = get_files(pathfile,"mustache")

for file in all_files:

    with open('../queries/'+ file, 'r') as f:
        query = chevron.render(f, {})

    # Perform query:
    ENDPOINT.setQuery(query)
    ENDPOINT.setReturnFormat("csv")
    result = ENDPOINT.query().convert()

    ## Store the resulting tables
    resulting_data = result.decode('utf-8').splitlines()
    with open("output_"+ file +".csv", "w") as csv_file:
        writer = csv.writer(csv_file, delimiter = ';')
        for line in resulting_data:
            writer.writerow(re.split('\s+',line))

## Edit the tables

df_PERSON = pd.read_csv("output_cde2omop_person.mustache.csv")
df_CONDITION_VISIT = pd.read_csv("output_cde2omop_condition_visit.mustache.csv")
df_MEASUREMENT_VISIT = pd.read_csv("output_cde2omop_measurement_visit.mustache.csv")

os.remove("output_cde2omop_person.mustache.csv")
os.remove("output_cde2omop_condition_visit.mustache.csv")
os.remove("output_cde2omop_measurement_visit.mustache.csv")


# PERSON
df_PERSON = df_PERSON.where(pd.notnull(df_PERSON), None)
df_PERSON.loc[df_PERSON.gender_source_value == 'http://purl.obolibrary.org/obo/NCIT_C16576', 'gender_concept_id'] = "8532"
df_PERSON.loc[df_PERSON.gender_source_value == 'http://purl.obolibrary.org/obo/NCIT_C20197', 'gender_concept_id'] = "8507"
df_PERSON.loc[df_PERSON.gender_source_value == 'http://purl.obolibrary.org/obo/NCIT_C124294', 'gender_concept_id'] = "9999"
df_PERSON.loc[df_PERSON.gender_source_value == 'http://purl.obolibrary.org/obo/NCIT_C17998', 'gender_concept_id'] = "9999"



for index, row in df_PERSON.iterrows():

    # Create all date-related columns:
    date_string = df_PERSON["Birth_datetime"][index]
    date = datetime. strptime(date_string, '%Y-%m-%d')
    time = datetime.min.time()
    datetime = datetime.combine(date, time)
    df_PERSON["Birth_datetime"][index] = datetime
    df_PERSON["Year_of_birth"][index] = datetime.year
    df_PERSON["Month_of_birth"][index] = datetime.month
    df_PERSON["Day_of_birth"][index] = datetime.day


    if row["race_concept_id"] == None:
        df_PERSON["race_concept_id"][index] = 0     

    if row["Ethnicity_concept_id"] == None:
        df_PERSON["Ethnicity_concept_id"][index] = 0       

df_PERSON.to_csv("../data/PERSON.csv", index = False, header=True)


# CONDITION - VISIT:
df_CONDITION_VISIT = df_CONDITION_VISIT.where(pd.notnull(df_CONDITION_VISIT), None)


for index, row in df_CONDITION_VISIT.iterrows():
    if row["condition_type_concept_id"] == None:
        df_CONDITION_VISIT["condition_type_concept_id"][index] = "32879" 

    if row["condition_status_concept_id"] == None:
        df_CONDITION_VISIT["condition_status_concept_id"][index] = "32893" 

    if row["visit_type_concept_id"] == None:
        df_CONDITION_VISIT["visit_type_concept_id"][index] = "32879" 

    if row["visit_concept_id"] == None:
        df_CONDITION_VISIT["visit_concept_id"][index] = "38004515" 

    date_string = df_CONDITION_VISIT["condition_start_date"][index]
    date = datetime. strptime(date_string, '%Y-%m-%d')
    time = datetime.min.time()
    datetime = datetime.combine(date, time)
    df_CONDITION_VISIT["condition_start_datetime"][index] = datetime

    date_string = df_CONDITION_VISIT["condition_end_date"][index]
    date = datetime. strptime(date_string, '%Y-%m-%d')
    time = datetime.min.time()
    datetime = datetime.combine(date, time)
    df_CONDITION_VISIT["condition_end_datetime"][index] = datetime

    date_string = df_CONDITION_VISIT["visit_start_date"][index]
    date = datetime. strptime(date_string, '%Y-%m-%d')
    time = datetime.min.time()
    datetime = datetime.combine(date, time)
    df_CONDITION_VISIT["visit_start_datetime"][index] = datetime

    date_string = df_CONDITION_VISIT["visit_end_time"][index]
    date = datetime. strptime(date_string, '%Y-%m-%d')
    time = datetime.min.time()
    datetime = datetime.combine(date, time)
    df_CONDITION_VISIT["visit_end_datetime"][index] = datetime


df_CONDITION_VISIT[df_CONDITION_VISIT.columns[0:16]].to_csv("../data/CONDITION.csv", index = False, header=True)

df_VISIT_C = df_CONDITION_VISIT[df_CONDITION_VISIT.columns[[1,10,11,16,17,18,19,20,21,22,23,24,25,26,27,28,29]]]

# MEASUREMENT - VISIT:

df_MEASUREMENT_VISIT = df_MEASUREMENT_VISIT.where(pd.notnull(df_MEASUREMENT_VISIT), None)


for index, row in df_MEASUREMENT_VISIT.iterrows():

    if row["visit_type_concept_id"] == None:
        df_MEASUREMENT_VISIT["visit_type_concept_id"][index] = "32879" 

    if row["visit_concept_id"] == None:
        df_MEASUREMENT_VISIT["visit_concept_id"][index] = "38004515" 

    date_string = df_MEASUREMENT_VISIT["measurement_date"][index]
    date = datetime. strptime(date_string, '%Y-%m-%d')
    time = datetime.min.time()
    datetime = datetime.combine(date, time)
    df_MEASUREMENT_VISIT["measurement_datetime"][index] = datetime

    date_string = df_MEASUREMENT_VISIT["visit_start_date"][index]
    date = datetime. strptime(date_string, '%Y-%m-%d')
    time = datetime.min.time()
    datetime = datetime.combine(date, time)
    df_MEASUREMENT_VISIT["visit_start_datetime"][index] = datetime

    date_string = df_MEASUREMENT_VISIT["visit_end_time"][index]
    date = datetime. strptime(date_string, '%Y-%m-%d')
    time = datetime.min.time()
    datetime = datetime.combine(date, time)
    df_MEASUREMENT_VISIT["visit_end_datetime"][index] = datetime

df_MEASUREMENT_VISIT[df_MEASUREMENT_VISIT.columns[0:19]].to_csv("../data/MEASUREMENT.csv", index = False, header=True)

df_VISIT_M = df_MEASUREMENT_VISIT[df_MEASUREMENT_VISIT.columns[[1,12,13,19,20,21,22,23,24,25,26,27,28,29,30,31,32]]]

# VISIT:

df_VISIT = pd.concat([df_VISIT_C, df_VISIT_M])
df_VISIT.to_csv("../data/VISIT.csv", index = False, header=True)



