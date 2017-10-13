#!/usr/bin/env python
# +----------------------------------------------------------------------------------------+
# | Script  : This script create Metric,Query,Host,Network,Integration,and Process alerts  |
# | Notes   : Please make sure your CSV file having valid inputs                           |
# | Notes   : Please confiure the Datadog credentials in datadogKeys.py                    |
# +----------------------------------------------------------------------------------------+
import sys
import csv
import getopt
from datadogKeys import *
from itertools import islice
from datadog import initialize, api

options = {
            'api_key': datadog_api_key,
            'app_key': datadog_app_key
           }

initialize(**options)

#======================================================================

# Create a new monitor
options = {
    "notify_no_data": True,
    "no_data_timeframe": 20
}
existing_alert_queries = []

all_monitors = api.Monitor.get_all()
for monitor in all_monitors:
	existing_alert_queries.append(monitor['query'])


csvFile = csv.reader(open("alertsInputs.csv", "rb"))
for i,line in enumerate(csvFile):
	if i >=1:
		if line[13] == "yes":
			if line[11] == "metric alert":
				get=line[1].split(',')
				get_values = []
				for x in get:
					get_values.append(x)
				if len(get_values) < 3:
					if line[5] == "on average":
						query = "avg(last_"+line[6]+"):"+line[7]+":"+line[1]+"{"+line[2]+"}"+" by "+"{"+line[10]+"}"+" "+line[4]+" "+line[8]
						if query in existing_alert_queries:
							print "Alert aleady exist"
						else:
							api.Monitor.create(type="metric alert", query=query, name=client_name+"-"+line[0], message=line[3])	
					elif line[5] == "at least once":
						query = "min(last_"+line[6]+"):"+line[7]+":"+line[1]+"{"+line[2]+"}"+" by "+"{"+line[10]+"}"+" "+line[4]+" "+line[8]
						if query in existing_alert_queries:
							print "Alert aleady exist"
						else:
							api.Monitor.create(type="metric alert", query=query, name=client_name+"-"+line[0], message=line[3])	
					elif line[5] == "at all times":
						query = "max(last_"+line[6]+"):"+line[7]+":"+line[1]+"{"+line[2]+"}"+" by "+"{"+line[10]+"}"+" "+line[4]+" "+line[8]
						if query in existing_alert_queries:
							print "Alert aleady exist"
						else:
							api.Monitor.create(type="metric alert", query=query, name=client_name+"-"+line[0], message=line[3])	
					elif line[5] == "in total":
						query = "sum(last_"+line[6]+"):"+line[7]+":"+line[1]+"{"+line[2]+"}"+" by "+"{"+line[10]+"}"+" "+line[4]+" "+line[8]
						if query in existing_alert_queries:
							print "Alert aleady exist"
						else:
							api.Monitor.create(type="metric alert", query=query, name=client_name+"-"+line[0], message=line[3])	
					else:
						print "\""+line[5]+"\""+"is invalid threashold, please provide valid threshold for metric alert"
				else:
					query = "avg(last_"+line[6]+"):( "+line[7]+":"+get_values[0]+"{"+line[2]+"}"+" by "+"{"+line[10]+"}"+" - "+line[7]+":"+get_values[1]+"{"+line[2]+"}"+" by "+"{"+line[10]+"}"+" ) "+" / "+line[7]+":"+get_values[2]+"{"+line[2]+"}"+" by "+"{"+line[10]+"}"+" * "+"100 "+line[4]+" "+line[8]
					if query in existing_alert_queries:
						print "Alert aleady exist"
					else:
						api.Monitor.create(type="metric alert", query=query, name=client_name+"-"+line[0], message=line[3])
		

			elif line[11] == "query alert":
				if line[5] == "on average":
					query = "avg(last_"+line[6]+"):"+line[7]+":"+line[1]+"{"+line[2]+"}"+" by "+"{"+line[10]+"}"+" * "+"100 "+line[4]+" "+line[8]
					if query in existing_alert_queries:
						print "Alert aleady exist"
					else:
						api.Monitor.create(type="metric alert", query=query, name=client_name+"-"+line[0], message=line[3])
				elif line[5] == "at least once":
					query = "min(last_"+line[6]+"):"+line[7]+":"+line[1]+"{"+line[2]+"}"+" by "+"{"+line[10]+"}"+" * "+"100 "+line[4]+" "+line[8]
					if query in existing_alert_queries:
						print "Alert aleady exist"
					else:
						api.Monitor.create(type="metric alert", query=query, name=client_name+"-"+line[0], message=line[3])
				elif line[5] == "at all times":
					query = "max(last_"+line[6]+"):"+line[7]+":"+line[1]+"{"+line[2]+"}"+" by "+"{"+line[10]+"}"+" * "+"100 "+line[4]+" "+line[8]
					if query in existing_alert_queries:
						print "Alert aleady exist"
					else:
						api.Monitor.create(type="metric alert", query=query, name=client_name+"-"+line[0], message=line[3])
				elif line[5] == "in total":
					query = "sum(last_"+line[6]+"):"+line[7]+":"+line[1]+"{"+line[2]+"}"+" by "+"{"+line[10]+"}"+" * "+"100 "+line[4]+" "+line[8]
					if query in existing_alert_queries:
						print "Alert aleady exist"
					else:
						api.Monitor.create(type="metric alert", query=query, name=client_name+"-"+line[0], message=line[3])
				else:
					print "\""+line[5]+"\""+"is invalid threashold, please provide valid threshold for query alert"


			elif line[11] == "service check":
				if line[12] =="network":
					if line[7] == "ssl":
						if (line[1] == "All monitored SSL endpoints") and (line[2] == "monitoring:on"):
							query = "\"http.ssl_cert\".over(\"*\").by(\"host\",\"instance\",\"url\").last(3).count_by_status()"
							if query in existing_alert_queries:
								print "Alert aleady exist"
							else:
								api.Monitor.create(type="service check", query=query, name=client_name+"-"+line[0], message=line[3])
						elif (line[1] == "All monitored SSL endpoints") and (line[2] != "monitoring:on"):
							query = "\"http.ssl_cert\".over(\""+line[2]+"\").by(\"host\",\"instance\",\"url\").last(3).count_by_status()"
							if query in existing_alert_queries:
								print "Alert aleady exist"
							else:
								api.Monitor.create(type="service check", query=query, name=client_name+"-"+line[0], message=line[3])					
						elif (line[1] != "All monitored SSL endpoints") and (line[2] == "monitoring:on"):
							query = "\"http.ssl_cert\".over(\"*\",\"instance:"+line[1]+"\").by(\"host\",\"instance\",\"url\").last(3).count_by_status()"
							if query in existing_alert_queries:
								print "Alert aleady exist"
							else:
								api.Monitor.create(type="service check", query=query, name=client_name+"-"+line[0], message=line[3])
						elif (line[1] != "All monitored SSL endpoints") and (line[2] != "monitoring:on"):
							query = "\"http.ssl_cert\".over(\"application:bastionhost\",\"availability-zone:us-west-2a\",\"instance:ecosystem_preprod\").by(\"host\",\"instance\",\"url\").last(3).count_by_status()"
							if query in existing_alert_queries:
								print "Alert aleady exist"
							else:
								api.Monitor.create(type="service check", query=query, name=client_name+"-"+line[0], message=line[3])
						else:
							print "Please provide valid inputs"

					elif line[7] == "http":
						if (line[1] == "All monitored SSL endpoints") and (line[2] == "monitoring:on"):
							query = "\"http.can_connect\".over(\"*\").by(\"host\",\"instance\",\"url\").last(3).count_by_status()"
							if query in existing_alert_queries:
								print "Alert aleady exist"
							else:
								api.Monitor.create(type="service check", query=query, name=client_name+"-"+line[0], message=line[3])
						elif (line[1] == "All monitored SSL endpoints") and (line[2] != "monitoring:on"):
							query = "\"http.can_connect\".over(\""+line[2]+"\").by(\"host\",\"instance\",\"url\").last(3).count_by_status()"
							if query in existing_alert_queries:
								print "Alert aleady exist"
							else:
								api.Monitor.create(type="service check", query=query, name=client_name+"-"+line[0], message=line[3])					
						elif (line[1] != "All monitored SSL endpoints") and (line[2] == "monitoring:on"):
							query = "\"http.can_connect\".over(\"*\",\"instance:"+line[1]+"\").by(\"host\",\"instance\",\"url\").last(3).count_by_status()"
							if query in existing_alert_queries:
								print "Alert aleady exist"
							else:
								api.Monitor.create(type="service check", query=query, name=client_name+"-"+line[0], message=line[3])
						elif (line[1] != "All monitored SSL endpoints") and (line[2] != "monitoring:on"):
							query = "\"http.can_connect\".over(\"application:bastionhost\",\"availability-zone:us-west-2a\",\"instance:ecosystem_preprod\").by(\"host\",\"instance\",\"url\").last(3).count_by_status()"
							if query in existing_alert_queries:
								print "Alert aleady exist"
							else:
								api.Monitor.create(type="service check", query=query, name=client_name+"-"+line[0], message=line[3])
						else:
							print "Please provide valid inputs"

					elif line[7] == "tcp":
						if (line[1] == "All monitored SSL endpoints") and (line[2] == "monitoring:on"):
							query = "\"tcp.can_connect\".over(\"*\").by(\"host\",\"instance\",\"url\").last(3).count_by_status()"
							if query in existing_alert_queries:
								print "Alert aleady exist"
							else:
								api.Monitor.create(type="service check", query=query, name=client_name+"-"+line[0], message=line[3])
						elif (line[1] == "All monitored SSL endpoints") and (line[2] != "monitoring:on"):
							query = "\"tcp.can_connect\".over(\""+line[2]+"\").by(\"host\",\"instance\",\"url\").last(3).count_by_status()"
							if query in existing_alert_queries:
								print "Alert aleady exist"
							else:
								api.Monitor.create(type="service check", query=query, name=client_name+"-"+line[0], message=line[3])					
						elif (line[1] != "All monitored SSL endpoints") and (line[2] == "monitoring:on"):
							query = "\"tcp.can_connect\".over(\"*\",\"instance:"+line[1]+"\").by(\"host\",\"instance\",\"url\").last(3).count_by_status()"
							if query in existing_alert_queries:
								print "Alert aleady exist"
							else:
								api.Monitor.create(type="service check", query=query, name=client_name+"-"+line[0], message=line[3])
						elif (line[1] != "All monitored SSL endpoints") and (line[2] != "monitoring:on"):
							query = "\"tcp.can_connect\".over(\""+line[2]+"\",\"instance:"+line[1]+"\").by(\"host\",\"instance\",\"url\").last(3).count_by_status()"
							if query in existing_alert_queries:
								print "Alert aleady exist"
							else:
								api.Monitor.create(type="service check", query=query, name=client_name+"-"+line[0], message=line[3])
						else:
							print "Please provide valid inputs"
					else:
						print "Please provide valid inputs for network alert"

			
				elif line[12] == "host":
					if line[2] == "All monitored Host":
						query = "\"datadog.agent.up\".over(\"*\").by(\"host\").last(2).count_by_status()"
						if query in existing_alert_queries:
							print "Alert aleady exist"
						else:
							api.Monitor.create(type="service check", query=query, name=client_name+"-"+line[0], message=line[3])
					else:
						query = "\"datadog.agent.up\".over(\""+line[2]+"\").by(\"host\").last(2).count_by_status()"
						if query in existing_alert_queries:
							print "Alert aleady exist"
						else:
							api.Monitor.create(type="service check", query=query, name=client_name+"-"+line[0], message=line[3])

			
				elif line[12] == "integration":
					if line[7] == "apache":
						if line[2] == "All monitored Host":
							query = "\"apache.can_connect\".over(\"*\").by(\"host\",\"port\").last(3).count_by_status()"
							if query in existing_alert_queries:
								print "Alert aleady exist"
							else:
								api.Monitor.create(type="service check", query=query, name=client_name+"-"+line[0], message=line[3])
						else:
							query = "\"apache.can_connect\".over(\""+line[2]+"\").by(\"host\",\"port\").last(3).count_by_status()"
							if query in existing_alert_queries:
								print "Alert aleady exist"
							else:
								api.Monitor.create(type="service check", query=query, name=client_name+"-"+line[0], message=line[3])

					elif line[7] == "tomcat":
						if line[2] == "All monitored Host":
							query = "\"tomcat.can_connect\".over(\"*\").by(\"host\",\"instance\").last(3).count_by_status()"
							if query in existing_alert_queries:
								print "Alert aleady exist"
							else:
								api.Monitor.create(type="service check", query=query, name=client_name+"-"+line[0], message=line[3])
						else:
							query = "\"tomcat.can_connect\".over(\""+line[2]+"\").by(\"host\",\"instance\").last(3).count_by_status()"
							if query in existing_alert_queries:
								print "Alert aleady exist"
							else:
								api.Monitor.create(type="service check", query=query, name=client_name+"-"+line[0], message=line[3])

					elif line[7] == "mysql":
						if line[2] == "All monitored Host":
							query = "\"mysql.can_connect\".over(\"*\").by(\"host\",\"port\").last(3).count_by_status()"
							if query in existing_alert_queries:
								print "Alert aleady exist"
							else:
								api.Monitor.create(type="service check", query=query, name=client_name+"-"+line[0], message=line[3])
						else:
							query = "\"mysql.can_connect\".over(\""+line[2]+"\").by(\"host\",\"port\").last(3).count_by_status()"
							if query in existing_alert_queries:
								print "Alert aleady exist"
							else:
								api.Monitor.create(type="service check", query=query, name=client_name+"-"+line[0], message=line[3])
					else:
						print "\""+line[7]+"\""+"is valid, please provide valid inputs for integration alert"


				elif line[12] == "process":
					if line[7] == "java":
						if line[2] == "All monitored Host":
							query = "\"process.up\".over(\"*\",\""+line[1]+"\").by(\"host\",\"process\").last(5).count_by_status()"
							if query in existing_alert_queries:
								print "Alert aleady exist"
							else:
								api.Monitor.create(type="service check", query=query, name=client_name+"-"+line[0], message=line[3])
						else:
							query = "\"process.up\".over(\""+line[2]+"\",\""+line[1]+"\").by(\"host\",\"process\").last(5).count_by_status()"
							if query in existing_alert_queries:
								print "Alert aleady exist"
							else:
								api.Monitor.create(type="service check", query=query, name=client_name+"-"+line[0], message=line[3])
					else:
						print "\""+line[7]+"\""+"is valid, please provide valid inputs for integration alert"
				else:
					print "\""+line[12]+"\""+"is valid monitoring name, please provide valid inputs for process alert"
			else:
				print "line no "+str(i)+" in csv file having invalid metric type:" + "\""+line[11]+"\""
				
			print "Alert created for the line in the csv file: "+str(i)

		else:
			pass
	else:
		pass