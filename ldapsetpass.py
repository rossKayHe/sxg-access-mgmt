import ldap3, sys, configparser
from ldap3 import Connection, ALL, core, MODIFY_REPLACE

base_dn = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]
user_dn = 'CN=' + username + ',' + base_dn
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
user_search = ldap_connection.search(base_dn, '(&(sAMAccountName=' +
                                            username +
                                            ')(objectClass=person))',
                                            attributes = ['distinguishedName'])

# Check the results
if not user_search:
    print ("User", username, "not found in AD:")
    sys.exit(1)


PASSWORD_ATTR = "unicodePwd"

# Set AD password
unicode_pass = "\"" + password + "\""
password_value = unicode_pass.encode("utf-16-le")
add_pass = {PASSWORD_ATTR: [(MODIFY_REPLACE, [password_value])]}

# Replace password
ldap_connection.modify(user_dn, add_pass)
if ldap_connection.result['result'] == 0:
  print ("Active Directory password for " + username + " was set successfully")
else:
  sys.stderr.write('Error setting AD password for: ' + username + '\n')
  sys.stderr.write('Message: ' + ldap_connection.result['description'] + '\n')
  sys.exit(1)

# LDAP unbind
ldap_connection.unbind()


