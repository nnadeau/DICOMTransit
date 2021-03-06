import requests
import logging
import sys
import os
import json
from dotenv import load_dotenv
from LORIS.helper import is_response_success


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger('LORISQuery')


def login():
    """
    Logs into LORIS using the stored credential. Must use PyCurl as Requests is not working.
    :return: BOOL if or not it is successful. also, the JSON token that is necessary to conduct further transactions.
    """
    logger = logging.getLogger('LORIS_login')

    #Load environmental variables.
    load_dotenv()

    username = os.getenv("LORISusername")
    password = os.getenv("LORISpassword")

    data = json.dumps({"username":username, "password":password})

    #Login URL
    url = os.getenv("LORISurl")
    updated_url = url + 'login'


    # requests style login # NOT WORKING!
    r = requests.post(updated_url, data=data)


    logger.info(str(r.status_code) + r.reason)

    response_json = r.json()

    return is_response_success(r.status_code, 200), response_json.get('token')


def getCNBP(token, endpoint):
    """
    Get from a CNBP LORIS database endpoint
    :param endpoint:
    :return: bool on if such PSCID (INSTITUTIONID + PROJECTID + SUBJECTID) exist already.
    """
    logger = logging.getLogger('LORIS_get')
    logger.info("Getting LORIS endpoing: "+ endpoint + "at")
    load_dotenv()
    url = os.getenv("LORISurl")
    updatedurl = url + endpoint
    logger.info(updatedurl)
    HEADERS = {'Authorization': 'token {}'.format(token)}

    with requests.Session() as s:
        s.headers.update(HEADERS)
        r = s.get(updatedurl)
        logger.info("Get Result:" + str(r.status_code) + r.reason)

        return r.status_code, r.json()


def postCNBP(token, endpoint, data):
    """
    post some data to a LORIS end point.
    :param endpoint:
    :param data:
    :return: bool on if request is successful, r for the request (CAN BE NULL for 201 based requests)
    """
    logger = logging.getLogger('LORIS_post')
    logger.info("Posting data to: "+endpoint)
    logger.info("Data: "+data)
    logger.info("!!!!!!!!!!BEWARE THAT SOME ENDPOINTS HAVE TRAILING SLASH, OTHERS DON'T.!!!!!!!!!!!!!!")
    load_dotenv()
    url = os.getenv("LORISurl")
    updatedurl = url + endpoint

    HEADERS = {'Authorization': 'token {}'.format(token)}

    with requests.Session() as s:
        s.headers.update(HEADERS)
        r = s.post(updatedurl, data=data)
        logger.info("Post Result:" + str(r.status_code) + r.reason)

        return r.status_code, r

def putCNBP(token, endpoint, data):
    """
    Put some data to a LORIS end point.
    :param endpoint:
    :param data:
    :return: bool on if request is successful, r for the request (CAN BE NULL for 201 based requests)
    """
    logger = logging.getLogger('LORIS_put')
    logger.info("Putting data to: "+endpoint)
    logger.info("Data: "+data)
    logger.info("!!!!!!!!!!BEWARE THAT SOME ENDPOINTS HAVE TRAILING SLASH, OTHERS DON'T.!!!!!!!!!!!!!!")

    load_dotenv()
    url = os.getenv("LORISurl")
    updatedurl = url + endpoint

    HEADERS = {'Authorization': 'token {}'.format(token)}

    with requests.Session() as s:
        s.headers.update(HEADERS)
        r = s.put(updatedurl, data=data)
        logger.info("Put Result:" + str(r.status_code) + r.reason)

        return r.status_code, r



# Only executed when running directly.
if __name__ == '__main__':
    #print(login())
    #getCNBP("projects")
    Success, token = login()
    #print("Test complete")