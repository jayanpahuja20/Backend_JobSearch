from typing import List, Dict, Any

import pandas as pd
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from models import JobMappingGithubS2, JobMappingKaggleS1, JobMappingGithubS4, JobMappingKaggleS3, \
    SearchJobRequestModel, CompanyMappingDS2, SearchCompanyRequestModel, job_col_mappings, DBMapping
from data_handlers import job_search_results, company_search_results, \
    job_addition, job_addition_to_existing, delete_job_source, delete_from_existing_table, get_user_data

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/",response_class=HTMLResponse)
async def root(request: Request):
    # return {"message": "Website is live. Please enter /docs to access the APIs"}
    return templates.TemplateResponse("home.html",context={"request":request})


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


@app.post("/v1/add/new_job2")
async def add_job2(add_job_request: SearchJobRequestModel) -> List[Dict[str, Any]]:
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

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", context={"request": request})

@app.get("/signup", response_class=HTMLResponse)
def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", context={"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    print("Hello")
    name = request.query_params.get('name', '')
    email = request.query_params.get('email', '')
    user_data=get_user_data(email)[0]
    # print(user_data)
    location=user_data["location"]
    experience=user_data["eligibility"]
    return templates.TemplateResponse("user_dashboard.html", context={"request": request, "name":name, "email":email, "location":location, "experience":experience})

@app.get("/job_search", response_class=HTMLResponse)
def jobSearch(request: Request):
    return templates.TemplateResponse("JobSearch.html", context={"request": request})

@app.get("/job_search_result",response_class=HTMLResponse)
async def search_jobs( request: Request):
   
    new_query = {}
    new_query["company_name"] = request.query_params.get('company_name', '')
    new_query["title"] = request.query_params.get('title', '')
    new_query["location"] = request.query_params.get('location', '')
    new_query["salary"] = request.query_params.get('salary', '')
    new_query["eligibility"] = request.query_params.get('eligibility', '')
    new_query["description"] = request.query_params.get('description', '')
    new_query["industry"] = request.query_params.get('industry', '')
    new_query["link"] = request.query_params.get('link', '')
    new_query["date_posted"] = request.query_params.get('date_posted', '')
    new_query["employment_type"] = request.query_params.get('employment_type', '')
    
    #print(job_search_results(new_query))
    df = pd.DataFrame.from_dict(job_search_results(new_query))
    html = df.to_html( index=False, classes='stocktable', table_id='table1')
    html = html.replace('class="dataframe ','class="')  
  #  return templates.TemplateResponse("JobSearch.html", context={"request": request})
    return templates.TemplateResponse("result.html", context={"request": request,"table":html})
    

@app.get("/company_search", response_class=HTMLResponse)
def companySearch(request: Request):
    return templates.TemplateResponse("CompanySearch.html", context={"request": request})
@app.get("/company_search_result", response_class=HTMLResponse)
async def search_companies( request: Request):
   
    new_query = {}
    new_query["name"] = request.query_params.get('name', '')
    new_query["domain"] = request.query_params.get('domain', '')
    new_query["year_founded"] = request.query_params.get('year_founded', '')
    new_query["industry"] = request.query_params.get('industry', '')
    new_query["locality"] = request.query_params.get('locality', '')
    new_query["country"] = request.query_params.get('country', '')
    new_query["industry"] = request.query_params.get('industry', '')
    new_query["linkedin_url"] = request.query_params.get('linkedin_url', '')
    new_query["current_employees"] = request.query_params.get('current_employees', '')
    new_query["total_employees"] = request.query_params.get('total_employees', '')
    print(new_query)
    
    #print(job_search_results(new_query))
    df = pd.DataFrame.from_dict(company_search_results(new_query))
    html = df.to_html( index=False, classes='stocktable', table_id='table1')
    html = html.replace('class="dataframe ','class="')  
    #return templates.TemplateResponse("JobSearch.html", context={"request": request})
    return templates.TemplateResponse("result.html", context={"request": request,"table":html})

@app.get("/Recommended", response_class=HTMLResponse)
def RecommendedSearch(request: Request):
    print("Recommended Search")
    email = "yashika20161@iiitd.ac.in"
    user_data=get_user_data(email)[0]
    # print(user_data)
    new_query = {}
    new_query['location']=user_data["location"]
    new_query['eligibility']=user_data["eligibility"]
    print("looking for error")
    print(job_search_results(new_query))
    df = pd.DataFrame.from_dict(job_search_results(new_query))
    html = df.to_html( index=False, classes='stocktable', table_id='table1')
    html = html.replace('class="dataframe ','class="')  
    #return templates.TemplateResponse("JobSearch.html", context={"request": request})
    return templates.TemplateResponse("result.html", context={"request": request,"table":html})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
