==Nunaliit CSV Import==
A script for importing CSV data into couchDB as Nunaliit documents. 

===Prerequisites===
* CouchDB-Python library, available [here](https://github.com/djc/couchdb-python/).

===Configuration Requirements===
The script requires configuration information for the following variables; 
* **couchDbURL** - URL of the couchDb, default value is the localhost URL 127.0.0.1
* **couchDbPort** - Port number, default is 5984
* **couchDbUserName** - Your user name, default is admin
* **couchDbUserPass** - User name's password
* **couchDbName** - Name of your couchDb database
* **fileName** - File location of the CSV file, e.g. data/mydata.csv"
* **schemaName** - Nunaliit schema name e.g. "demo_doc"

===Steps to run the script===
# Provide the configuration requirments listed above
# Run the script, 'python nunaliitCSVImport.py'
