import sys, ldap3, configparser
from ldap3 import Connection, ALL, core

base_dn = sys.argv[1]
username = sys.argv[2]
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
                                            attributes = ['memberof'])

# Check the results
if not user_search: 
    print ("User", username, "not found in AD:")
    sys.exit(1)

print (ldap_connection.entries[0])

# LDAP unbind
ldap_connection.unbind()

