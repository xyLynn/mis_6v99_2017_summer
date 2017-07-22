# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#import modules
import requests, os, zipfile, openpyxl,sqlite3, glob, getpass, re, csv
import pandas as pd

#FIRST QUESTION
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
        newname.insert(0, 't_')
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
        newname.insert(0,'c_')
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
cur.close()
conn.close()






#SECOND QUESTION
#download xlsx file
k_url = "http://kevincrook.com/utd/hospital_ranking_focus_states.xlsx"
r = requests.get(k_url)
xf = open("hospital_ranking_focus_states.xlsx", "wb")
xf.write(r.content)
xf.close()

#create hospital_ranking_focus_states.xlsx file
wb = openpyxl.load_workbook("hospital_ranking_focus_states.xlsx")

#create three pandas dataframe
#create a pandas dataframe for sheet Hospital National Ranking
sheet = wb.get_sheet_by_name("Hospital National Ranking")
ranker = []
i = 1 
while sheet.cell(row=i, column=1).value !=None: #transform excel content into list
    rank = [sheet.cell(row=i, column=1).value, sheet.cell(row=i, column=2).value]
    ranker.append(rank)
    i += 1
r = pd.DataFrame(ranker[1:], columns=["ProviderID", "Ranking"])  #transform list into pandas dataframe
#create a pandas dataframe for sheet Focus States
sheet2 = wb.get_sheet_by_name("Focus States")
fst = []
i = 1 
while sheet2.cell(row=i, column=1).value !=None: #transform excel content into list
    st = [sheet2.cell(row=i, column=1).value, sheet2.cell(row=i, column=2).value]
    fst.append(st)
    i += 1   
s = pd.DataFrame(fst[1:], columns=["StateName", "StateAbbre"])  #transform list into pandas dataframe
#create a pandas dataframe for file hospital_general_information
fp = os.path.join(staging_dir_name, 'hospital_general_information.fix')
hf = open(fp, 'rt', encoding= 'utf-8')
hlist = [] #transform file content into list
for row[:7] in csv.reader(hf):
    hlist.append(row[:7])
hf.close()
h = pd.DataFrame(hlist[1:], columns=["ProviderID", "HospitalName", "Address", "City", "State", "ZipCode", "County"]) #transform list into pandas dataframe

#left join Ranking and Hospital Information
nation = pd.merge(r, h, how='left', left_on='ProviderID', right_on='ProviderID' )
nation = nation.drop("Address", 1)
nation = nation.drop("ZipCode", 1)
nation = nation.drop("Ranking", 1)
nation = nation.head(100)

#create excel file Nationwide
wb2 = openpyxl.Workbook()
#define a function to create sheets
def creat_sheet(sheetname):
    sheet_1 = wb2.create_sheet(sheetname)
    sheet_1.cell(row=1, column=1, value='Provider ID') #specify column names
    sheet_1.cell(row=1, column=2, value='Hospital Name')
    sheet_1.cell(row=1, column=3, value='City')
    sheet_1.cell(row=1, column=4, value='State')
    sheet_1.cell(row=1, column=5, value='County')
#use the defined function to create state sheets and Nationwide sheet
creat_sheet("Nationwide")
for i in range(1, len(fst)):
    creat_sheet(fst[i][0])
wb2.remove_sheet(wb2.get_sheet_by_name('Sheet'))
#save the excel
wb2.save("hospital_ranking.xlsx")
wb2.close()

#export the data to excel
writer = pd.ExcelWriter('hospital_ranking.xlsx', engine='xlsxwriter')
pd.io.formats.excel.header_style = None
nation.to_excel(writer,'Nationwide', index=False)
for i in range(1, len(fst)): #export data to state sheet
    if (nation['State'] == fst[i][1]).any():
        state = nation[nation.State == fst[i][1]]
        state.to_excel(writer,fst[i][0], index=False)
#save the changes
writer.save()






#THIRD QUESTION






























