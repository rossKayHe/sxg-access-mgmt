import ldap3, sys, configparser
from ldap3 import Connection, ALL, core, MODIFY_REPLACE

base_dn = sys.argv[1]
username = sys.argv[2]
user_dn = 'CN=' + username + ',' + base_dn
nordSMPwData = sys.argv[3]
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
user_search = ldap_connection.search(base_dn, '(&(name=' +
                                            username +
                                            ')(objectClass=person))',
                                            attributes = ['distinguishedName'])

# Check the results
if not user_search:
    print ("User", username, "not found in AD:")
    sys.exit(1)

# Set NordSMPwData value
add_pass = {'NordSMPwData': [(MODIFY_REPLACE, nordSMPwData)]}

# Replace password
ldap_connection.modify(user_dn, add_pass)
if ldap_connection.result['result'] == 0:
  print ("NordSMPwData for " + username + " was set successfully")
else:
  sys.stderr.write('Error setting NordSMPwData for: ' + username + '\n')
  sys.stderr.write('Message: ' + ldap_connection.results['description'] + '\n')
  sys.exit(1)

# LDAP unbind
ldap_connection.unbind()


