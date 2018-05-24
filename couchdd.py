#!/usr/bin/env python2
import requests
import json
import argparse
import os
import base64

def getBanner(url):
    banner = json.loads(requests.get(url).text)
    print "[+] CouchDB Version: %s" % banner["version"]

def auditCouchDB(url):
    getBanner(url)
    db_list = json.loads(requests.get(url + "/_all_dbs").text)
    print "[+] Database Count: %s" % len(db_list)
    print "[+] Databases: %s" % db_list
    checkDBs(url, db_list)

def checkDBs(url, db_list):
    for db in db_list:
        r = requests.get(url + "/%s/_all_docs" % db)
        if r.status_code == 200:
            print "[!] Database '%s' can be accessed without authentication, dumping contents..." % db
            dumpNoAuthDB(url, db)

def dumpNoAuthDB(url, db):
    r = requests.get(url + "/%s/_all_docs?include_docs=true&attachments=true" % db)
    saveDBDocs(db, r.text)
    saveAttachments(db, r.text)

    print "[!] Saved database contents in '%s/dump' folder for review." % os.getcwd()

def saveDBDocs(db, data):
    dump_dir = os.path.join(os.getcwd(), "dump", db)
    if not os.path.exists(dump_dir):
        os.makedirs(dump_dir)
    f = open(dump_dir + "/%s.json" % db, "wb")
    f.write(data.encode('UTF-8'))
    f.close()

def saveAttachments(db, data):
    db_collection = json.loads(data)
    doc_count = db_collection["total_rows"]
    attachments_dir = os.path.join(os.getcwd(), "dump", db, "attachments")
    for i in xrange(0, doc_count):
        if '_attachments' in db_collection["rows"][i]["doc"]:
            if not os.path.exists(attachments_dir):
                os.makedirs(attachments_dir)
            attach_number = len(db_collection["rows"][i]["doc"]["_attachments"].keys())
            for j in xrange(0, attach_number):
                attach_id = db_collection["rows"][i]["doc"]["_id"]
                attach_name = db_collection["rows"][i]["doc"]["_attachments"].keys()[j]
                attach_data = db_collection["rows"][i]["doc"]["_attachments"][attach_name]["data"]
                f = open(attachments_dir + "/%s_%s" % (attach_id, attach_name), "wb")
                f.write(base64.b64decode(attach_data))
                f.close()

def main():
    parser = argparse.ArgumentParser(description='couchdd - CouchDB Enumeration and Dump Script for DBs Without Authentication')
    parser.add_argument('--rhost', help='CouchDB IP address', default='127.0.0.1')
    parser.add_argument('--rport', help='CouchDB Port', default='5984')
    args = parser.parse_args()

    base_url = "http://%s:%s" % (args.rhost, args.rport)

    auditCouchDB(base_url)

if __name__ == "__main__":
    main()
