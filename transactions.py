from espn_api.football import League as fb_league
from espn_api.basketball import League as bb_league
from spontit import SpontitResource
from ssl import SSLError
from requests.exceptions import Timeout, ConnectionError
from urllib3.exceptions import ReadTimeoutError
import logging
import time
import sys

starttime = time.time()
resource = SpontitResource('jwill24', 'QC1I1NE14I2XHBW55Q04OEHCTDR5RELMHAFZUKT4OCBHJ25VZ2WV0OZUDJL6LGKVVHI2YV3E84P3CCVJEMCNMC4ZOSC2QO38UISK')
goat_league = fb_league(league_id=90359061, year=2020, espn_s2='AEBV%2BW%2F%2F1DGOy1iiBpocpFpegxEcV4ZhLWoeTzr%2BNQ8pCwar1AqPMqmI8u%2FA%2BIv0ii7WFXRM1e%2FTU3B6YNbn1sgisIdAOIMzpW2PFGFHJpQfBor%2BL5xdqw78xQZhbbxMZDonn4xo0xW%2BbqLwOEv0dc%2BHjWz8NNBfST6f0z9%2BT13LXh77Sln5cs\
dofCEPm2n2LoXe2cUOXLB6rW4rB4N4czYFWgH70TDFMUIT1dDZ%2FMrCrwXE%2BJ9ej5NaAoz9XoJC6B3SPbQaksTpq4KeaVQz6eeH', swid='{9404E72D-02B1-41C9-84E7-2D02B191C9FC}' )
kt_league = bb_league(league_id=79672, year=2021, espn_s2='AEAwMtmo2csfHtJSQ0OszgBeGKp79MilJy3qBU60MI0vC0zRasKoy0%2B83ts9R8TNGCaH3e5v10AInul%2FEUTRSW%2BxRL%2Bx5Widcgnkw0%2FiR0SNc9bLP7txlkQf2A0c9XVJIvMCt7VbCqne7eRYg%2BGfSPTAQXY%2BHpjmvG45ubw6AGgK%2FLp2xEOdIYsK02TeicS8lynRl6WxrJkCQnXdzs0c%2BFLB7%2BbtVmXleIrUcN1fzr1%2BeZ%2F8iqIFVECaaGx5yGPKzjqdgP%2FCCbm1ywEi1ZDJmYIZ', swid='{9404E72D-02B1-41C9-84E7-2D02B191C9FC}')


#-------------------------

def sendMessage(activity):

    a = activity.split(',')
    addition = True if len(a) > 3 else False

    team = a[0][a[0].find('Team(')+5:a[0].find(')')]
    if addition:
        if 'ADDED' in a[1]: n_a, n_d = 2, 4
        elif 'ADDED' in a[3]: n_a, n_d = 4, 2
        else:
            resource.push('TRADE ALERT!')
            return
        add = a[n_a][:a[n_a].find(')')]
        drop = a[n_d][:a[n_d].find(')')]
        activity_string = team + ' added ' + add + ' and dropped ' + drop
    else:
        drop = a[2][:a[2].find(')')]
        activity_string = team + ' dropped ' + drop
        
    resource.push(activity_string)
    #print(activity_string) # FIXME: for testing


#-------------------------


tmp_goat = goat_league.recent_activity()[0]
tmp_kt = kt_league.recent_activity()[0] #KTLEAGUE

#tmp_goat = 'initialize' # FIXME: for testing
#tmp_kt = 'initialize' # FIXME: for testing

while True:
    try:
        activity_goat = goat_league.recent_activity()
        activity_kt = kt_league.recent_activity() #KTLEAGUE
    except (Timeout, SSLError, ReadTimeoutError, ConnectionError) as e:
        #logging.warning("Network error occurred. Keep calm and carry on.", str(e))
        print("Network error occurred. Keep calm and carry on.")
    except Exception as e:
        #logging.error("Unexpected error!", e)
        print("Unexpected error!")
    finally:
        logging.info("Stream has crashed. System will restart twitter stream!")
        #print("System has crashed. Rebooting transaction sequence ...")

    # Check GOAT League
    if str(tmp_goat) != str(activity_goat[0]):
        print('Alert!')
        sendMessage(str(activity_goat[0]))
        tmp_goat = activity_goat[0]

    # Check KT League
    if str(tmp_kt) != str(activity_kt[0]):
        print()
        print('Alert!')
        print()
        sendMessage(str(activity_kt[0]))
        tmp_kt = activity_kt[0]
    
    duration = time.time()-starttime
    if duration <= 60: denom, unit = 1.0, 'seconds'
    elif duration > 60 and duration <= 3600: denom, unit = 60.0, 'minutes '
    elif duration > 3600: denom, unit = 3600, 'hours   '
    str_time = round(duration/float(denom),0)
    sys.stdout.write("\rTime running: {} {}".format(str_time, unit))
    sys.stdout.flush()
    time.sleep(15.0 - ((time.time() - starttime) % 15.0)) # check every 15 seconds
    #time.sleep(2.0 - ((time.time() - starttime) % 2.0)) # FIXME: for testing
    
