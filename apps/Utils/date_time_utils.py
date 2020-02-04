from datetime import datetime

def isNewDay(dat,newExpiry):
    isNew = False
    date = dat.strftime("%d")
    year = dat.strftime("%Y")
    month = dat.strftime("%m")
    
    tdat = datetime.now()
    tdate = tdat.strftime("%d")
    tyear = tdat.strftime("%Y")
    tmonth = tdat.strftime("%m")

    if newExpiry == "never":
        print("Never")
    elif newExpiry == "daily":
        print(tdate + date + tmonth + month + tyear + year)
        if tdate != date or tmonth != month or tyear != year:
            isNew = True                
    elif newExpiry == "monthly":
        print("Never")    
        if tmonth != month or tyear != year:
            isNew = True 
    elif newExpiry == "yearls":
        print("Never")
        if tyear != month:
            isNew = True 
    return isNew

def checkExpiry(lastMod,expiryDur):
    diff = (datetime.now() - lastMod).total_seconds()
    print(diff)
    return diff > expiryDur