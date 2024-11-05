import os
import sys

from fortifyapi.fortify import FortifyApi
import requests
from os import environ
import argparse
import json

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


# Set vars for connection
url = os.getenv('FORTIFY_URL') or eprint('FORTIFY_URL not set')
token = os.getenv('FORTIFY_TOKEN') or eprint('FORTIFY_TOKEN not set')

if url is None or token is None or url == "" or token == "":
    eprint('FORTIFY_URL or FORTIFY_TOKEN not set')
    sys.exit(os.EX_CONFIG)

default_id = "d4e30a50-d849-4ca4-bcd3-8415b7d586be"  # NOT A SECRET VALUE, SIMPLY A STATIC ID



def api():
    api = FortifyApi(host=url, token=token, verify_ssl=False)
    return api


def get_application_id(app_name: str) -> int:
    response = requests.get(f"{url}/api/v1/projects", params={'q': f"name:\"{app_name}\""},
                            headers={'Accept': 'application/json',
                                'Authorization': f'FortifyToken {token}'})
    data = response.json()
    if response.status_code != 200:
        eprint(f"Error getting application id! Fortify Server response: {response}. If you are receiving a 401 response the token for your organization may be out of date. Please contact your org's security champion with your org name.")

    if "count" in data and data["count"] >= 1:
        return data["data"][0]["id"]
    return None


def get_version_id(app_id: int, version_name: str) -> int:
    response = requests.get(f"{url}/api/v1/projects/{app_id}/versions/", params={'q': f"name:\"{version_name}\""},
                            headers={'Authorization': f'FortifyToken {token}'})

    data = response.json()
    if response.status_code != 200:
        eprint(f"Error getting version id. Fortify Server response: {response} {data}")

    if "count" in data and data["count"] >= 1:
        return data["data"][0]["id"]
    return None


def get_or_create_application_version(app_name, version_name, description, template_id=default_id) -> int:
    session = requests.Session()
    session.headers.update({'Content-Type': 'application/json'})

    app_id = get_application_id(app_name)
    if app_id:
        eprint("Application exists")
        version_id = get_version_id(app_id, version_name)
        if version_id:
            eprint("Version exists")
            return {"app_id": app_id, "version_id": version_id}
    fortify = api()

    # **application_name is ignored when application_id is given.**
    # so if application_name: "foo_not_existing" but application_id="xxxx"
    # and xxx exists, a new version inside xxxx is created.
    # if application_id is present but doesn't exist, the application is not created either
    # If application_id is not given, a new application named app_name is created
    response = fortify.create_application_version(app_name,
                                                  "Trend Standard Template",
                                                  version_name,
                                                  description=description,
                                                  application_id=app_id,
                                                  issue_template_id=template_id)

    if response.response_code == -1:
        eprint(f"Error creating application version (bulk). Fortify Server response: {response}")
        return {"app_id": None, "version_id": None}

    app_id = get_application_id(app_name)
    version_id = get_version_id(app_id, version_name)

    data = {"requests": [
        {"uri": f"{url}/api/v1/projectVersions/{version_id}/attributes",
         "httpVerb": "POST", "postData": {"values": [{"guid": "Active"}], "attributeDefinitionId": 5}
         },

        {"uri": f"{url}/api/v1/projectVersions/{version_id}/attributes",
         "httpVerb": "POST", "postData": {"values": [{"guid": "Internal"}], "attributeDefinitionId": 6}
         },

        {"uri": f"{url}/api/v1/projectVersions/{version_id}/attributes",
         "httpVerb": "POST", "postData": {"values": [{"guid": "externalpublicnetwork"}], "attributeDefinitionId": 7}
         },

        {"uri": f"{url}/api/v1/projectVersions/{version_id}/attributes",
         "httpVerb": "POST", "postData": {"values": [{"guid": "ApplicationComponent"}], "attributeDefinitionId": 8}
         },

        {"uri": f"{url}/api/v1/projectVersions/{version_id}/attributes",
         "httpVerb": "POST", "postData": {"values": [{"guid": "NA"}], "attributeDefinitionId": 9}
         },

        {"uri": f"{url}/api/v1/projectVersions/{version_id}/attributes",
         "httpVerb": "POST", "postData": {"values": [{"guid": "API"}], "attributeDefinitionId": 10}
         },

        {"uri": f"{url}/api/v1/projectVersions/{version_id}/attributes",
         "httpVerb": "POST", "postData": {"values": [{"guid": "WS"}], "attributeDefinitionId": 10}
         },

        # TODO: determine if it's worth setting language values here as well.

        {"uri": f"{url}/api/v1/projectVersions/{version_id}/attributes",
         "httpVerb": "POST", "postData": {"values": [{"guid": "None"}], "attributeDefinitionId": 12}
         },

        # TODO: replace "all of CA DS" id 1245 with series of calls for repo members, give repo owner
        # ownership of project. This cannot be done at the moment with the permissions for the service account
        {"uri": f"{url}/api/v1/projectVersions/{version_id}/authEntities",
         "httpVerb": "PUT", "postData": [{"id": "1245", "isLdap": "true"}]
         },

        {"uri": f"{url}/api/v1/projectVersions/{version_id}/resultProcessingRules",
         "httpVerb": "PUT", "postData": [
            {"identifier": "com.fortify.manager.BLL.processingrules.FileCountProcessingRule", "enabled": "false"},
            {"identifier": "com.fortify.manager.BLL.processingrules.LOCCountProcessingRule", "enabled": "false"},
        ]
         },

        {"uri": f"{url}/api/v1/projectVersions/{version_id}",
         "httpVerb": "PUT", "postData": {"committed": "true"}
         },

    ]
    }

    response = requests.post(f"{url}/api/v1/bulk",
                             data=json.dumps(data),
                             headers={'Authorization': f'FortifyToken {token}', 'Content-Type': 'application/json'})

    return {"app_id": app_id, "version_id": version_id}


def cli():
    """
    Parse command line arguments and invoke get_or_create_application_version
    """
    jid_desc = "PDG_XXXXXX - identifier added to version description, used to synchronized with dashboard. Please set manually if not set upon creation. Consult #rdsec with this message if needed."
    parser = argparse.ArgumentParser(
        description="""Print Fortify application and version ids of given fortify application name and version names. Create version and application if they don't exist.
        Requires environment variables 'FORTIFY_TOKEN' and 'FORTIFY_URL' to be set.  
        FORTIFY_TOKEN must be an automation token for a (service) account capable of creating a version and assign users to versions.
        FORTIFY_URL is the base url for the fortify service (e.g. https://codescan-ssc.mycompany.com/ssc) . It does not include the path to the api endpoing e.g. 'api/v1'. 
        """)
    parser.add_argument("app_name", help="application name")
    parser.add_argument("version_name", help="version name")
    parser.add_argument("--jid", help=jid_desc, required=False, default=jid_desc )
    args = parser.parse_args()
    try:
        print(get_or_create_application_version(args.app_name, args.version_name,args.jid))
    except Exception as e:
        eprint(e)
        sys.exit(os.EX_CONFIG)


if __name__ == '__main__':
    cli()
