from typing import List, Dict, Any

import matplotlib
import numpy
import pandas
from fastapi import FastAPI
import uvicorn
from models import JobMappingGithubS2, JobMappingKaggleS1, JobMappingGithubS4, JobMappingKaggleS3, \
    SearchJobRequestModel, CompanyMappingDS2, SearchCompanyRequestModel, job_col_mappings, DBMapping
from data_handlers import job_search_results, company_search_results, \
    job_addition, job_addition_to_existing, delete_job_source, delete_from_existing_table

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Website is live. Please enter /docs to access the APIs"}


@app.post("/v1/search/jobs")
async def search_jobs(job_request: SearchJobRequestModel) -> List[Dict[str, Any]]:
    query_dict = dict(job_request)
    print(query_dict)
    new_query = {}
    for keys in query_dict.keys():
        if query_dict[keys] not in ['', 0, 'string']:
            new_query[keys] = query_dict[keys]
    print(new_query)
    return job_search_results(new_query)


@app.post("/v1/search/company")
async def search_company(company_request: SearchCompanyRequestModel) -> List[Dict[str, Any]]:
    query_dict = dict(company_request)
    print(query_dict)
    new_query = {}
    for keys in query_dict.keys():
        if query_dict[keys] not in ['', 0, 'string']:
            new_query[keys] = query_dict[keys]
    print(new_query)
    return company_search_results(new_query)


@app.post("/v1/add/new_job")
async def add_job(add_job_request: SearchJobRequestModel) -> List[Dict[str, Any]]:
    query_dict = dict(add_job_request)
    print(query_dict)
    return job_addition(query_dict)


@app.post("/v1/add/new_job_existing_table")
async def add_job(add_job_request: SearchJobRequestModel, table: DBMapping) -> List[Dict[str, Any]]:
    query_dict = dict(add_job_request)
    print(query_dict)
    return job_addition_to_existing(query_dict, table)


@app.post("/v1/delete/data_source")
async def delete_source(table: DBMapping) -> str:
    table_name = table
    return delete_job_source(table_name)


@app.post("/v1/delete/query")
async def delete_query(delete_request: SearchJobRequestModel) -> List[Dict[str, Any]]:
    query_dict = dict(delete_request)
    new_query = {}
    for keys in query_dict.keys():
        if query_dict[keys] not in ['', 0, 'string']:
            new_query[keys] = query_dict[keys]
    print(new_query)
    return delete_from_existing_table(new_query)

# {
#   "_id": {
#     "$oid": "650c2d4a8b1b1bc972dd91e2"
#   },
#   "job_ID": {
#     "$numberLong": "3467802155"
#   },
#   "job": "Informatica Developer",
#   "location": "Hyderabad, Telangana, India",
#   "company_name": "Tata Consultancy Services",
#   "work_type": "On-site",
#   "full_time_remote": "Full-time · Mid-Senior level",
#   "no_of_employ": "10,001+ employees · IT Services and IT Consulting",
#   "no_of_application": 32,
#   "posted_day_ago": "4 hours",
#   "alumni": "10,073 company alumni",
#   "Hiring_person": "Priyanka gupta",
#   "linkedin_followers": "11,917,646 followers",
#   "hiring_person_link": "https://www.linkedin.com/in/priyanka-gupta-47ba171b1",
#   "job_details": "About the job Greetings from TATA Consultancy Services TCS is hiring for Informatica Developer Job Title: Informatica Developer Location: PAN India Experience Range: 2-6 Years Education: Minimum 15 Years of full time education(10th, 12th and Graduation) Job Description: TCS has always been in the spotlight for being adept in the next big technologies. What we can offer you is a space to explore varied technologies and quench your techie soul. Responsibilities: Good Knowledge in Data Warehouse and Database concepts.Expert in Informatica Power center concepts.Gather requirements to define data definitions, transformation logic, and data model logical and physical designs, data flow, and process.Design, develop, and test data processes per business requirements, following the development standards and best practices as well as participate in code peer reviews to ensure our applications comply with best practices.Work with business analysts to gather business requirements from end users and translate them into technical specifications.To be responsible for providing technical guidance / solutions.Provide estimates for development.Test solutions to validate whether requirements have been met; develop test plans, test scripts, and test conditions based on the business and system requirements. Skills: Experience in ETL development using Informatica PowerCenter, PowerCenter 9.x, 10.xExperience in Designing Extract Load Transform ETL solutions for data migration or data integrationExperience in Structure Query Language SQLStrong Informatica technical knowledge in the areas on Informatica Designer Components -Source Analyzer, Mapping Designer & Mapplet Designer, Transformation Developer, Workflow Manager, Workflow Monitor.Analyze, design, implement and test medium to complex mappings independently. Ability to design and implement easily scalable ETL componentsStrong SQL and related skills. Ability to develop and implement complex procedures and packages using Oracle PL/SQL.Experience in parameter file concepts.Experience in transformations like Source qualifier, joiners, union, aggregator, sorter, expression, transaction control, XML transformation, lookups, etcExperience with Informatica Advanced Techniques Dynamic Caching, Memory Management, Parallel Processing to increase Performance throughput"
# }


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
