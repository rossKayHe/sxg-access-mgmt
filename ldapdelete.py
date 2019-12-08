import ldap3, sys, configparser
from ldap3 import Connection, ALL, core

objname = sys.argv[1]
base_dn = sys.argv[2]
objtype =  sys.argv[3]
obj_dn = 'cn=' + objname + ',' + base_dn
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

# Check and see if obj exists
user_search = ldap_connection.search(base_dn, '(&(name=' +
                                            objname +
                                            ')(objectClass=' + objtype + '))',
                                            attributes = ['distinguishedName'])

# Check the results
if not user_search:
    print (objtype, objname, "does not exist in AD") 
    sys.exit(1)

# Add the new user account
ldap_connection.delete(obj_dn)

if ldap_connection.result['result'] !=0:
    print ("Error adding new " + objtype + ": %s" % ldap_connection.result['description'])
    sys.exit(1)

# LDAP unbind
ldap_connection.unbind()

# All is good
print ('Successfully deleted ' + obj_dn)

