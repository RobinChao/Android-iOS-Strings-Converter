# -*- coding: utf-8 -*-
# Script takes a csv and creates strings for Android (.xml) and iOS (.Strings).
# csv in the format [key, language1, langauge2 ......]
# usage - Python converter.py [FILEPATH]

import sys, os, getopt, csv, xml.etree.ElementTree as ET
from xml.dom import minidom

def prettify(elem):
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")
    
# Read in output directory
try:   
   sys.argv[1:] 
   fileDestination = sys.argv[1]
except IndexError:  
   print "Error: Please supply an output directory."
   print "Usage: converter.py [FILEPATH]"
   sys.exit()  

# Create directory if it doesn't exists
if not os.path.exists(fileDestination):
    os.makedirs(fileDestination)

# Read from csv
f = open('test_files/Strings.csv')
csv_f = csv.reader(f)

# Determine the number of languages from the csv
line1 = csv_f.next()
numberOfLocales =  len(line1)

# Create strings for each language
for x in range(1, numberOfLocales):
	#Returns to the start of the csv and ignores the first line
	f.seek(0)
	csv_f.next()
	rowIndex = 0

	# Android xml
	resources = ET.Element("resources")

	# Create iOS strings file
	iOSFile = open(fileDestination+"/"+line1[x]+".Strings", "w+")

	for row in csv_f:
		++rowIndex
		try:
			# Write string to xml
			ET.SubElement(resources, "string", name=row[0]).text = row[x].decode('utf-8')
			# Write string to iOS .Strings
			iOSFile.write("/*  */\n")
			iOSFile.write('"'+row[0]+'"'+ ' = ' + '"'+row[x]+'"' + ";\n")
			iOSFile.write("\n")
		except IndexError:
			f.seek(0)
			print "There is a problem with the csv file at row {}".format(rowIndex+1) + " with the language {}".format(line1[x])
			r = list(csv_f)
			print r[rowIndex]
			sys.exit()
	# Write to Android file
	androidFile = open(fileDestination+"/"+line1[x]+"_strings.xml", "w+")
	androidFile.write(prettify(resources).encode('utf-8'))	