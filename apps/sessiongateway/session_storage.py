import string
import json
import time
from datetime import datetime
import random 
from apps.DBUtils.sql_utils import excecuteFetchoneQuery,excecuteInsertQuery,excecuteUpdateQuery
from apps.Utils.date_time_utils import isNewDay
import logging



#log = configLogger(logging.getLogger(__name__))

#Method to create session on successfull login
def fetchSession(userId,appId):
    sessionId = fetchSessionIfExsists(userId,appId)
    if sessionId == "" :
        sessionId = createSession(userId,appId)
    return sessionId


#method to fetch session as it already exsist's
def fetchSessionIfExsists(userId,appId):
    logging.debug("fetchSessionIfExsists")
    sessionId = ""
    result = fetchSessionDataExsists(userId,appId)
    if result != "" and result is not None :
        sessionId =  result["SESSION_ID"]
        logging.debug("Session id exsists and updating the last request and last login")
        updateReq = updateSessiononLogin(userId,appId,sessionId)
        logging.debug("updateReq" + str(updateReq))
        if (not updateReq):
            sessionId = ""
    else:
            logging.debug("Since session Id is null delete the record")
            excecuteUpdateQuery("DELETE FROM TB_USER_LAST_LOGIN WHERE USER_ID = '" + userId  + "' AND APP_ID = '" + appId + "'" )
    
    return sessionId

#fetch session data of particular user 
def fetchSessionDataExsists(userId,appId):
    sessionData = ""
    result = excecuteFetchoneQuery("SELECT * FROM TB_USER_LAST_LOGIN where user_id like '" + userId + "' and app_id like '" + appId + "'" )
    if result != "" and result is not None :
        if result["SESSION_ID"] != "" and result["SESSION_ID"] is not None:
            sessionData = result
    return sessionData

#fetch session data of particular user 
def checkfetchSessionDataExsists(userId,appId,sessionId):
    sessionData = ""
    result = excecuteFetchoneQuery("SELECT * FROM TB_USER_LAST_LOGIN where user_id like '" + userId + "' and app_id like '" + appId + "' AND SESSION_ID = '" + sessionId + "'"  )
    if result != "" and result is not None :
        if result["SESSION_ID"] != "" and result["SESSION_ID"] is not None:
            sessionData = result
    return sessionData

#method to create session as it dosen't exsist's
def createSession(userId,appId):
    try:
        logging.debug("Inside create new session")
        currdate = time.strftime('%Y-%m-%d %H:%M:%S')
        rad = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 6)) 
        session_id = userId + appId + rad
        device_id = "TEMP"
        #login_time = ""
        #last_request_time = ""
        #create_ts = ""
        query = "INSERT INTO TB_USER_LAST_LOGIN (USER_ID,APP_ID,DEVICE_ID,SESSION_ID,LOGIN_TIME,LAST_REQ_TIME,CREATE_TS) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        values = (userId,appId,device_id,session_id,currdate,currdate,currdate)
        result = excecuteInsertQuery(query,(values))
        if result == True:
            logging.debug("result for fetchsessionId" + str(result))
        else:
            logging.debug("Not able to create session")
    except Exception as e: 
        logging.debug(e)
    return session_id
    
# update the session time
def updateSessiononLogin(userId,appId,sessionId):
    sessionUpdated = False
    currdate = time.strftime('%Y-%m-%d %H:%M:%S')
    logging.debug("Session id exsists and updating the last request and last login")
    sessionUpdated = excecuteUpdateQuery("UPDATE TB_USER_LAST_LOGIN SET LAST_REQ_TIME = '" + currdate + "' , LOGIN_TIME = '" + currdate + "' WHERE USER_ID = '" + userId  + "' AND APP_ID = '" + appId + "' AND SESSION_ID = '" + sessionId + "'" )
    return sessionUpdated

# update the session time
def updateSession(userId,appId,sessionId):
    logging.debug("update session")
    sessionUpdated = False
    currdate = time.strftime('%Y-%m-%d %H:%M:%S')
    logging.debug("Session id exsists and updating the last request and last login")
    sessionUpdated = excecuteUpdateQuery("UPDATE TB_USER_LAST_LOGIN SET LAST_REQ_TIME = '" + currdate + "' WHERE USER_ID = '" + userId  + "' AND APP_ID = '" + appId + "' AND SESSION_ID = '" + sessionId + "'" )
    return sessionUpdated

# update the session expiry
def updatesessionExpiry(userId,appId):
    sessionUpdated = False
    sessionUpdated = excecuteUpdateQuery("DELETE FROM TB_USER_LAST_LOGIN WHERE USER_ID = '" + userId  + "' AND APP_ID = '" + appId + "'" )
    return sessionUpdated

#delete session
def deleteSession(userId,appId,sessionId):
    sessionUpdated = False
    sessionUpdated = excecuteUpdateQuery("DELETE FROM TB_USER_LAST_LOGIN WHERE USER_ID = '" + userId  + "' AND APP_ID = '" + appId + "' AND SESSION_ID = '" + sessionId + "'"  )
    return sessionUpdated