#this is a little script to take files in the /home/vagrant/output directory and put their data back into mongo, indexed by url
from os import listdir
from os.path import isfile, join

mypath = '/home/vagrant/'
files = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
print files
