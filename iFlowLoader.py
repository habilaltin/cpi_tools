import requests as rq
import xmltodict
import re
import time
from pathlib import Path

def get_filename(val):
     """
     Try to get filename from header content-disposition
     """
     not_found = "filename_not_found_"+str(int(time.time()))
     if not val:
         return not_found
     fname = re.findall('filename=(.+)', val)
     if len(fname) == 0:
         return not_found
     fn = fname[0].replace('"','')
     return fn

### Config ###################

# Enter auth. data [Basic: base64_encoded(user:pw)]
secrets = ""

# Enter URL to tenant 
tenantUrl = ""

##############################

#headers
headers =   {
                'authorization': secrets,
                'x-csrf-token': "fetch",
                'cache-control': "no-cache"
            }

#read all integration packages
response = rq.get(url = tenantUrl+"/api/v1/IntegrationPackages", headers=headers)

#save token if needed later
token = response.headers["x-csrf-token"] 

#parse XML
json_object = xmltodict.parse(response.text)

#loop through all integration packages and get data for IntegrationDesigntimeArtifacts
for entry in json_object["feed"]["entry"]:

    #create directory structure if necessary
    #always begins from current dir and creates "backup_iflows"
    Path("backup_iflows/"+entry["m:properties"]["d:Name"]).mkdir(parents = True, exist_ok=True) 

    #get information about design artifacts
    response2 = rq.get(url = entry["id"]+"/IntegrationDesigntimeArtifacts", headers=headers)

    #parse to dict
    json_object2 = xmltodict.parse(response2.text, force_list={"entry": True})

    if "entry" in json_object2["feed"]:
        for entry2 in json_object2["feed"]["entry"]:

            #load zip files from server
            response3 = rq.get(url = entry2["id"]+"/$value", headers=headers)

            #determine filename from header
            filename = get_filename(response3.headers.get('Content-Disposition'))
            
            #save in folder
            open("backup_iflows/"+entry["m:properties"]["d:Name"]+"/"+filename, 'wb').write(response3.content)