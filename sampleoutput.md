### Add a service account to a group
python ldapaddmember.py OU=SVCTest,OU=XMLGateway,OU=Accounts,DC=nordstrom,DC=net dwtegc general-availability-exttest
### Response
```text
Successfully added dwtegc to general-availability-exttest
```

### List service account group membership
python ldapmemberof.py OU=SVCTest,OU=XMLGateway,OU=Accounts,DC=nordstrom,DC=net dwtegc  
### Response
```text
[('CN=dwtegc,OU=SVCTest,OU=XMLGateway,OU=Accounts,DC=nordstrom,DC=net',
  {'memberOf': ['CN=general-egc-exttest,OU=SVCTest,OU=XMLGateway,OU=Accounts,DC=nordstrom,DC=net']})]
```

### Remove a service account from a group
python ldapremovemember.py OU=SVCTest,OU=XMLGateway,OU=Accounts,DC=nordstrom,DC=net dwtegc general-availability-exttest
### Response
```text
Successfully removed dwtegc from general-availability-exttest
```

### Create a service account
python ldapcreateuser.py aaatestUser My@P@zzW0rd OU=SVCTest,OU=XMLGateway,OU=Accounts,DC=nordstrom,DC=net nordstrom.net 'My test description'
### Response
```text
Successfully created cn=aaatestUser,OU=SVCTest,OU=XMLGateway,OU=Accounts,DC=nordstrom,DC=net
```

### Delete a service account
python ldapdlete.py aaatestUser OU=SVCTest,OU=XMLGateway,OU=Accounts,DC=nordstrom,DC=net person
### Response
```text
Successfully deleted cn=aaatestUser,OU=SVCTest,OU=XMLGateway,OU=Accounts,DC=nordstrom,DC=net
```

### Create a group
python36 ldapcreategroup.py aaaMyTestGroup2 OU=SVCTest,OU=XMLGateway,OU=Accounts,DC=nordstrom,DC=net 'My description'
### Response
```text
Successfully created cn=aaaMyTestGroup2,OU=SVCTest,OU=XMLGateway,OU=Accounts,DC=nordstrom,DC=net
```

### Delete a group
python ldapdlete.py aaaMyTestGroup OU=SVCTest,OU=XMLGateway,OU=Accounts,DC=nordstrom,DC=net group
### Response
```text
Successfully deleted cn=aaaMyTestGroup,OU=SVCTest,OU=XMLGateway,OU=Accounts,DC=nordstrom,DC=net
```

### List group members
python ldapmembers.py OU=SVCTest,OU=XMLGateway,OU=Accounts,DC=nordstrom,DC=net general-availability-exttest
### Response
```text
[('CN=general-availability-exttest,OU=SVCTest,OU=XMLGateway,OU=Accounts,DC=nordstrom,DC=net',
  {'member': ['CN=svtorder,OU=SVCTest,OU=XMLGateway,OU=Accounts,DC=nordstrom,DC=net']})]
```

### Set a service account's API key
python ldapsetapi.py OU=SVCTest,OU=XMLGateway,OU=Accounts,DC=nordstrom,DC=net dwtegc MyAPIpazz
### Response
```text
NordSMPwData for dwtegc was set successfully!
```

### Set a service account password
python ldapsetpass.py OU=SVCTest,OU=XMLGateway,OU=Accounts,DC=nordstrom,DC=net aaatestUser MudarorHqddjw18
### Response
```text
Active Directory password for aaatestUser was set successfully
```

### Failed to Remove a service account from a group as it is not in the group
python ldapremovemember.py OU=SVCTest,OU=XMLGateway,OU=Accounts,DC=nordstrom,DC=net aaatestUser general-availability-exttest
### Response
```text
CN=aaatestUser,OU=SVCTest,OU=XMLGateway,OU=Accounts,DC=nordstrom,DC=net is not in general-availability-exttest
```

### Failed to Add a service account to a group as it is already in the group
python ldapaddmember.py OU=SVCTest,OU=XMLGateway,OU=Accounts,DC=nordstrom,DC=net dwtegc general-availability-exttest
### Response
```text
CN=dwtegc,OU=SVCTest,OU=XMLGateway,OU=Accounts,DC=nordstrom,DC=net is already in general-availability-exttest
```