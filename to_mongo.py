#this is a little script to take files in the /home/vagrant/output directory and put their data back into mongo, indexed by url
from os import listdir
from os.path import isfile, join
import csv

mypath = '/home/vagrant/phoenix_output'
files = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]

for file in files:
    with open(join(mypath,file),"r") as infile:
        csvreader = csv.reader(infile, delimiter='\\t', quotechar='\\"')
        for row in csvreader:
            print row
