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
            phoenix_date = row[1] # '20150122'
            phoenix_year = row[2] # '2015'
            phoenix_month = row[3] # '01'
            phoenix_day = row[4] # '22'
            phoenix_source = row[5] # 'IGOEUREEC'
            phoenix_sourceroot = row[6] # 'IGO'
            phoenix_sourceagent = row[7] # ''
            phoenix_sourceothers = row[8] # 'EUR;EEC'
            phoenix_target = row[9] # 'IGOEUREECLEG'
            phoenix_targetroot = row[10] # 'IGO'
            phoenix_targetagent = row[11] # ''
            phoenix_targetothers = row[12] # 'EUR;EEC;LEG'
            phoenix_code = row[13] # '041'
            phoenix_rootcode = row[14] # '04'
            phoenix_quadclass = row[15] # '1'
            phoenix_goldstein = row[16] # '1.0'
            phoenix_joinedissues = row[17] # ''
            phoenix_lat = row[18] # ''
            phoenix_lon = row[19] # ''
            phoenix_placename = row[20] # ''
            phoenix_statename = row[21] # ''
            phoenix_countryname = row[22] # ''
            phoenix_ids = row[23] # '54c179818250fc4e1e7aa659_1'
            phoenix_urls = row[24] # these are clearly urls
            phoenix_sources = row[25] # 'phil_bicolmail'
            collection.update({"_id": event_ids},{"$set": {"phoenix_found": 1, "phoenix_date": phoenix_date, "phoenix_year": phoenix_year, "phoenix_month": phoenix_month, "phoenix_day": phoenix_day, "phoenix_source": phoenix_source, "phoenix_sourceroot": phoenix_sourceroot, "phoenix_sourceagent": phoenix_sourceagent, "phoenix_sourceothers": phoenix_sourceothers, "phoenix_target": phoenix_target, "phoenix_targetroot": phoenix_targetroot, "phoenix_targetagent": phoenix_targetagent, "phoenix_targetothers": phoenix_targetothers, "phoenix_code": phoenix_code, "phoenix_rootcode": phoenix_rootcode, "phoenix_quadclass": phoenix_quadclass, "phoenix_goldstein": phoenix_goldstein, "phoenix_joinedissues": phoenix_joinedissues, "phoenix_lat": phoenix_lat, "phoenix_lon": phoenix_lon, "phoenix_placename": phoenix_placename, "phoenix_statename": phoenix_statename, "phoenix_countryname": phoenix_countryname, "phoenix_ids": phoenix_ids, "phoenix_urls": phoenix_urls, "phoenix_sources": phoenix_sources}})
