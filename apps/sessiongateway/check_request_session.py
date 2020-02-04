import json
import string
from datetime import datetime
from apps.sessiongateway.session_storage import checkfetchSessionDataExsists,updateSession,updatesessionExpiry
from apps.DBUtils.sql_utils import excecuteFetchoneQuery
from apps.Utils.date_time_utils import isNewDay


#validate session with sessionId
def validateSession(userId,appId,sessionId):
    print("validate user")
    sessionValid = True
    result = checkfetchSessionDataExsists(userId,appId,sessionId)
    if result != "" and result is not None :
        sessionInsec = (datetime.now() - result["LAST_REQ_TIME"]).total_seconds()
        lastloginInSec = (datetime.now() - result["LOGIN_TIME"]).total_seconds()
        config = excecuteFetchoneQuery("SELECT * FROM TB_APP_CONFIGS where app_id like '" + appId +  "'"  )
        if config != "" and config is not None :
            sessionExpiry = config["SESSION_TIMEOUT"]
            loginExpiry = config["LOGIN_TIMEOUT"]
            newExpiry = config["NEW_DAY_EXPIRY"]
            isNewExpiry = isNewDay(result["LOGIN_TIME"],newExpiry)
            if result["SESSION_ID"] == sessionId and sessionInsec > sessionExpiry and lastloginInSec > loginExpiry and  (not isNewExpiry):
                updatesessionExpiry(userId,appId)
                sessionValid = False
            else:
                updateSession(userId,appId,sessionId)
        else:
             sessionValid = False     
    else:
        sessionValid = False
    return sessionValid