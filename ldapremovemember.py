import sys, ldap3, configparser
from ldap3 import Connection, ALL, core, MODIFY_DELETE

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

user_search = ldap_connection.search(base_dn, '(&(sAMAccountName=' +
                                            username +
                                            ')(objectClass=person))',
                                            attributes = ['distinguishedName'])

# Check the results
if not user_search:
    print ("User", username, "not found in AD:")
    sys.exit(1)

group_search = ldap_connection.search(base_dn, '(&(name=' +
                                            groupname +
                                            ')(objectClass=group))',
                                            attributes = ['distinguishedName','member'])

# Check the results
if not group_search:
    print ("Group", groupname, "not found in AD:")
    sys.exit(1)

found = False
for dn in ldap_connection.entries[0]['member']:
    if user_dn in dn:    
        found = True
if not found:        
    print (user_dn + ' is not in ' +  groupname)
    sys.exit(1)

mod_list = {'member': [(MODIFY_DELETE, user_dn)]}
ldap_connection.modify(group_dn, mod_list)

if ldap_connection.result['result']!=0:
    Print ("Error removing " + username + "from " + groupname)
    sys.exit(1)

# LDAP unbind
ldap_connection.unbind()

print ('Successfully removed ' + username + ' from ' + groupname)

