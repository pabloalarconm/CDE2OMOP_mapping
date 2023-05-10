import yaml
import os
import chevron
import pandas as pd
import csv, re
from perseo.main import get_files
from datetime import date, datetime
from tableEdition import TableEdition
from serverConection import ServerConection
import io
import pickle
from SPARQLWrapper import SPARQLWrapper, POST, BASIC, CSV




# Import configuration file:
with open("../configuration/config.yaml") as file:
    configuration = yaml.load(file, Loader=yaml.FullLoader)

# Set credentials:
credentials = ServerConection.setCredentials(configuration)

# GraphDB connection:
query_configuration = ServerConection.queryConection(credentials)


# Import queries:
pathfile = "../queries/"
all_files = get_files(pathfile,"mustache")

for file in all_files:

    with open('../queries/'+ file, 'r') as f:
        query = chevron.render(f, {})

    # Perform query:
    query_configuration.setQuery(query)
    result = query_configuration.query().convert()
    if isinstance(result, list):  # Check if the result is a list
        result_csv = io.StringIO(result[1])  # Extract the CSV data from the list
    else:
        result_csv = io.StringIO(result.decode('utf-8'))
    df = pd.read_csv(result_csv)
    df.to_csv("../data/output_"+ file +".csv", index = False, header=True)














# ## Table edition:

# # Import preliminar tables
# df_PERSON = pd.read_csv("output_cde2omop_person.mustache.csv")
# df_CONDITION_VISIT = pd.read_csv("output_cde2omop_condition_visit.mustache.csv")
# df_MEASUREMENT_VISIT = pd.read_csv("output_cde2omop_measurement_visit.mustache.csv")

# # Remove them before saving the refined one:
# os.remove("output_cde2omop_person.mustache.csv")
# os.remove("output_cde2omop_condition_visit.mustache.csv")
# os.remove("output_cde2omop_measurement_visit.mustache.csv")

# # Headers:
# person_header = ["person_id","gender_concept_id", "year_of_birth", "month_of_birth", "day_of_birth", "birth_datetime", "race_concept_id", "ethnicity_concept_id", "location_id", "provider_id", "care_site_id", "person_source_value", "gender_source_value", "gender_source_concept_id", "race_source_value", "race_source_concept_id", "ethnicity_source_value", "ethnicity_source_concept_id"]
# condition_header = ["condition_occurrence_id","person_id","condition_concept_id","condition_start_date","condition_start_datetime","condition_end_date","condition_end_datetime","condition_type_concept_id","condition_status_concept_id","stop_reason","provider_id","visit_occurrence_id","visit_detail_id","condition_source_value","condition_source_concept_id","condition_status_source_value"]
# visit_header = ["visit_occurrunce_id","person_id","visit_concept_id","visit_start_date","visit_start_datetime","visit_end_time","visit_end_datetime","visit_type_concept_id","provider_id","care_site_id","visit_source_value","visit_source_concept_id","admitting_source_concept_id","admitting_source_value","discharge_to_concept_id","discharge_to_source_value","preceding_visit_occurrence_id"]
# measurement_header=["measurement_id","person_id","measurement_concept_id","measurement_date","measurement_datetime","measurement_time","operator_concept_id","value_as_number","value_as_concept_id","unit_concept_id","range_low","range_high","provider_id","visit_occurrence_id","visit_detail_id","measurement_source_value","measurement_source_conept_id","unit_source_value","value_source_value"]
#                ############ PERSON ###############


# df_PERSON = df_PERSON.where(pd.notnull(df_PERSON), None)
# df_PERSON.loc[df_PERSON.gender_source_value == 'http://purl.obolibrary.org/obo/NCIT_C16576', 'gender_concept_id'] = "8532"
# df_PERSON.loc[df_PERSON.gender_source_value == 'http://purl.obolibrary.org/obo/NCIT_C20197', 'gender_concept_id'] = "8507"
# df_PERSON.loc[df_PERSON.gender_source_value == 'http://purl.obolibrary.org/obo/NCIT_C124294', 'gender_concept_id'] = "9999"
# df_PERSON.loc[df_PERSON.gender_source_value == 'http://purl.obolibrary.org/obo/NCIT_C17998', 'gender_concept_id'] = "9999"



# for index, row in df_PERSON.iterrows():

#     # Create all date-related columns:
#     date_string = df_PERSON["birth_datetime"][index]
#     date = datetime. strptime(date_string, '%Y-%m-%d')
#     time = datetime.min.time()
#     datetime = datetime.combine(date, time)
#     df_PERSON["birth_datetime"][index] = datetime
#     df_PERSON["year_of_birth"][index] = datetime.year
#     df_PERSON["month_of_birth"][index] = datetime.month
#     df_PERSON["day_of_birth"][index] = datetime.day


#     if row["race_concept_id"] == None:
#         df_PERSON["race_concept_id"][index] = 0     

#     if row["ethnicity_concept_id"] == None:
#         df_PERSON["ethnicity_concept_id"][index] = 0       

# df_PERSON.to_csv("../data/PERSON.csv", index = False, header=True)


#               ############# CONDITION - VISIT ####################



# df_CONDITION_VISIT = df_CONDITION_VISIT.where(pd.notnull(df_CONDITION_VISIT), None)


# for index, row in df_CONDITION_VISIT.iterrows():
#     if row["condition_type_concept_id"] == None:
#         df_CONDITION_VISIT["condition_type_concept_id"][index] = "32879" 

#     if row["condition_status_concept_id"] == None:
#         df_CONDITION_VISIT["condition_status_concept_id"][index] = "32893" 

#     if row["visit_type_concept_id"] == None:
#         df_CONDITION_VISIT["visit_type_concept_id"][index] = "32879" 

#     if row["visit_concept_id"] == None:
#         df_CONDITION_VISIT["visit_concept_id"][index] = "38004515" 

#     date_string = df_CONDITION_VISIT["condition_start_date"][index]
#     date_calculated = TableEdition.date2datetime(date_string)
#     df_CONDITION_VISIT["condition_start_datetime"][index] = date_calculated

#     date_string = df_CONDITION_VISIT["condition_end_date"][index]
#     date_calculated = TableEdition.date2datetime(date_string)
#     df_CONDITION_VISIT["condition_end_datetime"][index] = date_calculated

#     date_string = df_CONDITION_VISIT["visit_start_date"][index]
#     date_calculated = TableEdition.date2datetime(date_string)
#     df_CONDITION_VISIT["visit_start_datetime"][index] = date_calculated

#     date_string = df_CONDITION_VISIT["visit_end_time"][index]
#     date_calculated = TableEdition.date2datetime(date_string)
#     df_CONDITION_VISIT["visit_end_datetime"][index] = date_calculated


# # df_CONDITION_VISIT[df_CONDITION_VISIT.columns[0:16]].to_csv("../data/CONDITION.csv", index = False, header=True)

# selected_cols = [col for col in df_CONDITION_VISIT.columns if col in condition_header]
# df_CONDITION = pd.DataFrame(df_CONDITION_VISIT, columns=selected_cols)
# df_CONDITION.to_csv("../data/CONDITION.csv", index = False, header=True)


#              ################## MEASUREMENT - VISIT ################################

# df_MEASUREMENT_VISIT = df_MEASUREMENT_VISIT.where(pd.notnull(df_MEASUREMENT_VISIT), None)


# for index, row in df_MEASUREMENT_VISIT.iterrows():

#     if row["visit_type_concept_id"] == None:
#         df_MEASUREMENT_VISIT["visit_type_concept_id"][index] = "32879" 

#     if row["visit_concept_id"] == None:
#         df_MEASUREMENT_VISIT["visit_concept_id"][index] = "38004515" 

#     date_string = df_MEASUREMENT_VISIT["measurement_date"][index]
#     date_calculated = TableEdition.date2datetime(date_string)
#     df_MEASUREMENT_VISIT["measurement_datetime"][index] = date_calculated

#     date_string = df_MEASUREMENT_VISIT["visit_start_date"][index]
#     date_calculated = TableEdition.date2datetime(date_string)
#     df_MEASUREMENT_VISIT["visit_start_datetime"][index] = date_calculated

#     date_string = df_MEASUREMENT_VISIT["visit_end_time"][index]
#     date_calculated = TableEdition.date2datetime(date_string)
#     df_MEASUREMENT_VISIT["visit_end_datetime"][index] = date_calculated


# selected_cols = [col for col in df_MEASUREMENT_VISIT.columns if col in measurement_header]
# df_MEASUREMENT = pd.DataFrame(df_MEASUREMENT_VISIT, columns=selected_cols)
# df_MEASUREMENT.to_csv("../data/MEASUREMENT.csv", index = False, header=True)

#                             ################# VISIT #######################



# selected_cols = [col for col in df_MEASUREMENT_VISIT.columns if col in visit_header]
# df_VISIT_M = pd.DataFrame(df_MEASUREMENT_VISIT, columns=selected_cols)

# selected_cols = [col for col in df_CONDITION_VISIT.columns if col in visit_header]
# df_VISIT_C = pd.DataFrame(df_CONDITION_VISIT, columns=selected_cols)


# df_VISIT = pd.concat([df_VISIT_C, df_VISIT_M])
# df_VISIT.to_csv("../data/VISIT.csv", index = False, header=True)



