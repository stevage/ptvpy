import hmac, hashlib, hmac, urllib2
import json
import apikey # This file must define devid and key
ptvbase="http://timetableapi.ptv.vic.gov.au"

def callapi(api, args):
  preamble = "/v2/"
  if args:
    args = "&" + args
  call = preamble + api + "?devid=" + apikey.devid + args

  sig=hmac.new(apikey.devkey, call , hashlib.sha1).hexdigest().upper()
  url=ptvbase + call + "&signature="+sig
  print url
  response = urllib2.urlopen(url)
  
  return json.load(response)

def healthcheck():
  import datetime
  # healthcheck()
  h = callapi("healthcheck", "timestamp=" + datetime.datetime.utcnow().replace(microsecond=0).isoformat())
  print h
  if not h['securityTokenOK'] or not h['databaseOK'] :
    raise Exception('Failed healthchck')

def stopsonaline(mode,line):
  # test.stopsonaline(4,'1818')
  h = callapi("mode/" + str(mode) + "/line/" + line + "/stops-for-line", "")
  return h

def specificnextdepartures(mode, line, stop, directionid, limit, for_utc):
  # specificnextdepartures("1","1881","2026","24","1",datetime.datetime.utcnow().replace(microsecond=0).isoformat())

  h = callapi("mode/" + mode + "/line/" + line + "/stop/" + stop + "/directionid/" + directionid + 
        "/departures/all/limit/" + limit, 
        "for_utc=" + for_utc)

  return h
