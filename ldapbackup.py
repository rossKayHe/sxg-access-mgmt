import sys, ldap3, datetime, configparser, boto3, subprocess
from botocore.config import Config
from pprint import pprint
from ldap3 import Server, Connection, ALL, core

dns = ['Prod','Test','SVCProd', 'SVCTest']
dn_suffix = ',OU=XMLGateway,OU=Accounts,DC=nordstrom,DC=net'

config = configparser.ConfigParser()
config.read(sys.path[0] +'/config/app.ini')
usr =  config.get('Section1', 'username')
data =  config.get('Section1', 'data')
awsuser = config.get('Section1', 'awsuser')
awsdata = config.get('Section1', 'awsdata')

subprocess.run("/usr/local/bin/awscreds --user " + awsuser + " --password '" + awsdata +"' --role arn:aws:iam::572824850745:role/NORD-Prod_ESB-DevUsers-Team --once", shell=True)

# LDAP connection
try:
    ldap_connection=Connection('ldaps://ldap0319.nordstrom.net:636',usr,data,auto_bind=True)
except core.exceptions.LDAPBindError as e:
    print ("Error connecting to LDAP server: %s" % e) 
    sys.exit(1)

for base_dn in dns:
    user_search = ldap_connection.search('OU='+base_dn+dn_suffix, 
                                        '(&(objectCategory=person)(objectClass=user)(name=*))')
                                        #attributes = ['NordSMPwData'])
    f = open(sys.path[0] + '/backup/' + datetime.date.today().isoformat() + base_dn  + ".txt", "w")
    for entry in ldap_connection.response:
        y = (entry.copy())
        del y['raw_dn']
        del y['raw_attributes']
        del y['type']
        f.write(str(y).replace('\'','"')+'\n')
    f.close()

if not user_search or len(ldap_connection.entries) < 1:
    print ("Error: Searching for users")
    sys.exit(1)

for base_dn in dns:
    group_search = ldap_connection.search('OU='+base_dn+dn_suffix,'(&(objectCategory=group)(name=*))',attributes = ['member','description','info'])
    f = open(sys.path[0] + '/backup/' + datetime.date.today().isoformat() + base_dn  + ".txt", "a")
    f.write('\n\n\n\n\n')
    for entry in ldap_connection.response:
        y = (entry.copy())
        del y['raw_dn']
        del y['raw_attributes']
        del y['type']
        f.write(str(y).replace('\'','"')+'\n')
    f.close()

if not group_search or len(ldap_connection.entries) < 1:
    print ("Error: Searching groups")
    sys.exit(1)


session = boto3.Session(profile_name='nordstrom-federated')
s3 = session.resource('s3', config=Config(proxies={'https': 'webproxy.nordstrom.net:8181','http': 'webproxy.nordstrom.net:8181'}))
for base_dn in dns:
    s3.meta.client.upload_file(sys.path[0] + '/backup/' + datetime.date.today().isoformat() + base_dn  + ".txt", 'prod-sxg-accessmgmt', datetime.date.today().isoformat() + base_dn  + ".txt")


