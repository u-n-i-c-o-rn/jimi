import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--config', help='Path to settings.json')
parser.add_argument('--id', help='System ID value')
parser.add_argument('--ip', help='Primary network address ( ip ) uses to address this system')
parser.add_argument('--secure', help='Enable TLS for internal jimi API')
parser.add_argument('--max_workers', help='Maxium number of workers')
parser.add_argument('--core_bind_address', help='Bind address for jimi_core')
parser.add_argument('--core_bind_port', help='Bind port for jimi_core')
parser.add_argument('--worker_bind_address', help='Bind address for jimi_core workers')
parser.add_argument('--worker_bind_port_start', help='Bind port start for jimi_core workers')
parser.add_argument('--web_bind_address', help='Bind address for jimi_web')
parser.add_argument('--web_bind_port', help='Bind port for jimi_core')
parser.add_argument('--db_host', help='Database connection details i.e. 127.0.0.1:27017')
parser.add_argument('--db_username', help='Database username')
parser.add_argument('--db_password', help='Database password')
parser.add_argument('--db', help='Database name to use')
args = parser.parse_args()
if args.config:
	with open(str(Path(args.config))) as f:
		config = json.load(f)
else:
	config = {
		"system" : {
			"systemID" : 0,
			"accessAddress" : "127.0.0.1",
			"secure" : False,
			"max_workers" : 1
		},
		"mongodb": {
			"hosts" : ["127.0.0.1:27017"],
			"db" : "jimi",
			"username" : None,
			"password" : None
		},
		"api": {
			"base" : "api/1.0",
			"core" : {
				"bind" : "127.0.0.1",
				"port" : 5000
			},
			"worker" : {
				"bind" : "127.0.0.1",
				"startPort" : 5001
			},
			"web" : {
				"bind" : "0.0.0.0",
				"port" : 5015
			}
		}
	}
	config["system"]["accessPort"] = config["api"]["core"]["port"]

if args.id:
	config["system"]["systemID"] = int(args.id)
if args.ip:
	config["system"]["accessAddress"] = args.ip
if args.secure:
	config["system"]["secure"] = bool(args.secure)
if args.max_workers:
	config["system"]["max_workers"] = int(args.max_workers)

if args.core_bind_address:
	config["api"]["core"]["bind"] = args.core_bind_address
if args.core_bind_port:
	config["api"]["core"]["port"] = int(args.core_bind_port)
if args.worker_bind_address:
	config["api"]["worker"]["bind"] = args.worker_bind_address
if args.worker_bind_port_start:
	config["api"]["worker"]["startPort"] = int(args.worker_bind_port_start)
if args.web_bind_address:
	config["api"]["web"]["bind"] = args.web_bind_address
if args.web_bind_port:
	config["api"]["web"]["port"] = int(args.web_bind_port)

if args.db_host:
	config["mongodb"]["hosts"] = [args.db_host]
if args.db_username:
	config["mongodb"]["username"] = args.db_username
if args.db_password:
	config["mongodb"]["password"] = args.db_password
if args.db:
	config["mongodb"]["db"] = args.db

import json
from pathlib import Path

from core import function
from core import helpers

from core import db
from core import settings
from core import cache
# Fix settings cache expiry time
cache.globalCache.updateCacheSettings("settingsCache",cacheExpiry=3600)
from core import logging
from core import api
from core import auth
from core import admin, audit, cluster, debug, flow, model, plugin, scheduler, static, storage, workers, exceptions, revision, organisation
from core.models import  action, conduct, trigger, webui

from system import logic, variable, system

from system.models import trigger as systemTrigger
