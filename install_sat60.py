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
from optparse import OptionParser


# Check if service is running
output = subprocess.check_output(['ps', '-A'])
if 'firewalld' in output:
    print("Firewall is up an running!")

# Check if operating system fulfills appropriate requirements
# Find out Red Hat major release
# open('/etc/redhat-release','r').read().split(' ')[6].split('.')[0]
os_major_release = str(open('/etc/redhat-release','r').read().split(' ')[6].split('.')[0])
if os_major_release == "7":
	print "OS prereqs fulfilled: you are running " + str(platform.linux_distribution())
else:
	print "ERROR: Please ensure that you are running RHEL 7." 
# Register system at Red Hat Network
# subscription-manager register --username= --password= --proxy= --proxyuser= --proxypassword= --force
