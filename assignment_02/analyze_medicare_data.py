# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#import modules
import requests, os, zipfile, openpyxl,sqlite3, glob, getpass, re, csv

#create a staging subdirectory called 'staging'
staging_dir_name = "staging"
os.mkdir(staging_dir_name)

#get the zip file
url = "https://data.medicare.gov/views/bg9k-emty/files/0a9879e0-3312-4719-a1db-39fd114890f1?content_type=application%2Fzip%3B%20charset%3Dbinary&filename=Hospital_Revised_Flatfiles.zip"
r = requests.get(url)

#download the zip file in 'staging'
zip_file_name = os.path.join(staging_dir_name, "test.zip")
zf = open(zip_file_name, "wb")
zf.write(r.content)
zf.close()

#unzip the file into various csv files in the staging directory.
z = zipfile.ZipFile(zip_file_name, 'r')
z.extractall(staging_dir_name)
z.close()

#delete FY2015_Percent_Change_in_Medicare_Payments.csv
rf = os.path.join(staging_dir_name,'FY2015_Percent_Change_in_Medicare_Payments.csv')
os.remove(rf)

#define a founction to transform table name
def trans_tname(name):
    name = str.lower(name) #lowercase
    name = name.replace(" ", "_")
    name = name.replace("-", "_")
    name = name.replace("%", "pct")
    name = name.replace("/", "_")
    newname = list(name) #If a table name starts with anything other than a letter “a” through “z” then prepend “t_” to the front of the table name
    if not re.search('[a-z]', newname[0]):    
        newname[0] = 't_'
    return ''.join(newname)

#define a founction to transform colomn name
def trans_cname(name):
    name = str.lower(name) #lowercase
    name = name.replace(" ", "_")
    name = name.replace("-", "_")
    name = name.replace("%", "pct")
    name = name.replace("/", "_")
    newname = list(name) #If a column name starts with anything other than a letter “a” through “z” then prepend “c_” to the front of the column name
    if not re.search('[a-z]', newname[0]):    
        newname[0] = 'c_'
    return ''.join(newname)


glob_dir = os.path.join(staging_dir_name,"*.csv")
#read the files with an encoding of cp1252
for file_name in glob.glob(glob_dir): 
    #read the files with an encoding of cp1252
    fn = os.path.join(staging_dir_name, os.path.basename(file_name))
    in_fp = open(fn, 'rt', encoding='cp1252')
    input_data = in_fp.read()
    in_fp.close()
    #write them out in utf-8 encoding
    ofn = os.path.join(staging_dir_name, trans_tname(os.path.splitext(os.path.basename(file_name))[0]) + ".fix")
    out_fp = open(ofn, 'wt', encoding='utf-8')
    for c in input_data:
        if c != '\0':
            out_fp.write(c) #get .fix files
    out_fp.close()

#create SQL connect
conn = sqlite3.connect('medicare_hospital_compare.db')
cur = conn.cursor()

#import .fix file to SQL db
glob_dir = os.path.join(staging_dir_name, "*.fix")
for csvfile in glob.glob(glob_dir): 
    #get table name
    tablename = trans_tname(os.path.splitext(os.path.basename(csvfile))[0])
    #read the csvfile
    f = open(csvfile, encoding = 'utf-8')
    varlist = []
    for row in csv.reader(f):
        varlist.append(row)
    f.close()
    #get the column name    
    newheader = []
    for head in varlist[0]:
        newheader.append(trans_cname(head))
    #create the table 
    header = ", ".join("%s text" % head for head in newheader)
    query_string_1 = "CREATE TABLE %s (%s)" % (tablename, header)
    cur.execute(query_string_1)
    #insert values    
    var_string = ', '.join('?' * len(varlist[0]))
    query_string_2 = 'INSERT INTO %s VALUES (%s);' % (tablename, var_string)    
    for i in range(1, len(varlist)):       
        if len(varlist[i]) != 1: #skip lines that don't have the right number of columns
            cur.execute(query_string_2, varlist[i])
           
    conn.commit()

