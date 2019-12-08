import sys, ldap3, configparser
from ldap3 import Connection, ALL, core, MODIFY_ADD

base_dn = sys.argv[1]
username = sys.argv[2]
groupname = sys.argv[3]
user_dn = 'CN=' + username + ',' + base_dn
group_dn = 'CN=' + groupname + ',' + base_dn
config = configparser.ConfigParser()
config.read(sys.path[0] + '/config/app.ini')
usr =  config.get('Section1', 'username')
data =  config.get('Section1', 'data')

# LDAP connection
try:
    ldap_connection=Connection('ldaps://ldap0319.nordstrom.net:636',usr,data,auto_bind=True)
except core.exceptions.LDAPBindError as e:
    print ("Error connecting to LDAP server: %s" % e)
    sys.exit(1)

# Check and see if user exists
user_search = ldap_connection.search(base_dn,
                                        '(&(name=' +
                                        username +
                                        ')(objectClass=person))',
                                        attributes = ['distinguishedName'])
if not user_search:
    print ("Error finding username: " + username + " in AD.")
    sys.exit(1)

group_search = ldap_connection.search(base_dn,
                                        '(&(name=' +
                                        groupname +
                                        ')(objectClass=group))',
                                        attributes = ['distinguishedName','member'])
if not group_search:
    print ("Error finding groupname: " + groupname)
    sys.exit(1)

for dn in ldap_connection.entries[0]['member']:
    if user_dn in dn:
        print (user_dn + ' is already in ' +  groupname)
        sys.exit(1)
 
# Add account to group
mod_list = {'member': [(MODIFY_ADD, user_dn)]}
ldap_connection.modify(group_dn, mod_list)
if ldap_connection.result['result'] != 0:
    print ("Error adding " + username + " to " + groupname)
    sys.exit(1)

# LDAP unbind
#ldap_connection.unbind()

# All is good
print ('Successfully added ' + username + ' to ' + groupname)

