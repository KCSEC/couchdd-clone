couchdd
couchdd is a simple standalone script which does one thing and one thing only: it enumerates any database not protected with authentication from a CouchDB instance and loots everything.

CouchDB Database Access Control Primer
If you create a database via the CouchDB REST API as below...

curl --user admin:pwd -X PUT http://IP:5984/dbA

... by default it can be accessed for anonymous document reads (or writes), unless you do the following...

curl -X PUT http://IP:5984/dbA/_security --user admin:pwd -H "Content-Type: application/json" -d '{"admins": { "names": [], "roles": [] }, "members": { "names": ["user1"], "roles": [] } }

...which will restrict access to dbA to members only (user1) or admin. This default behaviour is not a secret, is clearly stated in the CouchDB documentation[1] and should never be the configuration state of a live system but, you know, I've seen everything.

Usage
Usage:

python couchdd.py [-h] [--rhost RHOST] [--rport RPORT]

If a database with no user membership set is found the script will:

create a 'dump' folder under the current directory with a per-database subfolder
copy and save on the filesystem all the document collections in JSON format
extract any inline Base64-encoded file attachment from the document collection
Disclaimer
It's not enterprise. It doesn't have any structured exception handling. If something goes wrong, horrible things might and will happen including error stack traces, segmentation faults, kernel panics and fires. It should be used only when the rhost part coincides with a system you own or which falls under the broad expression "under scope". It probably won't find anything.

References
[1] http://docs.couchdb.org/en/2.0.0/api/database/security.html

#### Clone from deleted rep
https://github.com/faber-rwx/couchdd
