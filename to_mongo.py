#this is a little script to take files in the /home/vagrant/output directory and put their data back into mongo, indexed by url
from os import listdir
from os.path import isfile, join
import csv
import utilities
from pymongo import MongoClient

collection = utilities.make_conn('','','')


mypath = '/home/vagrant/phoenix_output'
files = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]

for file in files:
    with open(join(mypath,file),"r") as infile:
        csvreader = csv.reader(infile, delimiter='\t', quotechar='\"')
        for row in csvreader:
            event_date = row[1] # '20150122'
            event_year = row[2] # '2015'
            event_month = row[3] # '01'
            event_day = row[4] # '22'
            event_source = row[5] # 'IGOEUREEC'
            event_sourceroot = row[6] # 'IGO'
            event_sourceagent = row[7] # ''
            event_sourceothers = row[8] # 'EUR;EEC'
            event_target = row[9] # 'IGOEUREECLEG'
            event_targetroot = row[10] # 'IGO'
            event_targetagent = row[11] # ''
            event_targetothers = row[12] # 'EUR;EEC;LEG'
            event_code = row[13] # '041'
            event_rootcode = row[14] # '04'
            event_quadclass = row[15] # '1'
            event_goldstein = row[16] # '1.0'
            event_joinedissues = row[17] # ''
            event_lat = row[18] # ''
            event_lon = row[19] # ''
            event_placename = row[20] # ''
            event_statename = row[21] # ''
            event_countryname = row[22] # ''
            event_ids = row[23] # '54c179818250fc4e1e7aa659_1'
            event_urls = row[24] # these are clearly urls
            event_sources = row[25] # 'phil_bicolmail'
            print collection.find({"url": event_urls})
