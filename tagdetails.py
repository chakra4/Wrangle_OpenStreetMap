import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
import operator
import sys
import getopt

def Audit(OsmFile,ElementToSearch,TagKeyToSearch,Details,OutFile):
  osm_file_handle = open(OsmFile, "r")
  tagValues = defaultdict(set)
  tagCount = {}
  for event, elem in ET.iterparse(osm_file_handle, events=("start",)):
    #if elem.tag == "node" or elem.tag == "way":
    if (elem.tag == ElementToSearch or ElementToSearch == 'all'):
      for tag in elem.iter("tag"):
        attribute = tag.attrib['k']
        value = tag.attrib['v']
        if (tagCount.has_key(attribute)):
          tagCount[attribute] += 1
        else:
          tagCount[attribute] = 1
        tagValues[attribute].add(value)
        if (attribute == TagKeyToSearch and Details == 'yes'):
          #To print current XML Element
          print ET.tostring(elem, encoding='utf-8')
  osm_file_handle.close()
  #print tagCount

  #Print attributes in sorted order
  if(TagKeyToSearch == ""):
    keylist = tagCount.keys()
    keylist.sort()
    for key in keylist:
      print "%s: %s" % (key, tagCount[key])
  else:
      print "%s: %s" % (TagKeyToSearch, tagCount[TagKeyToSearch])
      print sorted(tagValues[TagKeyToSearch])

def usage():
  print "tagdetails.py -i <InputOsmFile> -e <ElementToSearch ('node' or 'way' or 'all')> -k <TagKeyToSearch> -d <Details ('yes' or 'no')>"

if __name__ == '__main__':
  try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:e:k:d:o:h', ['ifile=', 'element=', 'tagkey', 'details=', 'ofile=', 'help='])
  except getopt.GetoptError:
      usage()
      sys.exit(2)

  OsmFile = ""
  ElementToSearch = ""
  TagKeyToSearch = ""
  Details = ""
  OutFile = ""
  
  for opt, arg in opts:
    if opt in ('-h', '--help'):
      usage()
      sys.exit(2)
    elif opt in ('-i', '--ifile'):
      OsmFile = arg
    elif opt in ('-e', '--element'):
      ElementToSearch = arg
    elif opt in ('-k', '--tagkey'):
      TagKeyToSearch = arg
    elif opt in ('-d', '--details'):
      Details = arg
    elif opt in ('-o', '--ofile'):
      OutFile = arg
    else:
      usage()
      sys.exit(2)

  Audit(OsmFile,ElementToSearch,TagKeyToSearch,Details,OutFile)
