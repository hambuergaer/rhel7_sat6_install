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
# Version:              0.3
# Creation Date:        2015-03-30
# --------------------------------------------------
#
# Version History:
#
# 2015-03-30: Initial script start.
# 2015-04-10: Working on script art: writing needed definitions
# 2015-05-11: Add function add_firewall_rules()
#
##################################################################################################

# Adding script version
script_version=str(0.3)

# Importing some modules
import os
import re
import sys
import platform
import commands
import subprocess
import crypt
import getpass

# Some variables
hostname = platform.node()

# Check for service
def check_for_service(servicename):
	output = subprocess.check_output(['ps', '-A'])
	if servicename in output:
        	return 0
	else:
        	return 1

# Check if operating system is RHEL 7
def check_osversion():
	os_major_release = str(open('/etc/redhat-release','r').read().split(' ')[6].split('.')[0])
	if os_major_release == "7":	
		return 0
	else:
		return 1

# Check if system is already registered and subscribed to Red Hat CDN.
def check_rhsm():
	command = '/usr/sbin/subscription-manager list | grep -e Subskribiert -e Subscribed'
	if subprocess.call(command, shell=True, stdout=subprocess.PIPE) == 0:
		return 0
	else:
		return 1
# Register and subscribe the system to Red Hat CDN and auto-attach to neede subscription.
def register_rhsm(*multipleargs):
	user = "--username="+rhn_user
	password = "--password="+rhn_password
	try:
        	subprocess.call('subscription-manager', 'register', '--force', user, password, stdout=subprocess.PIPE)
		subprocess.call('subscription-manager', 'attach', '--auto', stdout=subprocess.PIPE)
        	print "INFO: Your system is now registered at Red Hat Network."
	except:
        	print "ERROR: Can`t register your system at Red Hat Network."
        	sys.exit(1)

#def enable_repos():

#def attach_poolid():

# Add needed firewall rules permanently to firewalld.
def add_firewall_rules():
	firewallcmd = '/usr/bin/firewall-cmd'
	try:
		subprocess.call(firewallcmd, '--permanent', '--direct', '--add-port="443/tcp"', '--add-port="5671/tcp"', '--add-port="80/tcp"', '--add-port="8140/tcp"', '--add-port="9090/tcp"', '--add-port="8080/tcp"')
		subprocess.call(firewallcmd, '--permanent', '--direct', '--add-rule ipv4 filter OUTPUT 0 -o lo -p tcp -m tcp', '--dport 9200 -m owner --uid-owner foreman -j ACCEPT')
		subprocess.call(firewallcmd, '--permanent', '--direct', '--add-rule ipv6 filter OUTPUT 0 -o lo -p tcp -m tcp', '--dport 9200 -m owner --uid-owner foreman -j ACCEPT')
		subprocess.call(firewallcmd, '--permanent', '--direct', '--add-rule ipv4 filter OUTPUT 0 -o lo -p tcp -m tcp', '--dport 9200 -m owner --uid-owner katello -j ACCEPT')
		subprocess.call(firewallcmd, '--permanent', '--direct', '--add-rule ipv6 filter OUTPUT 0 -o lo -p tcp -m tcp', '--dport 9200 -m owner --uid-owner katello -j ACCEPT')
		subprocess.call(firewallcmd, '--permanent', '--direct', '--add-rule ipv4 filter OUTPUT 0 -o lo -p tcp -m tcp', '--dport 9200 -m owner --uid-owner root -j ACCEPT')
		subprocess.call(firewallcmd, '--permanent', '--direct', '--add-rule ipv6 filter OUTPUT 0 -o lo -p tcp -m tcp', '--dport 9200 -m owner --uid-owner root -j ACCEPT')
		subprocess.call(firewallcmd, '--permanent', '--direct', '--add-rule ipv4 filter OUTPUT 1 -o lo -p tcp -m tcp', '--dport 9200 -j DROP')
		subprocess.call(firewallcmd, '--permanent', '--direct', '--add-rule ipv7 filter OUTPUT 1 -o lo -p tcp -m tcp', '--dport 9200 -j DROP')
		subprocess.call(firewallcmd, '--complete-reload')
	except:
        	print "ERROR: Can`t set appropriate firewall rules. Exit."
        	sys.exit(1)

############# MAIN #############

# Check if operating system is RHEL 7
if check_osversion() == 0:
	print "INFO: Operating systems fits needed Operating System requirements."
else:
	print "ERROR: Make sure you are running Red Hat Enterprise Linux 7.x."
	sys.exit(1)

# Check if firewalld is running. If yes add needed firewall rules. 
if check_for_service('firewalld') == 0:
	print "INFO: Firewall is running. Will add needed permanent firewall rules."
	add_firewall_rules()
else:
	print "INFO: Firewall is not running. Doing nothing."

# Check if system is already registered to Red Hat CDN. If not register it and attach needed subscription.
if check_rhsm() == 0:
	print "INFO: Your system is already subscribed to Red Hat CDN."
	print "INFO: Will now enable needed YUM repositories."
else:
	print "INFO: Your system needs to be subscribed to Red Hat CDN."
	print "INFO: I will now register your system " + hostname + " to Red Hat Network. Please answer the followig questions:"
	use_proxy = raw_input("Do you use a Proxy server? (y/n): ")
	while not use_proxy:
		print "Please enter either 'y' or 'n'."
		use_proxy = raw_input("Do you use a Proxy server? (y/n): ")
	if use_proxy == "y" or use_proxy == "Y":
		print "Answer was yes!"
	if use_proxy == "n" or use_proxy == "N":
		rhn_user = raw_input("Please enter your RHN user: ")
		print "Now enter your RHN password: "
		rhn_password = getpass.getpass()
		register_rhsm(rhn_user, rhn_password)
	else:
		sys.exit(1)

############# END MAIN #############
