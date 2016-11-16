# This script tool copies and converts a CSV file downloaded from the
#U.S. Census Bureau American FactFinder tool into a geodatabase table
#containing only those fields useful for the end user. These fields are
#selected from a text file containing a list of fields in the format:
#existingFieldName1,desiredFieldName1,fieldType1|existingFieldName2,desiredFieldName2,fieldType2 etc.
#The tool will then join the resulting table to a TIGER/Line shapefile for use in ArcMap.

#Import arcpy
import arcpy
from arcpy import env

#collect input files and desired outpath
targetFolder = arcpy.GetParameterAsText(0)

targetFile = arcpy.GetParameterAsText(1)

inputCsv = arcpy.GetParameterAsText(2)

inputText = arcpy.GetParameterAsText(3)

arcpy.env.workspace = targetFolder
out_path = targetFolder

#allows overwrite
env.overwriteOutput = True

#Create empty table to hold desired columns from CSV
arcpy.CreateTable_management(out_path, "TempTable.dbf")
tempTable = "TempTable.dbf"

# Import CSV module, open CSV file and read header line
import csv
csvFile = open(inputCsv, "r")
csvReader = csv.reader(csvFile,delimiter =",", quotechar= '"')
headerline = csvReader.next()
csvList = headerline
print csvList

# set first column statement to allow insert cursor to insert first column only
firstColumn = True

# Open text file
textFile = open(inputText, "r")
lineOfText = textFile.readline()
###print lineOfText
fieldSetList = lineOfText.split("|")
#print fieldSetList

#If value in text file is present in csv header line, create new field in temp table
#based on input in text file
for fieldSet in fieldSetList:
    fieldInfo = fieldSet.split(",")
    fieldNameIn = (fieldInfo[0])
    fieldNameOut = (fieldInfo[1])
    fieldType = (fieldInfo[2])
    print fieldNameOut + ", " + fieldType
    arcpy.AddMessage(fieldNameOut + ", " + fieldType)
    arcpy.AddField_management(tempTable, fieldNameOut, fieldType)
    
    #if fields in text file are in csvList, copy rows from csv to table
    if fieldNameIn in csvList:
        print fieldNameIn
        arcpy.AddMessage("This is a field: " + fieldNameIn)
        #copy rows from csv to table
        csvNameIndex = csvList.index(fieldNameIn)
        try:

            #if the first column in the table does not already contain values,
            #use the insert cursor to loop through rows in CSV file and insert
            #values for first column
            if firstColumn:
                with arcpy.da.InsertCursor(tempTable, (fieldNameOut,)) as cursor:    
                    for line in csvReader:
                        segmentedLine = line
                        #Changes the field type depending on input in text file
                        if fieldType == "FLOAT":
                            csvName = float(segmentedLine[csvNameIndex])
                        elif fieldType == "LONG":
                            csvName = int(segmentedLine[csvNameIndex])
                        else:
                            csvName = (segmentedLine[csvNameIndex])
                        rowIn = (csvName,)
                        cursor.insertRow(rowIn)
                    del cursor
                    csvFile.seek(0)
                    csvReader.next()
                    firstColumn = False

            #if the first table column contains values, use the update cursor to loop
            #through CSV file rows and update values for additional columns
            else:
                with arcpy.da.UpdateCursor(tempTable, (fieldNameOut,)) as cursor:
                    row = cursor.next()
                    for line in csvReader:
                        try:
                            segmentedLine = line
                            #Changes the field type depending on input in text file
                            if fieldType == "FLOAT":
                                csvName = float(segmentedLine[csvNameIndex])
                            elif fieldType == "LONG":
                                csvName = int(segmentedLine[csvNameIndex])
                            else:
                                csvName = (segmentedLine[csvNameIndex])
                            rowIn = (csvName,)
                            row[0] = csvName
                            cursor.updateRow(row)
                            row = cursor.next()
                        except StopIteration:
                            print "No more rows in column"
                    csvFile.seek(0)
                    csvReader.next()

        except:
            print "Something is wrong with the cursors!"
            arcpy.AddMessage("Something is wrong with the cursors!")
            print arcpy.GetMessages(2)

        
    else:
        print "Nothing to see here"
        arcpy.AddMessage("Nothing to see here")

#Join temp table file with TIGER/Line file
arcpy.JoinField_management(targetFile, "GEOID", tempTable, "GEO_id2")



#Close open files
csvFile.close()
textFile.close()

print "All done!"
arcpy.AddMessage("All done!")

