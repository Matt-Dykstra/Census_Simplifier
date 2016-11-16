# Census_Simplifier

#NOTE: This was most recently tested on 10.2. There are no guarantees it will work on 10.3 or higher.

#This tool copies and converts a CSV file downloaded from the U.S. Census Bureau American FactFinder tool into a geodatabase table 
#accepted by ArcGIS and containing only those fields useful for the end user. A user selection of fields is enabled through 
#the use of a text file list of desired fields, field names, and field types (TEXT, FLOAT, and LONG are supported). 

#The tool will then join the resulting table to a TIGER/Line shapefile for use in ArcMap.

The primary file format provided by the U.S. Census Bureau for data from the American FactFinder site is a comma delimited (.csv) format. 
#However, the file cannot be used immediately in ArcGIS because some of the default formatting is incompatible with ArcGIS, 
#and most downloaded files contain many more fields than are needed. This script tool solves both the issue of incompatible 
#formatting and unwieldy tables. 

#INSTRUCTIONS:

#download both the toolbox (must have ArcMap) and python tool.

#download desired census data and matching tiger/line file.

#Create text file as follows:
#existingFieldName1,desiredFieldName1,fieldType1|existingFieldName2,desiredFieldName2,fieldType2 etc.
# ONLY FIELD TYPES TEXT, FLOAT, and LONG are supported.

#Open the scripting tool “Census to TIGER/Line” in ArcMap.Input the target folder, target file, input CSV, 
and input text as prompted by in-tool directions.

#Run the tool. Output should be tempTable.dbf file, along with additional information added to shapefile. 
#I did not choose to have the table automatically deleted, as it may be useful as a check on tool function.

#Examine .dbf output file and target shapefile for accurate transfer of selected fields. 
