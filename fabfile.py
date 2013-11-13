# Copyright 2013 Mathias WOLFF
# This file is part of pyfreebilling.
# 
# pyfreebilling is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# pyfreebilling is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with pyfreebilling.  If not, see <http://www.gnu.org/licenses/>
from fabric.api import * from fabric.colors 
import green, red

def build_commit(warn_only=True):
	"""
	Build a commit
	* prompt user for the name of the local feature branch you are developing 
	* prompt user for the name of the remote branch you want to push your changes to 
	* checkout your local feature branch 
	* git track add new and modified files 
	* prompt user for a commit message 
	* run the git commit command with the specified commit message 
	* checks out the local copy of the remote branch 
	* does a git pull to pull any changes from that remote branch 
	* checks out the local feature branch 
	* rebases the local feature branch off the recently updated local copy of the remote branch 
	* checks out the local copy of the remote branch 
	* merges the work from your recently rebased local feature branch into the local copy of the remote branch 
	* pushes the local copy of the remote branch to origin 
	* checks out the local feature branch so that work can continue
	
	Run the command : 
	
	::
	
	    fab build_commit
	""" 
	local_branch = prompt("checkout branch: ")
	rebase_branch = prompt("rebase branch: ")
	
	local('git checkout %s' % local_branch)
	local('git add .')
	local('git add -u .')
	
	message = prompt("commit message: ")
	
	local('git commit -m "%s"' % message)
	local('git checkout %s' % rebase_branch)
	local('git pull origin %s' % rebase_branch)
	local('git checkout %s' % local_branch)
	local('git rebase %s' % rebase_branch)
	local('git checkout %s' % rebase_branch)
	local('git merge %s' % local_branch)
	local('git push origin %s' % rebase_branch)
	local('git checkout %s' % local_branch)
	
def server():
	"""
	This pushes to the EC2 instance defined below
	This function handles the connection information
	""" 
	# The Elastic IP to your server 
	env.host_string = '999.999.999.999' 
	# your user on that system 
	env.user = 'ubuntu' 
	# Assumes that your *.pem key is in the same directory as your fabfile.py 
	env.key_filename = 'my_ec2_security_group.pem'

def staging():
	"""
	deployment script :
	The above command switches to the vhost directory, installs requirements, collects static files, syncs and migrates the database, and then restarts the web application process.
	
	Run the command : fab server staging
	""" 
	# path to the directory on the server where your vhost is set up 
	path = "/home/ubuntu/www/dev.yaconiello.com" 
	# name of the application process 
	process = "staging" 
	
	print(red("Beginning Deploy:")) 
	with cd("%s/app" % path) : 
		run("pwd") 
		print(green("Pulling master from GitHub...")) 
		run("git pull origin master") 
		print(green("Installing requirements...")) 
		run("source %s/venv/bin/activate && pip install -r requirements.txt" % path)
		print(green("Collecting static files...")) 
		run("source %s/venv/bin/activate && python manage.py collectstatic --noinput" % path)
		print(green("Syncing the database...")) 
		run("source %s/venv/bin/activate && python manage.py syncdb" % path) 
		print(green("Migrating the database...")) 
		run("source %s/venv/bin/activate && python manage.py migrate" % path)
		print(green("Restart the uwsgi process")) 
		run("sudo service %s restart" % process) 
	print(red("DONE!"))
