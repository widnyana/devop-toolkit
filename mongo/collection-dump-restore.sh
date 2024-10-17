#!/bin/bash
set -euo pipefail
set -x
# Variables
SRC_DB="database_name"                                # Source database name
SRC_COLLECTION="collection_name"                      # Source collection name
SRC_HOST="127.0.0.1" # Source MongoDB server (e.g., IP or hostname)
SRC_PORT="27017"                                  # Source MongoDB port
SRC_USER="source_user"                             # Source MongoDB username
SRC_PASS="source_password"                             # Source MongoDB password

DEST_DB="database_name"                      # Destination database name
DEST_COLLECTION="collection_name" # New collection name
DEST_HOST="destination_host"             # Destination MongoDB server
DEST_PORT="27017"                        # Destination MongoDB port
DEST_USER="destination_user"             # Destination MongoDB username
DEST_PASS="destination_password"         # Destination MongoDB password

# Temp directory for dump
DUMP_DIR="/tmp/mongo_dump"

# Dump the collection from the source server
echo "Dumping collection $SRC_COLLECTION from $SRC_DB on $SRC_HOST..."
mongodump --ssl --host $SRC_HOST --port $SRC_PORT --username $SRC_USER --password $SRC_PASS --db $SRC_DB --collection $SRC_COLLECTION --out $DUMP_DIR

if [ $? -ne 0 ]; then
  echo "Failed to dump collection."
  exit 1
fi

# Restore the collection to the destination server
echo "Restoring collection as $DEST_COLLECTION in $DEST_DB on $DEST_HOST..."
mongorestore --host $DEST_HOST --port $DEST_PORT --username $DEST_USER --password $DEST_PASS --db $DEST_DB --collection $DEST_COLLECTION $DUMP_DIR/$SRC_DB/$SRC_COLLECTION.bson

if [ $? -ne 0 ]; then
  echo "Failed to restore collection."
  exit 1
fi

# Cleanup
echo "Cleaning up dump files..."
rm -rf $DUMP_DIR

echo "Dump and restore completed successfully!"
