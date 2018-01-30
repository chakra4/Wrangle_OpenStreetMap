#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
"""
Your task is to wrangle the data and transform the shape of the data
into the model we mentioned earlier. The output should be a list of dictionaries
that look like this:
"""

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

city_mapping = { 
            'BENGALURU': 'Bengaluru',
            'Bangalore': 'Bengaluru',
            'Bangalore ': 'Bengaluru',
            'bangalore': 'Bengaluru',
            'Devasandra':'Devasandra, K.R Puram',
            'Doddanekundi, Marathahalli': 'Doddanekundi, Bangalore',
            'K R Puram, Bangalore': 'K.R Puram, Bangalore',
            'K.R Puram' : 'K.R Puram, Bangalore',
            'KALKERE': 'Kalkere',
            'Kundalahalli, Whitefielid': 'Kundalahalli, Bangalore',
            'Mahadevapura': 'Mahadevapura, Bangalore',
            'Marathahalli': 'Marathahalli, Bangalore',
            'Marathhalli': 'Marathahalli, Bangalore',
            'Marathhalli, Bangalore': 'Marathahalli, Bangalore',
            'Seshadripuram, Bangalore': 'Sheshadripuram, Bangalore'
            }

def is_address(elem) :
    return (elem.attrib['k'].startswith("addr:"))

def is_valid_address(elem) :
    addrList = elem.attrib['k'].split(':')
    if (len(addrList) <= 2) :
        return True
    return False

def audit_postcode(postcode):
    #Remove all space
    postcode = postcode.replace(" ","")
    #Remove all non-numeric characters
    result = re.sub('[^0-9]','', postcode)
    return result

def audit_city(city):
    if(city_mapping.has_key(city)):
        city = city_mapping[city]
    return city

def shape_element(element):
    node = {}
    created = {}
    latlon = [0,0]
    latlonIndex = {"lat" : 0 , "lon":1}
    if element.tag == "node" or element.tag == "way" :
        # YOUR CODE HERE
        #PROCESS THE ATTRIBUTES
        node['type'] = element.tag
        #print element.attrib
        for attr in element.attrib :
            #print attr, element.attrib[attr]
            if (attr in CREATED) :
                created[attr] = element.attrib[attr]
            elif attr == "lon" or attr == "lat" :
                latlon[latlonIndex[attr]] = float(element.attrib[attr])
            else :
                node[attr] = element.attrib[attr]
        node['created'] = created
        if (element.tag == "node") :
            node['pos'] = latlon
            
        #PROCESS 2ND LEVEL TAGS
        addr = {}
        for tag in element.iter("tag") :
            if is_address(tag):
                if is_valid_address(tag):
                    addrList = tag.attrib['k'].split(':')
                    attribValue = tag.attrib['v']
                    if (addrList[1] == 'postcode') :
                        attribValue = audit_postcode(attribValue)
                    if (addrList[1] == 'city') :
                        #print addrList[1]
                        attribValue = audit_city(attribValue)
                        #print attribValue
                    addr[addrList[1]] = attribValue
            else :
                node[tag.attrib['k']] = tag.attrib['v']
        if addr:
            node['address'] = addr
        
        nodeRefs = []        
        for tag in element.iter("nd") :
            nodeRefs.insert(len(nodeRefs), tag.attrib['ref'])
        if (len(nodeRefs) > 0) :
            node['node_refs'] = nodeRefs
            
        #pprint.pprint(node)
        return node
    else:
        return None


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

def test():
    # NOTE: if you are running this code on your computer, with a larger dataset, 
    # call the process_map procedure with pretty=False. The pretty=True option adds 
    # additional spaces to the output, making it significantly larger.
    data = process_map('bengaluru.osm', True)
    #pprint.pprint(data)

if __name__ == '__main__':
    test()
