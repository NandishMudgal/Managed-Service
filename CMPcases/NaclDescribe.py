import boto3
import logging
from logging import handlers
import sys
import traceback
import csv


ec2conn = boto3.client('ec2')
regions = ec2conn.describe_regions()['Regions']
for region in regions:
        rule = []
        associ = []
        print region['RegionName']
        ec2 = boto3.client('ec2',region_name=region['RegionName'])
        desc_nacl = ec2.describe_network_acls()
        for Ass in desc_nacl['NetworkAcls']:
                associ.append(Ass)
                for rules in Ass['Entries']:
                        rule.append(rules)
                        #print len(Ass['Entries'])
                        cidr = ""
                        if 'CidrBlock' or 'Ipv6CidrBlock' in rules:
                                try:
                                        cidr += rules['CidrBlock']
                                except:
                                        cidr += rules['Ipv6CidrBlock']
                        #print cidr
                        if 'PortRange' in rules:
                                fromPort = rules['PortRange']['From']
                                toPort = rules['PortRange']['To']
                                print rules['RuleNumber'], rules['Protocol'], fromPort, toPort, cidr, rules['Egress']
                                #for i in range(1,len(rule)):
                                with open('test.csv','w') as fp:
                                        a = csv.writer(fp,delimiter=',')
                                        data=[['RuleNumber','Protocol','fromPort','toPort','source','Egress'],
                                                [rules['RuleNumber'],rules['Protocol'],fromPort,toPort,cidr,rules['Egress']]]
                                        a.writerows(data)
                        print rules['RuleNumber'], rules['Protocol'], cidr, rules['Egress']
                        #for i in range(1,len(rule)):
                        with open('test.csv','w') as fp:
                                a = csv.writer(fp,delimiter=',')
                                data=[['RuleNumber','Protocol','fromPort','toPort','source','Egress'],
                                        [rules['RuleNumber'],rules['Protocol'],'','',cidr,rules['Egress']]]
                                a.writerows(data)
