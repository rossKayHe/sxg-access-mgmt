import ldap3, sys, configparser
from ldap3 import Connection, ALL, core

groupname = sys.argv[1]
base_dn = sys.argv[2]
desc =  sys.argv[3]
f = open(sys.path[0] + '/config/ginfo.txt', "rb").read()
info =  f.replace(b'\n',b'\r\n').decode('ascii')
group_dn = 'cn=' + groupname + ',' + base_dn
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

# Check and see if group exists
user_search = ldap_connection.search(base_dn, '(&(name=' +
                                            groupname +
                                            ')(objectClass=group))',
                                            attributes = ['distinguishedName'])

# Check the results
if user_search:
    print ("Group", groupname, "already exists in AD") 
    sys.exit(1)

print (info)

# Lets build our group
group_attrs = {'objectClass': ['group'], 'cn': groupname, \
                                            'sAMAccountName': groupname, \
                                            'groupType': '-2147483646', \
                                            'info': info, \
                                            'description': desc }
# Add the new group
ldap_connection.add(group_dn, attributes=group_attrs)

if ldap_connection.result['result'] !=0:
    print ("Error adding new group: %s" % ldap_connection.result['description'])
    sys.exit(1)

# LDAP unbind
ldap_connection.unbind()

# All is good
print ('Successfully created ' + group_dn)

