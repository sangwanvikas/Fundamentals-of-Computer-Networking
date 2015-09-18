#!/usr/bin/env python
from urllib import urlopen
from csv import reader
import sys
import re

import threading, urllib2
from math import radians, cos, sin, asin, sqrt
import socket

####################################################################################
''' dictionary - it will contain { (IP adress : correcponding distance from client)} '''
####################################################################################
temp = {}

''' a list containing tuples, where each tuple contains an IP of a replica with its respective geo locatio  '''
replica_geo_info = [("52.0.73.113",  "39.04","-77.49"),
                    ("52.16.219.28", '53.33', '-6.25'),
                    ("52.11.8.29",   '45.84', '-119.70'),
                    ("52.8.12.101",  '37.34', '-121.89'),
                    ("52.28.48.84",  '50.12', '8.68'),
                    ("52.68.12.77",  '35.69', '139.75'),
                    ("52.74.143.5",  '1.29', '103.86'),
                    ("52.64.63.125", '-33.87', '151.21'),
                    ("54.94.214.108",'-23.55', '-46.64')]

####################################################################################
''' calculate geolocation of an IP - provided as an input argument'''
####################################################################################
def find_client_location(client_addr):

    received_content = urlopen('http://api.hostip.info/get_html.php?ip='+ client_addr+'&position=true').read()

    lat = received_content.split('Latitude:')[1].split(' ')[1].split('\n')[0]
    longitude = received_content.split('Longitude:')[1].split('\n')[0].split('Longitude:')[0]

    return (lat.strip(), longitude.strip())
 

########################################################################################
"""  find distance when longitude and latitude of two points on the globe are given """
########################################################################################
def find_distance(lt_client, lt_replica, lg_client, lg_replica, replica_ip):
    # convert decimal degrees to radians 
    lg_client, lt_client, lg_replica, lt_replica = map(radians, [lg_client, lt_client, lg_replica, lt_replica])
    # haversine formula 
    subtract_lg = lg_replica - lg_client 
    subtract_lt = lt_replica - lt_client 
    value = sin(subtract_lt/2)**2 + cos(lt_client) * cos(lt_replica) * sin(subtract_lg/2)**2
    dist = 2 * asin(sqrt(value)) 
    
    temp.update({replica_ip:dist})


#####################################################################################################
''' this method is called from DNS script with IP address of the client asn an input argument'''
#####################################################################################################
def initiate_mapping_script(client_host_name):
    ip =str(client_host_name)
    client_point_on_earth = find_client_location(ip)

    curr_x = float(client_point_on_earth[0])
    curr_y = float(client_point_on_earth[1])
    
    [find_distance(curr_x,float(replica_x), curr_y, float(replica_y), replica_ip) for replica_ip,replica_x,replica_y in replica_geo_info]
    va = sorted(temp.items(), key=lambda e: e[1])
    return va[0][0]

#####################################################################################################
''' Script ends here '''
#####################################################################################################