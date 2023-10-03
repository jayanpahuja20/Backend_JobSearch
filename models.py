from typing import Final, Any

from pydantic import BaseModel
from enum import Enum


class SearchJobRequestModel(BaseModel):
    title: str
    company_name: str
    location: str
    salary: int
    eligibility: str
    description: str
    industry: str
    link: str
    date_posted: str
    employment_type: str


class SearchCompanyRequestModel(BaseModel):
    name: str
    domain: str
    year_founded: int
    industry: str
    size_range: str
    locality: str
    country: str
    linkedin_url: str
    current_employees: int
    total_employees: int


class JobMappingKaggleS1(Enum):
    title: Final = "job"
    company_name: Final = "company_name"
    location: Final = "location"
    salary: Final = ""
    eligibility: Final = ""
    description: Final = "job_details"
    industry: Final = "no_of_employ"
    link: Final = "job_id"
    date_posted: Final = "posted_day_ago"
    employment_type: Final = "full_time_remote"


class JobMappingKaggleS3(Enum):
    title: Final = "job_title"
    company_name: Final = ""
    location: Final = "location"
    salary: Final = "job_salary"
    eligibility: Final = "job_experience_required"
    description: Final = "job_details"
    industry: Final = "industry"
    link: Final = ""
    date_posted: Final = "crawl_timestamp"
    employment_type: Final = ""


class JobMappingGithubS2(Enum):
    title: Final = "title"
    company_name: Final = "company"
    location: Final = "location"
    salary: Final = "salary"
    eligibility: Final = "months_experience, education, Seniority level"
    description: Final = "description"
    industry: Final = "job_function"
    link: Final = "post_url"
    date_posted: Final = ""
    employment_type: Final = "Employment type"


class JobMappingGithubS4(Enum):
    title: Final = "job_title"
    company_name: Final = "company_name"
    location: Final = "city, state, geo"
    salary: Final = "salary_offered"
    eligibility: Final = ""
    description: Final = "job_description"
    industry: Final = "category"
    link: Final = "url"
    date_posted: Final = "post_date"
    employment_type: Final = "job_type"


class CompanyMappingDS2(Enum):
    name: Final = "name"
    domain: Final = "domain"
    year_founded: Final = "year_founded"
    industry: Final = "industry"
    size_range: Final = "size_range"
    locality: Final = "locality"
    country: Final = "country"
    linkedin_url: Final = "linkedin_url"
    current_employees: Final = "current employee estimate"
    total_employees: Final = "total employee estimate"


class DataBaseMapModel(BaseModel):
    job: Final = "Jobs"
    company: Final = "Companies"

