
# Oulets Project

Outlets is web application that will alow users to create oulets and their items in order to display it to all vistors of this web page.


## Included Files
1. database_setup.py
1. outletDB.db
1. outlet.py
1. templets folder
1. static folder

## Tool you need to install
1. Virtual Box
1. Vagrant
1. Python 3.6.2
1. Flask framework

## Database Structure
The databse contains the following three tables: 
1. **user** - contains all registered users.  
1. **outlet** - contains all outlets information.
1. **item** - contains all items of the outlets.

## Runing The Project
1. Install Vagrant and VirtualBox
1. Launch the Vagrant VM (vagrant up)
1. Write your Flask application locally in the vagrant/catalog directory (which will automatically be synced to /vagrant/catalog within the VM).
1. Run  `python /vagrant/catalog/online_store/databse_setup.py` , this is for the first time to create database.
1. Run Run your application within the VM `python /vagrant/catalog/online_store/outlet.py`
1. Access and test your application by visiting http://localhost:5000 locally