import json

from apps.Utils.formresponse import formScssResp
from apps.Utils.message_constants import LOGGEDOUT_SCSS_MSG

def create_user(userObj):

    res = formScssResp("000",LOGGEDOUT_SCSS_MSG,"logoutResp",{})
    return res
