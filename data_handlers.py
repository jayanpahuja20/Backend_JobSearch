from typing import Dict, Union, Type, Any

from pymongo import MongoClient
from models import JobMappingGithubS2, JobMappingKaggleS1, JobMappingGithubS4, JobMappingKaggleS3, \
    SearchJobRequestModel, CompanyMappingDS2, SearchCompanyRequestModel, DataBaseMapModel

from bson import ObjectId, json_util
import json

connection_string = "mongodb+srv://jayan20071:jayanpahuja123@jobsearch.y4tc9qr.mongodb.net/"


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
            if key == "Kaggle_S1":
                for enum_val in JobMappingKaggleS1:
                    if ("" + enum_val.name) in query_dict.keys():
                        if enum_val.value == "":
                            flag = False
                            break
                        query_for_db[enum_val.value] = query_dict["" + enum_val.name]
            elif key == "Github_S2":
                for enum_val in JobMappingGithubS2:
                    if ("" + enum_val.name) in query_dict.keys():
                        if enum_val.value == "":
                            flag = False
                            break
                        query_for_db[enum_val.value] = query_dict["" + enum_val.name]
            elif key == "Kaggle_S3":
                for enum_val in JobMappingKaggleS3:
                    if ("" + enum_val.name) in query_dict.keys():
                        if enum_val.value == "":
                            flag = False
                            break
                        query_for_db[enum_val.value] = query_dict["" + enum_val.name]
            elif key == "Github_S4":
                for enum_val in JobMappingGithubS4:
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
