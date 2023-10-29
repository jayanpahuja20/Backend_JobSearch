from typing import Dict, Union, Type, Any

from pymongo import MongoClient
from models import JobMappingGithubS2, JobMappingKaggleS1, JobMappingGithubS4, JobMappingKaggleS3, \
    SearchJobRequestModel, CompanyMappingDS2, SearchCompanyRequestModel, DataBaseMapModel, job_col_mappings , DB_Class_Mappings

from bson import ObjectId, json_util
import json

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from fuzzywuzzy import fuzz

connection_string = "mongodb+srv://jayan20071:jayanpahuja123@jobsearch.y4tc9qr.mongodb.net/"
newconnection = "mongodb+srv://admin:weloveIIA@jobs.dohb4ca.mongodb.net/"

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)
    
def get_DB(DB_Name):
    if(DB_Name in ["Kaggle_S1", "Github_S2", "Kaggle_S3", "Github_S4"]):
        connection_string = "mongodb+srv://jayan20071:jayanpahuja123@jobsearch.y4tc9qr.mongodb.net/"
    elif(DB_Name == "NewJobs"):
        connection_string = "mongodb+srv://admin:weloveIIA@jobs.dohb4ca.mongodb.net/"
    elif (DB_Name == "DS_2"):
        connection_string = "mongodb+srv://jayan20071:jayanpahuja123@jobsearch.y4tc9qr.mongodb.net/"
        client = MongoClient(connection_string)
        db = client[DataBaseMapModel.company]
        collection = db[DB_Name]
        return collection
    client = MongoClient(connection_string)
    db = client[DataBaseMapModel.job]
    collection = db[DB_Name]
    return collection

def Transform(DatasetName , query):
    if(type(query)!=dict):
        query = query[0]
    Transformed={}
    for enum_val in DB_Class_Mappings[DatasetName]:
        if(enum_val.value==""):
            print(enum_val.value)
            Transformed[enum_val.name] = ""
        else:
            Transformed[enum_val.name] = query[enum_val.value]
    
    L = []
    L.append(Transformed)
    return L

def DB_Match(query , DB_Name ):
    Database = get_DB(DB_Name)
    cursor = Database.find({})
    query = Transform(DB_Name , query)[0]
    
    
    for entry in cursor:
        entry = Transform(DB_Name, entry)[0]
        
        if(entity_matching(query , entry)):
           return True

    return False  
 
        
def entity_matching (row1 , row2, threshold_tfidf=0.5, threshold_fuzzy=60):
    if(not(row1) or not(row2)):
        return False
    
    # Convert dictionaries to DataFrames
    df1 = pd.DataFrame([row1])
    df2 = pd.DataFrame([row2])

    # Create a 'text' column by concatenating values in each row
    df1['text'] = df1.apply(lambda row: ' '.join(row.astype(str)), axis=1)
    df2['text'] = df2.apply(lambda row: ' '.join(row.astype(str)), axis=1)

    # Create TF-IDF vectorizers
    tfidf_vectorizer = TfidfVectorizer()
    
    # Fit and transform the text data in the table
    tfidf_matrix_table = tfidf_vectorizer.fit_transform(df2["text"])
    
    # Transform the text data in the query
    tfidf_matrix_query = tfidf_vectorizer.transform(df1["text"])
    
    # Compute the cosine similarities between the query and table using TF-IDF
    cosine_sim = linear_kernel(tfidf_matrix_query, tfidf_matrix_table)
    
    # Create an empty list to store matching rows
    matching_rows = []
    
    # Iterate through the similarity matrix and apply FuzzyWuzzy matching
    for i in range(len(cosine_sim[0])):
        similarity_tfidf = cosine_sim[0][i]
        if similarity_tfidf > threshold_tfidf:
            key_query, value_query = row1.popitem()
            key_table, value_table = row2.popitem()
            # Use FuzzyWuzzy to compare 
            value_similarity = fuzz.token_sort_ratio(value_query, value_table)
            if value_similarity > threshold_fuzzy:
                matching_rows.append((key_query, value_query, key_table, value_table, similarity_tfidf, value_similarity))
    
    # Return the matching rows
    return bool(matching_rows)


def entity_matching_old(query, table, threshold_tfidf=0.5, threshold_fuzzy=60):
    
    # Create a 'text' column in the table by concatenating selected columns
    table['text'] = table.apply(lambda row: ' '.join(row.astype(str)), axis=1)
    
    # Convert the query dictionary into a Pandas DataFrame with a single row
    query_df = pd.DataFrame([query])
    
    # Preprocess the data to handle missing values and ensure they are represented as strings
    query_df = query_df.fillna('')
    query_df['text'] = query_df.apply(lambda row: ' '.join(row.astype(str)), axis=1)
    
    # Create TF-IDF vectorizers
    tfidf_vectorizer = TfidfVectorizer()
    
    # Fit and transform the text data in the table
    tfidf_matrix_table = tfidf_vectorizer.fit_transform(table['text'])
    
    # Transform the text data in the query
    tfidf_matrix_query = tfidf_vectorizer.transform(query_df['text'])
    
    # Compute the cosine similarities between the query and table using TF-IDF
    cosine_sim = linear_kernel(tfidf_matrix_query, tfidf_matrix_table)
    
    # Create an empty list to store matching rows
    matching_rows = []
    
    # Iterate through the similarity matrix and apply FuzzyWuzzy matching
    for i in range(len(cosine_sim[0])):
        similarity_tfidf = cosine_sim[0][i]
        if similarity_tfidf > threshold_tfidf:
            name_query = query['text']
            name_table = table.iloc[i]['text']
            # Use FuzzyWuzzy to compare 
            name_similarity = fuzz.token_sort_ratio(name_query, name_table)
            if name_similarity > threshold_fuzzy:
                matching_rows.append((i, similarity_tfidf, name_similarity))
    
    # Return the matching rows
    return bool(matching_rows)


def entity_matching_for_search(query,results):
    if(not results):
        return False
    for result in results:
        if(entity_matching(query,result)):
            return True
    return False

def job_search_results(query_dict: Dict[str, Any]):
    try:
        final_results = []
        for key in ["Kaggle_S1", "Github_S2", "Kaggle_S3", "Github_S4" , "NewJobs"]:
            flag = True
            query_for_db = {}
            collection_name = key
            
            for enum_val in job_col_mappings[key]:
                if ("" + enum_val.name) in query_dict.keys():
                    if enum_val.value == "":
                        flag = False
                        break
                    query_for_db[enum_val.value] = query_dict["" + enum_val.name]
            
            if flag:
                collection = get_DB(collection_name)
                results = list(collection.find(query_for_db))
                if(not results):
                    continue
                
                results=Transform(key,results)
                if(not entity_matching_for_search(results,final_results)):
                    final_results.extend(results)
                else:
                    print("Duplicate result")
                    
                
                   
        
    
        for i in range(0, len(final_results)):
            dump = json.dumps(final_results[i], default=str)
            final_results[i] = json.loads(dump)
            
        return final_results

    except Exception as e:
        print("Error:", str(e))
        return []


def company_search_results(query_dict: Dict[str, Any]):
    try:
        client = MongoClient(connection_string)
        db = client[DataBaseMapModel.company]
        final_results = []
        for key in ["DS_2"]:
            flag = True
            query_for_db = {}
            collection_name = key
            if key == "DS_2":
                for enum_val in CompanyMappingDS2:
                    if ("" + enum_val.name) in query_dict.keys():
                        if enum_val.value == "":
                            flag = False
                            break
                        query_for_db[enum_val.value] = query_dict["" + enum_val.name]
            # print(query_dict)
            # print(query_for_db)
            if flag:
                collection = db[collection_name]
                results = list(collection.find(query_for_db))
                if(not results):
                    continue
                results=Transform(key,results)
                if(not entity_matching_for_search(results,final_results)):
                    final_results.extend(results)
                else:
                    print("Duplicate result")
                
        
        for i in range(0, len(final_results)):
            dump = json.dumps(final_results[i], default=str)
            final_results[i] = json.loads(dump)
        return final_results

    except Exception as e:
        print("Error:", str(e))
        return []

def job_addition(query_dict: Dict[str, Any]):
     
    collection = get_DB('NewJobs')
    if(not DB_Match(query_dict,"NewJobs")):
        result = collection.insert_one(query_dict)
    else:
        print("Duplicate entry")
    return []
if __name__ == "__main__":
    #DB_Match("hlelo" ,"NewJobs"  )
    Database = get_DB("NewJobs")


