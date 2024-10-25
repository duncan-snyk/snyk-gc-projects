import requests
import json
import datetime
import argparse
import os

# Globals set at the command-line
snyk_api_token = ""
org_id = ""
age_days = 2

delete_flag = False
verbose = False

def get_args():
    global snyk_api_token
    global org_id
    global delete_flag
    global age_days
    global verbose

    parser = argparse.ArgumentParser(prog="python3 snyk-gc-projects.py", description = "Scan a Snyk Org for projects and optionally delete any which have not been updated recently")
    parser.add_argument('-o', '--org_id',    required = False, default = os.getenv("SNYK_ORG_ID"))
    parser.add_argument('-t', '--api_token', required = False, default = os.getenv("SNYK_API_TOKEN"))
    parser.add_argument('-a', '--age',       required = False, default = 7, help = "Set the age in days to be considered stale if lastTestedDate is older")
    parser.add_argument('-d', '--delete',    action = "store_true", help = "Delete stale projects")
    parser.add_argument('-v', '--verbose',   action = "store_true", required = False, help = "Print API calls")
    args = parser.parse_args()

    snyk_api_token = args.api_token
    print(f"API_TOKEN::{snyk_api_token}::")
    org_id = args.org_id
    delete_flag = args.delete
    age_days = int(args.age)
    verbose = bool(args.verbose)

    if age_days < 1 :
        print(f"Project age must be greater than one day, {age_days} given")
        raise 

    if snyk_api_token == None:
        print("Snyk API Token is not set. Either supply at the command-line or set the SNYK_API_TOKEN environment variable")
        raise

    if org_id == None:
        print("Snyk Org ID is not set. Either supply at the command-line or set the SNYK_ORG_ID environment variable")
        raise

    if not delete_flag:
        print("********************************************************")
        print(f"* Dry Run     Age = {age_days}")
        print("********************************************************")
    else:
        print("********************************************************")
        print(f"* Deleting    Age = {age_days}")
        print("********************************************************")

def get_base_url(path = ""):
    return f"https://api.snyk.io/rest/orgs/{org_id}{path}"

def get_base_v1_url(path = ""):
    return f"https://api.snyk.io/v1/org/{org_id}{path}"
    
def build_headers():
    headers = {
        "Authorization": f"token {snyk_api_token}"
    }
    return headers

def run_get_request(url):
    if verbose:
        print(f"GET {url}")
    response = requests.get(url, headers=build_headers())
    response.raise_for_status()
    return response.json()

def get_now():
    now = datetime.datetime.today().strftime('%Y-%m-%d')
    return now

# Function to get a list of projects
def get_projects():
    now = get_now()
    json = run_get_request(get_base_url(f"/projects?version={now}"))
    return json['data']

def get_project(pid):
    now = get_now()
    json = run_get_request(get_base_v1_url(f"/project/{pid}?version={now}"))
    return json


# Function to check if a project is outdated
def is_project_outdated(project):
    last_updated = project.get("lastTestedDate")
    if not last_updated:
        return False

    # Convert last_updated to a datetime object
    last_updated_datetime = datetime.datetime.fromisoformat(last_updated)

    if verbose:
        print(last_updated_datetime)

    # Calculate the difference in hours
    time_delta = datetime.datetime.now(datetime.timezone.utc) - last_updated_datetime
    hours_since_update = time_delta.total_seconds() / 3600

    return hours_since_update > age_days * 24

# Function to delete a project
def delete_project(project_id):
    now = get_now()
    response = requests.delete(get_base_url(f"/projects/{project_id}?version={now}"), headers=build_headers())
    response.raise_for_status()

def main():
    get_args()

    projects = get_projects()

    for p in projects:
        project = get_project(p["id"])
        project_id = project["id"]
        project_name = project["name"]
        print(f"Checking project {project_name} / {project_id} : ", end="")
        if is_project_outdated(project):
            if delete_flag:
                print(f"Deleting")
                delete_project(project_id)
            else:
                print("Would delete")
        else:
            print("Active")



if __name__ == '__main__':
    main()