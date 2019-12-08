import ldap3, sys, configparser, re 
from ldap3 import Connection, ALL, core, MODIFY_REPLACE

username = sys.argv[1]
password = sys.argv[2]
base_dn = sys.argv[3]
domain = sys.argv[4]
desc =  sys.argv[5]
user_dn = 'cn=' + username + ',' + base_dn
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
if user_search:
    print ("User", username, "already exists in AD") 
    sys.exit(1)

# Lets build our user: Disabled to start (514)
user_attrs = {'objectClass': ['top', 'person', 'organizationalPerson', 'user'], \
                                            'cn': username, \
                                            'userPrincipalName': username + '@' + domain, \
                                            'sAMAccountName': username, \
                                            'givenName': username, \
                                            'sn': username, \
                                            'displayName': username, \
                                            'description': desc, \
                                            'userAccountControl': '514'}

# if base_dn like svc 
if re.match(r"OU=SVC*", base_dn):
  # Prep the password
  unicode_pass = '\"' + password + '\"'
  password_value = unicode_pass.encode('utf-16-le')
  add_pass = {'unicodePwd': [(MODIFY_REPLACE, [password_value])]}
  # 512 will set user account to enabled.  65536 sets password does not expire
  mod_acct = {'userAccountControl': [(MODIFY_REPLACE, '66048')]}

# Add the new user account
ldap_connection.add(user_dn, attributes=user_attrs)

if ldap_connection.result['result'] !=0:
    print ("Error adding new user: %s" % ldap_connection.result['description'])
    sys.exit(1)

# if base_dn like svc 
if re.match(r"OU=SVC*", base_dn):
  # Add the password
  ldap_connection.modify(user_dn, add_pass)
  if ldap_connection.result['result'] != 0:
      print ("Error setting password: %s" % ldap_connection.result['description'])
      sys.exit(1)

  # Change the account back to enabled
  ldap_connection.modify(user_dn, mod_acct)
  if ldap_connection.result['result'] != 0:
      print ("Error enabling user: %s" % ldap_connection.result['description'])
      sys.exit(1)

# LDAP unbind
ldap_connection.unbind()

# All is good
print ('Successfully created ' + user_dn)

