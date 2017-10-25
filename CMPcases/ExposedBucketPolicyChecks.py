#!/usr/bin/env python
import boto3
import ast

public_buckets = []
s3 = boto3.client('s3')
buckets_desc = s3.list_buckets()
for bucket in buckets_desc['Buckets']:
	try:
		bucket_policy = s3.get_bucket_policy(Bucket=bucket['Name'])
		policy = bucket_policy['Policy']
		policy_check = ast.literal_eval(policy)
		policyStat = policy_check['Statement']
		for BuckPolicy in policyStat:
			if BuckPolicy['Effect'] == 'Allow' and BuckPolicy['Principal'] == '*':
				if 'Condition' in BuckPolicy:
					condition_check=BuckPolicy["Condition"]
					ipAdd=condition_check["IpAddress"]
					if '0.0.0.0/0' in ipAdd["aws:Referer"]:
						public_buckets.append(bucket['Name'])
					else:
						pass
				else:
					public_buckets.append(bucket['Name'])
			else:
				pass

	except:
		pass

for bucket in buckets_desc['Buckets']:
	try:		
		buket_acl = s3.get_bucket_acl(Bucket=bucket['Name'])
		for acl in buket_acl['Grants']:
			if 'Group' in acl['Grantee']['Type']:
				if 'AllUsers' in acl['Grantee']['URI']:
					public_buckets.append(bucket['Name'])
				else:
					pass
			else:
				pass
	except:
		pass


exposedPolicy = list(set(public_buckets))
if exposedPolicy != []:
	print "Buckets which having public bucket policy:\n" + "+-------------------------------------------------+"
	for expPolicy in exposedPolicy:
		print expPolicy
else:
	pass



