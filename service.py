from typing import List, Dict, Any

import matplotlib
import numpy
import pandas
from fastapi import FastAPI
import uvicorn
from models import JobMappingGithubS2, JobMappingKaggleS1, JobMappingGithubS4, JobMappingKaggleS3, \
    SearchJobRequestModel, CompanyMappingDS2, SearchCompanyRequestModel, job_col_mappings
from data_handlers import job_search_results,company_search_results,job_addition

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
        if query_dict[keys] not in ['', 0]:
            new_query[keys] = query_dict[keys]
    print(new_query)
    return job_search_results(new_query)


@app.post("/v1/search/company")
async def search_company(company_request: SearchCompanyRequestModel) -> List[Dict[str, Any]]:
    query_dict = dict(company_request)
    print(query_dict)
    new_query = {}
    for keys in query_dict.keys():
        if query_dict[keys] not in ['', 0]:
            new_query[keys] = query_dict[keys]
    print(new_query)
    return company_search_results(new_query)

@app.post("/v1/add/job")
async def add_job(add_job_request: SearchJobRequestModel) -> List[Dict[str, Any]]:
    query_dict = dict(add_job_request)
    print(query_dict)
    return job_addition(query_dict)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
