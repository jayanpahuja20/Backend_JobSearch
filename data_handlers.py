from typing import Dict, Union, Type, Any

from pymongo import MongoClient
from models import JobMappingGithubS2, JobMappingKaggleS1, JobMappingGithubS4, JobMappingKaggleS3, \
    SearchJobRequestModel, CompanyMappingDS2, SearchCompanyRequestModel, DataBaseMapModel, job_col_mappings

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


def job_search_results(query_dict: Dict[str, Any]):
    try:
        client = MongoClient(connection_string)
        db = client[DataBaseMapModel.job]
        final_results = []
        for key in ["Kaggle_S1", "Github_S2", "Kaggle_S3", "Github_S4"]:
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
                collection = db[collection_name]
                results = list(collection.find(query_for_db))
                print(results)
                final_results.extend(results)
        print(final_results)
        for i in range(0, len(final_results)):
            dump = json.dumps(final_results[i], default=str)
            final_results[i] = json.loads(dump)
            print(type(final_results[i]))
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
                print(results)
                final_results.extend(results)
        print(final_results)
        for i in range(0, len(final_results)):
            dump = json.dumps(final_results[i], default=str)
            final_results[i] = json.loads(dump)
            print(type(final_results[i]))
        return final_results

    except Exception as e:
        print("Error:", str(e))
        return []

def job_addition(query_dict: Dict[str, Any]):
    client = MongoClient(newconnection)
    db = client['Jobs'] 
    collection = db['NewJobs']

    result = collection.insert_one(query_dict)
    print(result)
    return []
if __name__ == "__main__":
    query = {"company_name": "CyberCoders", "title": "Senior Data Engineer"}
    database_name = "Jobs"
    column_mappings = {
        "Github_S2": {"title": "title", "company_name": "company", "location": "location", "salary": "None",
                      "eligibility": "education", "job_id": "None", "description": "description",
                      "industry": "Industries", "link": "post_url", "date_posted": "None",
                      "employment_type": "Employment type"}
        # "Github_S4": {"title": "_id", "company_name": "Company", "location": "JobTitle", "salary": "abc", "eligibility": "abc", "job_id": "abc", "description": "abc", "industry": "abc", "link": "abc", "date_posted": "abc", "employment_type": "abc"},
        # "Kaggle_S1": {"title": "_id", "company_name": "Company", "location": "JobTitle", "salary": "abc", "eligibility": "abc", "job_id": "abc", "description": "abc", "industry": "abc", "link": "abc", "date_posted": "abc", "employment_type": "abc"},
        # "Kaggle_S3": {"title": "_id", "company_name": "Company", "location": "JobTitle", "salary": "abc", "eligibility": "abc", "job_id": "abc", "description": "abc", "industry": "abc", "link": "abc", "date_posted": "abc", "employment_type": "abc"},
    }

    collection_keys = ["Github_S2", "Github_S4", "Kaggle_S1", "Kaggle_S3"]
    query_result = job_search_results(database_name)

def entity_matching(query, table, threshold_tfidf=0.5, threshold_fuzzy=60):

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
            name_query = query['name']
            name_table = table.iloc[i]['name']
            # Use FuzzyWuzzy to compare 
            name_similarity = fuzz.token_sort_ratio(name_query, name_table)
            if name_similarity > threshold_fuzzy:
                matching_rows.append((i, similarity_tfidf, name_similarity))
    
    # Return the matching rows
    return bool(matching_rows)
