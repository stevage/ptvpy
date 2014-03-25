'''
Unofficial Python wrapper for Public Transport Victoria API
Read the full API documentation here: http://stevage.github.io/PTV-API-doc/

Documentation in "quotes" here is verbatim from PTV.
Source: Licensed from Public Transport Victoria under a Creative Commons Attribution 3.0 Australia Licence.

This Python module itself is licensed under WTFPL.

To use it, rename the included apikey.example to apikey.py and include your API key and DevID.
Don't have one? Email APIKeyRequest@ptv.vic.gov.au with subject "PTV Timetable API - request for key"
'''
import hmac, hashlib, hmac, urllib, urllib2
import json, datetime
import apikey # This file must define devid and key
ptvbase="http://timetableapi.ptv.vic.gov.au"

def nownomicro():
  ''' Returns current time, without microseconds, as required by PTV API.'''
  return datetime.datetime.utcnow().replace(microsecond=0)

def now8601():
  ''' Returns current time, without microseconds, as required by PTV API, in 8601 format.'''
  return nownomicro().isoformat()


def callAPI(api, args={}):
  ''' Makes the specified API call, handling signature computation and developer id.'''
  import urllib
  preamble = "/v2/"
  if args:
    args = "&" + urllib.urlencode(args)
  else:
    args = ""
  call = preamble + api + "?devid=" + apikey.devid + args

  sig=hmac.new(apikey.devkey, call , hashlib.sha1).hexdigest().upper()
  url=ptvbase + call + "&signature="+sig
  print url
  response = urllib2.urlopen(url)
  
  return json.load(response)

def healthCheck():
  ''' Verifies that devID and key are correct so future calls will succeed.
  "A check on the timely availability, connectivity and reachability of the services that deliver security, caching and data to web clients. A health status report is returned."
  '''
  # eg: healthCheck()
  h = callAPI("healthcheck", { "timestamp": now8601() } )
  if not h['securityTokenOK'] or not h['databaseOK'] :
    raise Exception('Failed healthchck')
  return h

def stopsNearby(latitude, longitude):
  '''Stops Nearby returns up to 30 stops nearest to a specified coordinate."'''
  # stopsNearby(-38, 145)
  return callAPI("nearme/latitude/" + str(latitude) + "/longitude/" + str(longitude))
  

def transportPOIsByMap(poi, lat1, long1, lat2, long2, griddepth, limit):
  '''"Transport POIs by Map returns a set of locations consisting of stops and/or myki ticket outlets (collectively known as points of interest - i.e. POIs) within a region demarcated on a map through a set of latitude and longitude coordinates."'''
  # transportPOIsByMap(2,-37,145,-37.5,145.5,3,10)
  return callAPI("poi/" + str(poi) + "/lat1/" + str(lat1) + "/long1/" + str (long1) + 
    "/lat2/" + str(lat2) + "/long2/" + str(long2) + "/griddepth/" + str(griddepth) + "/limit/" + str(limit)) 
  

def search(query):
  '''"The Search API returns all stops and lines that match the input search text."'''
  # search("Hoddle St")
  
  return callAPI("search/" + urllib.quote(str(query)))

def broadNextDepartures(mode, stop, limit):
  '''"Broad Next Departures returns the next departure times at a prescribed stop irrespective of the line and direction of the service. For example, if the stop is Camberwell Station, Broad Next Departures will return the times for all three lines (Belgrave, Lilydale and Alamein) running in both directions (towards the city and away from the city)."'''
  # broadNextDepartures(0,1104,2)

  return callAPI("mode/" + str(mode) + "/stop/" + str(stop) + "/departures/by-destination/limit/" + str(limit))

def specificNextDepartures(mode, line, stop, directionid, limit, for_utc=nownomicro()):
  '''"Specific Next Departures returns the times for the next departures at a prescribed stop for a specific mode, line and direction. For example, if the stop is Camberwell Station, Specific Next Departures returns only the times for one line running in one direction (for example, the Belgrave line running towards the city)."'''
  # specificNextDepartures("1","1881","2026","24","1")

  return callAPI("mode/" + str(mode) + "/line/" + str(line) + "/stop/" + str(stop) + "/directionid/" + str(directionid) + 
        "/departures/all/limit/" + str(limit), 
        {"for_utc": for_utc.isoformat() })

def stoppingPattern(mode,run,stop,for_utc=nownomicro()):
  ''' "The Stopping Pattern API returns the stopping pattern for a specific run (i.e. transport service) from a prescribed 
  stop at a prescribed time. The stopping pattern is comprised of timetable values ordered by stopping order."'''
  # stoppingPattern(0,4780,1104)
  # /v2/mode/%@/run/%@/stop/%@/stopping-pattern?for_utc=%@&devid=%@&signature=%@
  return callAPI("mode/" + str(mode) + "/run/" + str(run) + "/stop/" + str(stop) + "/stopping-pattern", 
    {"for_utc": for_utc.isoformat()})

def stopsOnALine(mode,line):
  '''"The Stops on a Line API returns a list of all the stops for a requested line, ordered by location name."'''
  # stopsOnALine(4,'1818')
  h = callAPI("mode/" + str(mode) + "/line/" + line + "/stops-for-line")
  return h

