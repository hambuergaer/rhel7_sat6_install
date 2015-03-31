#!/usr/bin/env python
##################################################################################################
# install_sat60.py
#
# Description:
# ------------
# This script will help you install a disconnected Red Hat Satellite 6.0 on top of a base RHEL 7 
# installation. 
#
# Author:               Frank Reimer
# Version:              0.1
# Creation Date:        2015-03-30
# --------------------------------------------------
#
# Version History:
#
# 2015-03-30: Initial script start. 
#
##################################################################################################

# Adding script version
script_version=str(0.1)

# Importing some modules
import os
import re
import sys
import platform
import commands
import subprocess
import crypt
import getpass
import json
from optparse import OptionParser

# Some variables
hostname = platform.node()

# Check if service is running
output = subprocess.check_output(['ps', '-A'])
if 'firewalld' in output:
	print("INFO: Firewall is up an running! Will add needed firewall rules.")
else:
	print "INFO: Firewall is NOT running. Are you sure you want to run this system without a local firwall?"	

# Check if operating system fulfills appropriate requirements
# Find out Red Hat major release
os_major_release = str(open('/etc/redhat-release','r').read().split(' ')[6].split('.')[0])
if os_major_release == "7":
	print "INFO: OS prereqs fulfilled: you are running " + str(platform.linux_distribution())
else:
	print "ERROR: Please ensure that you are running RHEL 7." 

# Cheeck if FQDN is resolvable by DNS
try:
	subprocess.check_call(['nslookup', hostname])
	print "INFO: Hostname " + platform.node() + " is resolvable via DNS."
except:
	
	print "ERROR: Please make sure that your hostname is resolvable via DNS."
	sys.exit(1)

# Check if NTP is working
try:
	ntpd = subprocess.check_output(['ps', '-A'])
	if "ntpd" in ntpd:
		print "INFO: NTP seems working."
	else:
		print "ERROR: Please make sure that NTP is working on your client."	
		sys.exit(1)	
except:
	print "ERROR: Please make sure that NTP is working in your client."	
	sys.exit(1)

# Register system at Red Hat Network
print "="*60
print "INFO: I will now register your system " + hostname + " to Red Hat Network. Please answer the followig questions:"
rhn_user = raw_input("Please enter your RHN user: ")
print "INFO: Now enter your RHN password: "
#rhn_password = crypt.crypt(getpass.getpass())
rhn_password = getpass.getpass()
a="--username="+rhn_user
b="--password="+rhn_password
try:
	subprocess.call(['subscription-manager', 'register', '--force', a, b])
	print "INFO: Your system is now registered at Red Hat Network."
except:
	print "ERROR: Can`t register your system at Red Hat Network."
	sys.exit(1)

try:
	print "INFO: Try to auto-attach to a valid subscription."
	subprocess.call(['subscription-manager', 'attach', '--auto'])
except:
	print "ERROR: Was not able to auto-attach to a valid subscription."
	sys.exit(1)

rhn_pool_id= raw_input("INFO: Now enter your Subscription Pool ID: ")
c="--pool="+rhn_pool_id

try:
	subprocess.call(['subscription-manager', 'subscribe', c])
	print "INFO: Your system is now subscribed to pool " + rhn_pool_id
except:
	print "ERROR: Could not subscribe your system to pool id " + rhn_pool_id
	sys.exit(1)	

try:
	subprocess.call(['subscription-manager', 'repos', '--disable "*"'])
except:
	print "ERROR: Could not disable YUM repos."
	sys.exit(1)

try:
	print "INFO: Enable needed YUM repos."
	subprocess.call(['subscription-manager', 'repos', '--enable rhel-7-server-rpms', '--enable rhel-server-rhscl-7-rpms', '--enable rhel-7-server-satellite-6.0-rpms'])
except:
	print "ERROR: Could not enable needed YUM repos."
	sys.exit(1)


# subscription-manager register --username= --password= --proxy= --proxyuser= --proxypassword= --force
