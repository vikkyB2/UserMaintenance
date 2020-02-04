import json



def formHdrResp(code,message):
    rslt = {"code":code,"message":message}
    return rslt

def formErrResp(code,message,responseNode,responseObj):
    rslt = {"code":code,"message":message,"response":{}}
    rslt["response"] = responseObj
    finalRslt = {}
    finalRslt[responseNode] = rslt
    return finalRslt

def formScssResp(code,message,responseNode,responseObj):
    rslt = {"code":code,"message":message,"response":{}}
    rslt["response"] = responseObj
    finalRslt = {}
    finalRslt[responseNode] = {}
    finalRslt[responseNode] = rslt
    return finalRslt

def updateRespJson(resp,responseNode,responseObj):
    resp[responseNode]['response'] = responseObj
    return resp
