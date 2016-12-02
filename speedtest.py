#!/usr/bin/python

import subprocess
import re
import time
import sys

def grep_it(pattern,string,default,debug,show_error=True):
  if debug: print "pattern: <%s>" % pattern
  out = re.search(pattern,string)
  try:
    out = out.group(1)
  except:
    out = error_it(pattern,string,default,show_error)
  if debug: print "out: %s" % out
  return out

def error_it(pattern,string,default,show_error=True):
    if show_error:
      print 'ERROR: failed to find pattern <'+pattern+'> in the following string:'
      print string
      print 'ERROR:',str(sys.exc_info())
      print 'ERROR: using default value: '+default
    return default

def clean_it(string):
  return string.replace('(','\(').replace(')','\)').replace('|','\|').replace('.','\.')


debug = False

if debug:
  stats="""Date: Sun,  6 Sep 2015 20:15:46 +0200 (CEST)
Status: RO

Retrieving speedtest.net configuration...
Retrieving speedtest.net server list...
Testing from KPN (77.163.148.21)...
Selecting best server based on latency...
Hosted by ExtraIP (Amersfoort) [26.83 km]: 26.496 ms
Testing download speed........................................
Download: 2.54 Mbit/s
Testing upload speed..................................................
Upload: 1.27 Mbit/
Share results: http://www.speedtest.net/result/5324756077.png
"""
else:
  if len(sys.argv)>2:
    with open(sys.argv[2], 'r') as myfile: stats=myfile.read()
  else:
    try:
      stats = subprocess.check_output(['/usr/local/bin/speedtest-cli','--share'])
    except Exception as e:
      sys.exit("ERROR: failed to call speedtest-cli: "+str(e))


if debug: print stats

# Example:
# Download: 38.87 Mbits/s
# Upload: 5.29 Mbits/s

pattern='Date: (.+?)\n'
timestamp = grep_it(pattern,stats,time.strftime("%a, %d %b %Y %H:%M:%S %z (%Z)"),debug,False)

pattern='Testing from (.+?) \('
testingfrom = grep_it(pattern,stats,'ERROR',debug)

pattern='Testing from %s \((.+?)\)' % clean_it(testingfrom)
ip = grep_it(pattern,stats,'ERROR',debug)

pattern='Hosted by (.+?) \['
host = grep_it(pattern,stats,'ERROR',debug)

pattern='Hosted by %s \[(.+?)\]:' % clean_it(host)
distance = grep_it(pattern,stats,'ERROR',debug)

try:
  pattern='Hosted by %s \[%s\]: (.+?)\n' % (clean_it(host),clean_it(distance))
except:
  ping = error_it(pattern,stats,'ERROR')
else:
  ping = grep_it(pattern,stats,'ERROR',debug)

pattern='Download: ([0-9]*\.[0-9]*.*)\n'
download = grep_it(pattern,stats,'ERROR',debug)

pattern='Upload: ([0-9]*\.[0-9]*.*)\n'
upload = grep_it(pattern,stats,'ERROR',debug)

pattern='Share results: (.+?)\n'
share = grep_it(pattern,stats,'ERROR',debug)

string =  timestamp + ', ' + download + ', ' + upload + ', ' + ping + ', ' + distance + ', ' + ip + ', ' + testingfrom + ', ' + host + ', ' + share

if debug:
  print "string:%s" % string
else:
  f = open(sys.argv[1], 'a')
  f.write(string + "\n")
  f.close()
