#!/usr/bin/env python
# +----------------------------------------------------------------------------------------+
# | Script  : This script create CPU,ELB,RDS,LAMBDA,NGINX,APACHE,TOMCAT Dashboards         |
# | Notes   : Please make sure your CSV file having valid inputs                           |
# | Notes   : Please confiure the Datadog credentials in datadogKeys.py                    |
# +----------------------------------------------------------------------------------------+
import sys
import csv
import getopt
from datadogKeys import *
from itertools import islice
from datadog import initialize, api
import ast

options = {
            'api_key': datadog_api_key,
            'app_key': datadog_app_key
           }

initialize(**options)
#======================================================================

queries = []
titles = []
existing_dashTitle = []
existing_queries = []
dashboard_id = []

board = api.Timeboard.get_all()
for desc_board in board['dashes']:
	dash_id = desc_board['id']
	desc_id = api.Timeboard.get(dash_id)
	dashboard_id.append(dash_id)
	dash_details = desc_id['dash']
	existing_dashTitle.append(dash_details['title'])
	for graph in dash_details['graphs']:
		query = graph['definition']
		for qry in query['requests']:
			queries.append(qry)


sysDashTitle = []
sysDashDesc = []
sysMetricTitle = []
system_queries = []

elbDashTitle = []
elbDashDesc = []
elbMetricTitle = []
elb_queries = []

rdsDashTitle = []
rdsDashDesc = []
rdsMetricTitle = []
rds_queries = []

lambdaDashTitle = []
lambdaDashDesc = []
lambdaMetricTitle = []
lambda_queries = []

apacheDashTitle = []
apacheDashDesc = []
apacheMetricTitle = []
apache_queries = []

nginxDashTitle = []
nginxDashDesc = []
nginxMetricTitle = []
nginx_queries = []

tomcatDashTitle = []
tomcatDashDesc = []
tomcatMetricTitle = []
tomcat_queries = []


csvFile = csv.reader(open("dashboardinput.csv", "rb"))
for i,line in enumerate(csvFile):
	if i >=1:
		if line[9] == "yes":
			if line[8] == "system metric":
				sysDashTitle.append(line[0])
				sysDashDesc.append(line[1])
				sysMetricTitle.append(line[7])
				if line[3] != "" and line[5] != "":
					moni_query = {"q": line[4]+":"+line[2]+"{"+line[3]+"} by {"+line[5]+"}"}
					if moni_query in queries:
						existing_queries.append(str(i))
					else:
						system_queries.append(moni_query)
				elif line[3] != "" and line[5] == "":
					moni_query = {"q": line[4]+":"+line[2]+"{*}"}
					if moni_query in queries:
						existing_queries.append(str(i))
					else:
						system_queries.append(moni_query)
				elif line[3] == "" and line[5] != "":
					moni_query = {"q": line[4]+":"+line[2]+"{*} by {"+line[5]+"}"}
					if moni_query in queries:
						existing_queries.append(str(i))
					else:
						system_queries.append(moni_query)
				else:
					print i, "Provide valid input for \"from\" and \"by value\" columns"

			elif line[8] == "elb metric":
				elbDashTitle.append(line[0])
				elbDashDesc.append(line[1])
				elbMetricTitle.append(line[7])
				if line[3] != "" and line[5] != "":
					moni_query = {"q": line[4]+":"+line[2]+"{"+line[3]+"} by {"+line[5]+"}"}
					if moni_query in queries:
						existing_queries.append(str(i))
					else:
						elb_queries.append(moni_query)
				elif line[3] != "" and line[5] == "":
					moni_query = {"q": line[4]+":"+line[2]+"{*}"}
					if moni_query in queries:
						existing_queries.append(str(i))
					else:
						elb_queries.append(moni_query)
				elif line[3] == "" and line[5] != "":
					moni_query = {"q": line[4]+":"+line[2]+"{*} by {"+line[5]+"}"}
					if moni_query in queries:
						existing_queries.append(str(i))
					else:
						elb_queries.append(moni_query)
				else:
					print i, "Provide valid input for \"from\" and \"by value\" columns"

			elif line[8] == "rds metric":
				rdsDashTitle.append(line[0])
				rdsDashDesc.append(line[1])
				rdsMetricTitle.append(line[7])
				if line[3] != "" and line[5] != "":
					moni_query = {"q": line[4]+":"+line[2]+"{"+line[3]+"} by {"+line[5]+"}"}
					if moni_query in queries:
						existing_queries.append(str(i))
					else:
						rds_queries.append(moni_query)
				elif line[3] != "" and line[5] == "":
					moni_query = {"q": line[4]+":"+line[2]+"{*}"}
					if moni_query in queries:
						existing_queries.append(str(i))
					else:
						rds_queries.append(moni_query)
				elif line[3] == "" and line[5] != "":
					moni_query = {"q": line[4]+":"+line[2]+"{*} by {"+line[5]+"}"}
					if moni_query in queries:
						existing_queries.append(str(i))
					else:
						rds_queries.append(moni_query)
				else:
					print i, "Provide valid input for \"from\" and \"by value\" columns"

			elif line[8] == "lambda metric":
				lambdaDashTitle.append(line[0])
				lambdaDashDesc.append(line[1])
				lambdaMetricTitle.append(line[7])
				if line[3] != "" and line[5] != "":
					moni_query = {"q": line[4]+":"+line[2]+"{"+line[3]+"} by {"+line[5]+"}"}
					if moni_query in queries:
						existing_queries.append(str(i))
					else:
						lambda_queries.append(moni_query)
				elif line[3] != "" and line[5] == "":
					moni_query = {"q": line[4]+":"+line[2]+"{*}"}
					if moni_query in queries:
						existing_queries.append(str(i))
					else:
						lambda_queries.append(moni_query)
				elif line[3] == "" and line[5] != "":
					moni_query = {"q": line[4]+":"+line[2]+"{*} by {"+line[5]+"}"}
					if moni_query in queries:
						existing_queries.append(str(i))
					else:
						lambda_queries.append(moni_query)
				else:
					print i, "Provide valid input for \"from\" and \"by value\" columns"

			elif line[8] == "apache metric":
				apacheDashTitle.append(line[0])
				apacheDashDesc.append(line[1])
				apacheMetricTitle.append(line[7])
				if line[3] != "" and line[5] != "":
					moni_query = {"q": line[4]+":"+line[2]+"{"+line[3]+"} by {"+line[5]+"}"}
					if moni_query in queries:
						existing_queries.append(str(i))
					else:
						apache_queries.append(moni_query)
				elif line[3] != "" and line[5] == "":
					moni_query = {"q": line[4]+":"+line[2]+"{*}"}
					if moni_query in queries:
						existing_queries.append(str(i))
					else:
						apache_queries.append(moni_query)
				elif line[3] == "" and line[5] != "":
					moni_query = {"q": line[4]+":"+line[2]+"{*} by {"+line[5]+"}"}
					if moni_query in queries:
						existing_queries.append(str(i))
					else:
						apache_queries.append(moni_query)

			elif line[8] == "nginx metric":
				nginxDashTitle.append(line[0])
				nginxDashDesc.append(line[1])
				nginxMetricTitle.append(line[7])
				if line[3] != "" and line[5] != "":
					moni_query = {"q": line[4]+":"+line[2]+"{"+line[3]+"} by {"+line[5]+"}"}
					if moni_query in queries:
						existing_queries.append(str(i))
					else:
						nginx_queries.append(moni_query)
				elif line[3] != "" and line[5] == "":
					moni_query = {"q": line[4]+":"+line[2]+"{*}"}
					if moni_query in queries:
						existing_queries.append(str(i))
					else:
						nginx_queries.append(moni_query)
				elif line[3] == "" and line[5] != "":
					moni_query = {"q": line[4]+":"+line[2]+"{*} by {"+line[5]+"}"}
					if moni_query in queries:
						existing_queries.append(str(i))
					else:
						nginx_queries.append(moni_query)

			elif line[8] == "tomcat metric":
				tomcatDashTitle.append(line[0])
				tomcatDashDesc.append(line[1])
				tomcatMetricTitle.append(line[7])
				if line[3] != "" and line[5] != "":
					moni_query = {"q": line[4]+":"+line[2]+"{"+line[3]+"} by {"+line[5]+"}"}
					if moni_query in queries:
						existing_queries.append(str(i))
					else:
						tomcat_queries.append(moni_query)
				elif line[3] != "" and line[5] == "":
					moni_query = {"q": line[4]+":"+line[2]+"{*}"}
					if moni_query in queries:
						existing_queries.append(str(i))
					else:
						tomcat_queries.append(moni_query)
				elif line[3] == "" and line[5] != "":
					moni_query = {"q": line[4]+":"+line[2]+"{*} by {"+line[5]+"}"}
					if moni_query in queries:
						existing_queries.append(str(i))
					else:
						tomcat_queries.append(moni_query)

			else:
				pass
		else:
			pass
	else:
		pass

if system_queries != []:
	i=0
	graph = []
	DashboardTitle = list(set(sysDashTitle))
	DashboardDesc = list(set(sysDashDesc))
	title = DashboardTitle[i]
	description = DashboardDesc[i]
	for qry in system_queries:
		definition = {
			"events": [],
			"requests": [qry],
			"viz": "timeseries"
		}
		
		dash_query = {
			"definition": definition,
			"title": sysMetricTitle[i]
		}	
		i+=1
		graph.append(dash_query)
	if title not in existing_dashTitle:
		api.Timeboard.create(title=title, description=description, graphs=graph)
	else:
		for ids in dashboard_id:
			desc_id = api.Timeboard.get(ids)
			dash_details = desc_id['dash']
			if title in dash_details['title']:
				api.Timeboard.update(ids, title=title, description=description, graphs=graph)
				print "CPU Dashboard is updated with new metrics"
			else:
				pass
else:
	print "System dashboard is already exist"


if elb_queries != []:
	i=0
	graph = []
	DashboardTitle = list(set(elbDashTitle))
	DashboardDesc = list(set(elbDashDesc))
	title = DashboardTitle[i]
	description = DashboardDesc[i]
	for qry in elb_queries:
		definition = {
			"events": [],
			"requests": [qry],
			"viz": "timeseries"
		}
		
		dash_query = {
			"definition": definition,
			"title": elbMetricTitle[i]
		}	
		i+=1
		graph.append(dash_query)
	if title not in existing_dashTitle:
		api.Timeboard.create(title=title, description=description, graphs=graph)
	else:
		for ids in dashboard_id:
			desc_id = api.Timeboard.get(ids)
			dash_details = desc_id['dash']
			if title in dash_details['title']:
				api.Timeboard.update(ids, title=title, description=description, graphs=graph)
				print "ELB Dashboard is updated with new metrics"
			else:
				pass
else:
	print "ELB dashboard is already exist"


if rds_queries != []:
	i=0
	graph = []
	DashboardTitle = list(set(rdsDashTitle))
	DashboardDesc = list(set(rdsDashDesc))
	title = DashboardTitle[i]
	description = DashboardDesc[i]
	for qry in rds_queries:
		definition = {
			"events": [],
			"requests": [qry],
			"viz": "timeseries"
		}
		
		dash_query = {
			"definition": definition,
			"title": rdsMetricTitle[i]
		}	
		i+=1
		graph.append(dash_query)
	if title not in existing_dashTitle:
		api.Timeboard.create(title=title, description=description, graphs=graph)
	else:
		for ids in dashboard_id:
			desc_id = api.Timeboard.get(ids)
			dash_details = desc_id['dash']
			if title in dash_details['title']:
				api.Timeboard.update(ids, title=title, description=description, graphs=graph)
				print "RDS Dashboard is updated with new metrics"
			else:
				pass
else:
	print "RDS dashboard is already exist"

if lambda_queries != []:
	i=0
	graph = []
	DashboardTitle = list(set(lambdaDashTitle))
	DashboardDesc = list(set(lambdaDashDesc))
	title = DashboardTitle[i]
	description = DashboardDesc[i]
	for qry in lambda_queries:
		definition = {
			"events": [],
			"requests": [qry],
			"viz": "timeseries"
		}
		
		dash_query = {
			"definition": definition,
			"title": lambdaMetricTitle[i]
		}	
		i+=1
		graph.append(dash_query)
	if title not in existing_dashTitle:
		api.Timeboard.create(title=title, description=description, graphs=graph)
	else:
		for ids in dashboard_id:
			desc_id = api.Timeboard.get(ids)
			dash_details = desc_id['dash']
			if title in dash_details['title']:
				api.Timeboard.update(ids, title=title, description=description, graphs=graph)
				print "LAMBDA Dashboard is updated with new metrics"
			else:
				pass
else:
	print "LAMBDA dashboard is already exist"

if apache_queries != []:
	i=0
	graph = []
	DashboardTitle = list(set(apacheDashTitle))
	DashboardDesc = list(set(apacheDashDesc))
	title = DashboardTitle[i]
	description = DashboardDesc[i]
	for qry in apache_queries:
		definition = {
			"events": [],
			"requests": [qry],
			"viz": "timeseries"
		}
		
		dash_query = {
			"definition": definition,
			"title": apacheMetricTitle[i]
		}	
		i+=1
		graph.append(dash_query)
	if title not in existing_dashTitle:
		api.Timeboard.create(title=title, description=description, graphs=graph)
	else:
		for ids in dashboard_id:
			desc_id = api.Timeboard.get(ids)
			dash_details = desc_id['dash']
			if title in dash_details['title']:
				api.Timeboard.update(ids, title=title, description=description, graphs=graph)
				print "APACHE Dashboard is updated with new metrics"
			else:
				pass
else:
	print "APACHE dashboard is already exist"

if nginx_queries != []:
	i=0
	graph = []
	DashboardTitle = list(set(nginxDashTitle))
	DashboardDesc = list(set(nginxDashDesc))
	title = DashboardTitle[i]
	description = DashboardDesc[i]
	for qry in nginx_queries:
		definition = {
			"events": [],
			"requests": [qry],
			"viz": "timeseries"
		}
		
		dash_query = {
			"definition": definition,
			"title": nginxMetricTitle[i]
		}	
		i+=1
		graph.append(dash_query)
	if title not in existing_dashTitle:
		api.Timeboard.create(title=title, description=description, graphs=graph)
	else:
		for ids in dashboard_id:
			desc_id = api.Timeboard.get(ids)
			dash_details = desc_id['dash']
			if title in dash_details['title']:
				api.Timeboard.update(ids, title=title, description=description, graphs=graph)
				print "NGINX Dashboard is updated with new metrics"
			else:
				pass
else:
	print "NGINX dashboard is already exist"

if tomcat_queries != []:
	i=0
	graph = []
	DashboardTitle = list(set(tomcatDashTitle))
	DashboardDesc = list(set(tomcatDashDesc))
	title = DashboardTitle[i]
	description = DashboardDesc[i]
	for qry in tomcat_queries:
		definition = {
			"events": [],
			"requests": [qry],
			"viz": "timeseries"
		}
		
		dash_query = {
			"definition": definition,
			"title": tomcatMetricTitle[i]
		}	
		i+=1
		graph.append(dash_query)
	if title not in existing_dashTitle:
		api.Timeboard.create(title=title, description=description, graphs=graph)
	else:
		for ids in dashboard_id:
			desc_id = api.Timeboard.get(ids)
			dash_details = desc_id['dash']
			if title in dash_details['title']:
				api.Timeboard.update(ids, title=title, description=description, graphs=graph)
				print "TOMCAT Dashboard is updated with new metrics"
			else:
				pass
else:
	print "TOMCAT dashboard is already exist"

if existing_queries != []:
	print "The metrics already created for the below lines in csv file: \n"+ str(existing_queries)