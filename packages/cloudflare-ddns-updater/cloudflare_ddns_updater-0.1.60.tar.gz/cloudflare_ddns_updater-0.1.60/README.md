This script updates a dns record in your Cloudflare account to match 
your current public IP address.\
First it checks your IP address, and if it is different from the IP address in your 
Cloudflare dns record, it updates the dns record in Cloudflare.\
It will run automatically at preset intervals.

### Prerequisites
To run this script you need a Cloudflare User API Token \
with the following Permissions:\
Zone - Zone - Read  
Zone - DNS - Edit\
and the following Zone Resources:\  
Include - Specific zone - yourdomain.xxx

These permissions are necessary to check the names and IDs of your dns records (Zone Read)\
and to change the IP address of a particular record (DNS Edit).

During setup, the script checks if crontab is installed and accessible.\
If not, it will exit. In this case setup crontab or run as root.\
In Debian 12 all users have crontab available\
In Alpine linux the user needs to run crontab -e, and write a comment line.

### How to obtain a Cloudflare API Token
Login to Cloudflare\
Click on My Profile (top right)\
Click on API Tokens\
Click on the 'Create Token' button\
Click on the 'Use template' button of Edit zone DNS\
Modify Permissions so that you have the following settings:\
Zone - Zone - Read  \
Zone - DNS - Edit    \
and the following Zone Resources:\
Include - Specific zone - yourdomain.xxx")\
Click on the 'Continue to summary' button\
Click on the 'Create Token' button.\
Save the Token


### Security
The Cloudflare token is saved in a json file readable only by the user (and root).
In my setup, it is in a VM with only one user, so it is not a problem, 
but if your setup is different, please consider this. 

Once '--setup' has run, you may remove the 'Zone Read' permission.\
By doing this, your token will not be able to read your A records. It will 
only have access to the particular record specified in setup.\
'--setup' will not be able to fetch your Zone and dns Record IDs anymore, but
 you will still be able to run the script with all the other arguments.
  

### Installation
To install on recent Linux systems use pipx.\
On older systems you can use pip.
  
On Debian or Ubuntu  
- `apt install pipx`

On Alpine Linux  
- `apk add pipx`  

Once installed:  
- `pipx ensurepath`  
- Logout and login again (or reboot)  
- `pipx install cloudflare-ddns-updater`  
  
### Setup
To setup the program  
- `cloudflare-ddns-updater --setup`  
  
To change IP check interval  
- `cloudflare-ddns-updater --cron`  
  
To stop automatic ip update  
- `cloudflare-ddns-updater --stop`  
  
To resume automatic IP update  
- `cloudflare-ddns-updater --start`  

To change log level
- `cloudflare-ddns-updater --logs`  

To remove all files created by the script  
- `cloudflare-ddns-updater --cleanup`  

To check the logs
- follow the log file path shown after installation
  
To uninstall
- `cloudflare-ddns-updater --cleanup\`
- `pipx uninstall cloudflare-ddns-updater`

Changes:\
0.1.60 - Improved hidden token input\
0.1.59 - Token input is hidden (where possible)\
0.1.58 - Bug fix and small ux change\
0.1.57 - Bug fixes + Now shows current intervals in --cron\
0.1.42 - Small ux changes - Log the log changes
0.1.41 - Now log levels actually change!\
0.1.40 - Changed required python version for compatibility
0.1.39 - Added choice of log levels\
0.1.38 - On first setup runs ip-updater once without waiting for cron job\
0.1.37 - Bug fix\
0.1.36 - ux change: user chooses from existing records and has option to create new one\
0.1.35 - Now forces update at every cron change and on first run only after setup\
0.1.34 - Further secured folders\
0.1.33 - secured folders - added check for crontab


TODO\
implement no echo for token input