import json

from apps.sessiongateway.session_storage import fetchSession,deleteSession,checkfetchSessionDataExsists
from apps.Utils.message_constants import BAD_REQUEST,INVALID_PASS,INVALID_REQUEST,INVALID_SESSION,INVALID_USER,LOGGEDOUT_SCSS_MSG,LOGIN_SCSS_MSG,PASSWORD_EXPIERD
from apps.Utils.formresponse import formScssResp,formErrResp,updateRespJson
from apps.DBUtils.sql_utils import excecuteFetchoneQuery
from apps.Utils.date_time_utils import checkExpiry
from apps.Utils.sha256 import hashPinbyKey
#from apps.Utils.logger import configLogger
import logging
import time
import hashlib

#log = configLogger(logging.getLogger(__name__))
# function to login user
def login_user(req,userId,appid):
    logging.debug("Login user")
    pin = req['requestData']['pin']
    result = excecuteFetchoneQuery("""SELECT * FROM "TB_USER_DETAILS" where "USER_ID" like '""" + userId + """' and "APP_ID" like '""" + appid + "'")
    res = authenticate_user(result,userId,appid,pin)
    if res['loginResp']['code'] == "000":
        sessionId = fetchSession(userId,appid)
        res = updateRespJson(res,"loginResp",{"sessionId":sessionId})
    return res

# function to authenticate user
def authenticate_user(result,userId,appid,pin):
    logging.debug("auth user")
    print(result)
    if result != "" and result is not None :
        if result['USER_ID'] != "" and result['PIN'] != "" :
            salt = appid + userId
            hashpin = hashPinbyKey(pin,salt)
            if result['PIN'] == hashpin:
                expierd = pinExpiry(appid,userId)
                if(expierd):
                    res = formScssResp("100",PASSWORD_EXPIERD,"loginResp",{})
                else:
                    res = formScssResp("000",LOGIN_SCSS_MSG,"loginResp",{})
            else:
                res = formErrResp("001",INVALID_PASS,"loginResp",{})
        else:
            res = formErrResp("002",INVALID_PASS,"loginResp",{})
    else:
        res = formErrResp("001",INVALID_USER,"loginResp",{})
    return res

# function to delete user
def logout_user(userId,appId,sessionId):
    logging.debug("log out user")
    res = formScssResp("000",LOGGEDOUT_SCSS_MSG,"logoutResp",{})
    exsistSession = checkfetchSessionDataExsists(userId,appId,sessionId)
    if exsistSession != "" and exsistSession is not None :
        logging.debug("Exsist user session Id ::" +  exsistSession["SESSION_ID"] + "Session Id ::" + sessionId)
        deleteSession(userId,appId,sessionId)
    return res

def pinExpiry(appid,userid):
    logging.debug("pin expiry")
    result = excecuteFetchoneQuery("""SELECT max("CHANGE_TIME") as LAST_MODF FROM "TB_USER_PASSWORDS" where "USER_ID" like '""" + userid + """' and "APP_ID" like '""" + appid + "'")
    if result is not [None] and result is not None :
        logging.debug("No previous password")
        maxModf = result["LAST_MODF"]
        config = excecuteFetchoneQuery("""SELECT * FROM "TB_APP_CONFIGS" where "APP_ID" like '""" + appid +  "'"  )
        if config is not [None] and config is not None :
            passwordExpiry = config["PASS_CHANGE_FREQ"]
            logging.debug(maxModf)
            return checkExpiry(maxModf,passwordExpiry)
        else:
            return True
    else:
        logging.debug("No previous password")
        return False
