#!/usr/bin/env python
#
#  Author by Agus Bimantoro <agus.bimantoro@gdplabs.id>
#	
#  $ggssh.py - ssh alias & manager tools 
#
#


import os
import sys
import ConfigParser


home_dir = os.getenv("HOME")
ggssh_base = "%s/.ggssh" % (home_dir)
ggssh_base_hosts = "%s/hosts" % (ggssh_base)
ggssh_base_keys = "%s/keys" % (ggssh_base)
	
def ggssh_usage():
	print("""Ex: ggssh add
    ggssh config
    ggssh apply 
    ggssh show""")
	sys.exit(0)

def ggssh_add():
	
	# got input
	ssh_alias = raw_input("SSH Alias []: ")
	ssh_user = raw_input("SSH User []: ")
	ssh_host = raw_input("SSH IP/Host []: ")
	ssh_identity = raw_input("SSH Identity Key []: ")
	
	# create app base dir
	if not(os.path.exists(ggssh_base)):
		os.mkdir(ggssh_base)
		os.system("echo 'source %s/ggssh.alias' >> %s/.bashrc" % (ggssh_base,home_dir))
	if not(os.path.exists(ggssh_base_hosts)):
		os.mkdir(ggssh_base_hosts)
	if not(os.path.exists(ggssh_base_keys)):
		os.mkdir(ggssh_base_keys)
	
	# ignored space on alias name
	if (len(ssh_alias.split()) >1):
		print("Error: %s: ssh alias doesn't support space string" % (ssh_alias))
		sys.exit(2)
	
	# exit, if identity key doesn't exist
	if not(os.path.exists(ssh_identity)):
		print("Error: %s: ssh identity file doesn't exist\n" % (ssh_identity))	
		sys.exit(2)
		
	# copying identity key
	ssh_identity_path = "%s/%s" % (ggssh_base_keys,ssh_alias)
	os.system("cp %s %s" % (ssh_identity,ssh_identity_path))

	# write out config to file
	ssh_config_strings = "[%s]\n\nuser=%s\nhost=%s\nkey=%s\n\n" % (ssh_alias,ssh_user,ssh_host,ssh_identity_path)	
	f = open("%s/%s" % (ggssh_base_hosts,ssh_alias),"a")
	f.write(ssh_config_strings)
	f.close()
	
def ggssh_apply():
	os.system("echo -n '' > %s/ggssh.alias" % (ggssh_base))
	for conf_file in os.listdir(ggssh_base_hosts):
		cnf = ConfigParser.ConfigParser()
		cnf.read("%s/%s" % (ggssh_base_hosts,conf_file))
		ssh_user = cnf.get(conf_file,"user")
		ssh_host = cnf.get(conf_file,"host")
		ssh_identity = cnf.get(conf_file,"key")
		cmd_alias = "alias %s='ssh -i %s %s@%s'\n" % (conf_file,ssh_identity,ssh_user,ssh_host)
		f = open("%s/ggssh.alias" % (ggssh_base),"a")
		f.write(cmd_alias)
		f.close()

def ggssh_config():
	ssh_alias = raw_input("Alias Name: ")
	
	# if alias name doesn't exist
	if not(os.path.exists("%s/%s" % (ggssh_base_hosts,ssh_alias))):
		print("Error: %s: alias doesn't exist" % (ssh_alias))
		sys.exit(2)

	cnf = ConfigParser.ConfigParser()
	cnf.read("%s/%s" % (ggssh_base_hosts,ssh_alias))
	ssh_user = cnf.get(ssh_alias,"user")
	ssh_host = cnf.get(ssh_alias,"host")
	ssh_identity = cnf.get(ssh_alias,"key")
	
	tmp_ssh_user = raw_input("SSH User [%s]: " % (ssh_user))
	tmp_ssh_host = raw_input("SSH IP/Host [%s]: " % (ssh_host))
	tmp_ssh_identity = raw_input("SSH Identity Key [%s]: " % (ssh_identity))
	
	if (tmp_ssh_user != ""):
		ssh_user = tmp_ssh_user
	if (tmp_ssh_host != ""):
		ssh_host = tmp_ssh_host
	if (tmp_ssh_identity != ""):
		ssh_identity = tmp_ssh_identity
		
	# write out config to file
	os.system("echo -n '' > %s/%s" % (ggssh_base_hosts,ssh_alias))
	ssh_config_strings = "[%s]\n\nuser=%s\nhost=%s\nkey=%s\n\n" % (ssh_alias,ssh_user,ssh_host,ssh_identity)	
	f = open("%s/%s" % (ggssh_base_hosts,ssh_alias),"a")
	f.write(ssh_config_strings)
	f.close()
	
def ggssh_show():
	fopen = os.popen("cat %s/ggssh.alias" % (ggssh_base)).readlines()
	for line in fopen:
		print line.strip()

	
if (len(sys.argv) < 2):
	ggssh_usage()
	
if (sys.argv[1] == "add"):
	ggssh_add()
elif (sys.argv[1] == "config"):
	ggssh_config()
elif (sys.argv[1] == "apply"):
	ggssh_apply()
elif (sys.argv[1] == "show"):
	ggssh_show()
else:
	ggssh_usage()

