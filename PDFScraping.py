########################################################
# Title: KIID PDF Scraping
#
# Purpose: Bulk scraping and processing of PDF Documents
#
# Author: Thomas Handscomb
#
# Last Modified: 22/07/2016
########################################################

#~~~~~~~~~~~~~~~~~~~~~~~
# PDF Scraping with tika

# Import libraries
import tika
import os
import csv
from tika import parser

tika.TikaClientOnly = True

# IMPORTANT NOTE
# In a command line, navigate to C:\Users\handsct\Downloads and run the following 
# to open up the PDF scraping server: java -jar tika-server-1.13.jar --port 8080

# Define the folder where the KIIDS are located
foldername = 'L://My Documents//2015//PDF Scraping//Input PDFs'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# A Manager agnostic approach
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~
for fn in os.listdir(foldername):
    OGCnotfound = 0
    ISINnotfound = 0
    PFeenotfound = 0
    #print (fn)
    pdffn = foldername + '//' + fn
    #print(pdffn)
    
    # Open the PDF
    parsedPDF = parser.from_file(pdffn)
    
    # Handle errors here
    try:
        PDFtext = parsedPDF["content"]
        
        print(fn)        
        
        #ISIN
        if PDFtext.find('LU') != -1:
            ISINStrLocation = PDFtext.find('LU')
        elif PDFtext.find('IE') != -1:
            ISINStrLocation = PDFtext.find('IE')
        else:
            ISINnotfound = 1
        ISIN = PDFtext[ISINStrLocation:ISINStrLocation+12]
        
        #ISIN Message        
        if ISINnotfound == 1:
            ISINMessage = 'Cannot find ISIN'
        else:
            ISINMessage = 'ISIN found'
            
        print(ISINMessage)
        
        # OGC Finding Algorithm
        for i in range(1, len(PDFtext)-50):
            OGCOpStr = PDFtext[i:i+50]
            if OGCOpStr.find('Ongoing') != -1 and (OGCOpStr.find('charge') != -1 \
            or OGCOpStr.find('Charge') != -1) and OGCOpStr.find('%') != -1 \
            and OGCOpStr.find('%')>OGCOpStr.find('Ongoing'):
                #print('Found length')
                OGCnotfound = 0
                break
            else:
                OGCnotfound = 1
        
        #OGC Message
        if OGCnotfound == 1:
            OGCMessage = 'Cannot find OGC'
        else:
            OGCMessage = 'OGC found'
            
        print(OGCMessage)
        
        # 3: Find % in the local Ongoing string
        Pctlocation = OGCOpStr.find('%')
        #Pctlocation
        
        # 4: Work back 4 characters from the % character
        OGC = OGCOpStr[Pctlocation-4:Pctlocation+1]
        #OGC
        
        # Performance fee algorithm
        # Find the optimal performance fee string        
        for j in range(1, len(PDFtext)-50):
            PFeeOpStr = PDFtext[j:j+50]
            
            if PFeeOpStr.find('Performance') != -1 and (PFeeOpStr.find('fee') != -1 \
            or PFeeOpStr.find('Fee') != -1) and (PFeeOpStr.find('%') != -1 \
            or PFeeOpStr.find('None') != -1 or PFeeOpStr.find('N/A') != -1 \
            or PFeeOpStr.find('No') != -1) \
            and (PFeeOpStr.find('None') != -1 or PFeeOpStr.find('N/A') != -1 \
            or PFeeOpStr.find('No') != -1 \
            or PFeeOpStr.find('%')>PFeeOpStr.find('Performance')):
                print('Found PFee')
                PFeenotfound = 0
                break
            else:
                PFeenotfound = 1
        #PFeeOpStr
        
        # Process optimal string to extract the performance fee
        if (PFeeOpStr.find('None') != -1 or \
        PFeeOpStr.find('N/A') != -1 or PFeeOpStr.find('No') != -1):
            PFee = '0.00%'
        elif PFeeOpStr.find('%') != -1:
            PFeePctlocation = PFeeOpStr.find('%')
            if PFeeOpStr[PFeePctlocation-3:PFeePctlocation+1].find('.') == -1:
                PFee = PFeeOpStr[PFeePctlocation-1:PFeePctlocation+1]
            else: 
                PFee = PFeeOpStr[PFeePctlocation-4:PFeePctlocation+1]
        else:
            PFee = 'Check this' 
        #PFee        
        
        if OGCnotfound == 1:
            OGC = ''
        if ISINnotfound ==1:
            ISIN = ''
        if PFeenotfound ==1:
            PFee = ''
        
        fields=[fn, ISIN, OGC, PFee]
        with open('L://My Documents//2015//PDF Scraping//Summary.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(fields)
        
    except:
        print("Cannot process " + fn)
        comment = 'PDF Encrypted'        
        Exceptionfields = [fn, comment]
        
        with open('L://My Documents//2015//PDF Scraping//Summary.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(Exceptionfields)
        pass


# For manager specific fn[0:2] == 'AB':
              

##########################
# Individual manager views
##########################
foldername = "L://My Documents//2015//PDF Scraping//Input PDFs//"
#AB American growth LU0130376550
#Amundi Us concentrated core LU0568585391
#CMI US enhanced eq LU0146081418
#FIL America LU0963540371
#HSBC multialpha NA LU0358929312
#ING Invest US Grwth LU0272292805
#Invesco US Structured Equity LU0149503897.pdf
#Natixis Harris US equity fund LU0130102931.pdf
#Russell US equity IE00BDW02572.pdf
#Pioneer US fundemental gwth LU0347184748.pdf

file = "Pioneer US fundemental gwth LU0347184748.pdf"
filename = foldername + file
filename

parsedPDF = parser.from_file(filename)

parsedPDF

PDFtext = parsedPDF["content"]

print(PDFtext)
type(PDFtext)

len(PDFtext)
# Find the ISIN
if PDFtext.find('LU') != -1:
    ISINStrLocation = PDFtext.find('LU')
elif PDFtext.find('IE') != -1:
    ISINStrLocation = PDFtext.find('IE')
else:
    print('ISIN Not found')
    ISINStrLocation = ''
    
print(ISINStrLocation)

ISIN = PDFtext[ISINStrLocation:ISINStrLocation+12]
print(ISIN)

# OGC finding algorithm 
# 2: Get the local Ongoing string

#Loop to find the % sign as well
OGCnotfound=0
for i in range(1, len(PDFtext)-50):
    OGCOpStr = PDFtext[i:i+50]
    if OGCOpStr.find('Ongoing') != -1 and (OGCOpStr.find('charge') != -1 \
    or OGCOpStr.find('Charge') != -1) and OGCOpStr.find('%') != -1 \
    and OGCOpStr.find('%')>OGCOpStr.find('Ongoing'):
        print('Found length')
        OGCnotfound = 0
        break
    else:
        OGCnotfound = 1

OGCOpStr

OGCOpStr.find('Ongoin')

# 1: Find the OGC location

# 3: Find % in the local Ongoing string
Pctlocation = OGCOpStr.find('%')
#Pctlocation

# 4: Work back 4 characters from the % character
OGC = OGCOpStr[Pctlocation-4:Pctlocation+1]
OGC

# Performance fee algorithm
# Find the optimal performance fee string

PFeenotfound = 0
for j in range(1, len(PDFtext)-50):
    PFeeOpStr = PDFtext[j:j+50]
    
    if PFeeOpStr.find('Performance') != -1 and (PFeeOpStr.find('fee') != -1 \
    or PFeeOpStr.find('Fee') != -1) and (PFeeOpStr.find('%') != -1 \
    or PFeeOpStr.find('None') != -1 or PFeeOpStr.find('N/A') != -1) \
    and (PFeeOpStr.find('None') != -1 or PFeeOpStr.find('N/A') != -1 \
    or PFeeOpStr.find('%')>PFeeOpStr.find('Performance')):
        print('Found PFee')
        PFeenotfound = 0
        break
    else:
        PFeenotfound = 1

PFeeOpStr

# Process optimal string to extract the performance fee
if (PFeeOpStr.find('None') != -1 or \
PFeeOpStr.find('N/A') != -1):
    PFee = '0.00%'
elif PFeeOpStr.find('%') != -1:
    PFeePctlocation = PFeeOpStr.find('%')
    if PFeeOpStr[PFeePctlocation-3:PFeePctlocation+1].find('.') ==-1:
        PFee = PFeeOpStr[PFeePctlocation-1:PFeePctlocation+1]
    else: 
        PFee = PFeeOpStr[PFeePctlocation-4:PFeePctlocation+1]
else:
    PFee = 'Check this'

PFeeOpStr[PFeePctlocation-1:PFeePctlocation+1]

PFee

