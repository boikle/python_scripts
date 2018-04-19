import couchdb
import csv

# Required Config information for connecting to the couchDb
couchDbURL = "127.0.0.1"
couchDbPort = "5984"
couchDbUserName = "admin"
couchDbUserPass = "Your password"
couchDbName = "Name of your couchDb database"
# Location of file being imported
fileName = "location of the csv file, e.g. data/mydata.csv"
# Assigned schema for import
schemaName = "nunaliit schema name"

# Connect to CouchDB
couch = couchdb.Server('http://' + couchDbUserName + ':' + couchDbUserPass + '@' + couchDbURL + ':' + couchDbPort + '/')
db = couch[couchDbName]

print( "Starting CSV import ..." )

# Walk through CSV file rows
with open(fileName, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    
    for row in reader:
        doc = {}
        # Add schema name
        doc['nunaliit_schema'] = schemaName
        rowContent = {}
        for keyValuePair in row.items():
            key = keyValuePair[0]
            value = keyValuePair[1]
            rowContent[key] = value
        doc[schemaName] = rowContent        
        db.save(doc)

print( "CSV import complete" )