import json
import logging

from apps.usermaintainance.login_user import login_user,logout_user
from apps.itemdata.items import fetchItems
from apps.sessiongateway.check_request_session import validateSession
from apps.usermaintainance.create_user import create_user
from apps.Utils.formresponse import formHdrResp,formScssResp
from apps.Utils.message_constants import INVALID_SESSION,INVALID_REQUEST,BAD_REQUEST
from apps.Utils.server_constants import SVR_CREATEUSER,SVR_LOG_OUT,SVR_LOG_IN,SVR_CHNG_PASS,FETCH_ITEMS

def routeRequest(reqjson,header):
    #req = json.dumps(reqjson)
    req = reqjson
    respjson  = {"resp":{},"hdrResp":formHdrResp("000","true")}
    userid = req["datahdr"]["userid"]
    appid = req["datahdr"]["appid"]
    sessionId = req["datahdr"]["sessionid"]
    try:
        reqDetails = req['requestDetails']
        reqId = req['requestDetails']['requestId']
        if reqId == SVR_LOG_IN:
            logging.debug("Login")
            logging.debug(json.dumps(req))
            userid = req["requestData"]["userid"]
            logging.debug("user Id " + userid)
            respjson["resp"] = login_user(req,userid,appid)
        elif reqId == SVR_LOG_OUT:
            respjson["resp"] = logout_user(userid,appid,sessionId)
        elif reqId == FETCH_ITEMS:
            respjson["resp"] = fetchItems()
        elif req['requestDetails']['session'] == True:
            sessionvalid = validateSession(userid,appid,sessionId)
            logging.debug(str(sessionvalid))
            if sessionvalid:
                logging.debug("A valid session")
                if reqId == SVR_CHNG_PASS:
                    respjson["resp"] = formScssResp("000","Success","changepassword",{})
                elif reqId == SVR_CREATEUSER:
                    logging.debug("create user")
                    respjson["resp"] = create_user(reqDetails)
            else :
                respjson["hdrResp"] = formHdrResp("006",INVALID_SESSION)
        else:
            logging.debug("Requests without interfaces")
            respjson["hdrResp"] = formHdrResp("007",INVALID_REQUEST)
    except:
        logging.debug("Exception " + e.msg)
        respjson["hdrResp"] = formHdrResp("007",BAD_REQUEST)
    
    return respjson


