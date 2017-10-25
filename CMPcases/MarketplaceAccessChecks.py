#!/usr/bin/env python

import boto3

usernames = []
Allowed_users = []
denyUsers = []
marketplaceAccess = []
group_name = "REAN-AllUsers-Deny"
min_users = 100
iam = boto3.client('iam')
lsusers = iam.list_users()
for user in lsusers['Users']:
    usernames.append(user['UserName'])

if (len(usernames)) >= min_users:
    Marker = lsusers['Marker']
    while Marker:
        userlist = iam.list_users(Marker=Marker)
        for user in userlist['Users']:
            usernames.append(user['UserName'])
        if userlist['IsTruncated'] == True:
            Marker=userlist['Marker']
        else:
            Marker= None

for groups in usernames:
    group_details = iam.list_groups_for_user(UserName=groups)
    group = group_details['Groups']
    userGroup = []
    for deny_group in group:
        userGroup.append(deny_group['GroupName'])
    if group_name in userGroup:
        denyUsers.append(groups)
    else:
        Allowed_users.append(groups)    

for marketPolicyUser in Allowed_users:
    managed_user_policies = iam.list_attached_user_policies(UserName=marketPolicyUser)
    managedPolicy = managed_user_policies['AttachedPolicies']
    marketPlacePolicy = []
    for policy in managedPolicy:
        marketPlacePolicy.append(policy['PolicyName'])
    if "AWSMarketplaceFullAccess" in marketPlacePolicy:
        marketplaceAccess.append(marketPolicyUser)
    if "AWSMarketplaceManageSubscriptions" in marketPlacePolicy:
        marketplaceAccess.append(marketPolicyUser)

if marketplaceAccess != []:
    print "Following IAM users having Marketplace Access: \n" + "+--------------------------------------------------------------+"
    for UsersWithMarketplaceAccess in marketplaceAccess:
        print UsersWithMarketplaceAccess
else:
    pass


