Datadog Dashboard creation script that fetch the inputs from CSV file


Configure the script to create the dashboard

Requirements

	1.This script needs pre-installed datadog python library files.
	
	  Installation : pip install datadog

	2.Configure the Datadog API key, Application key and Customer name in datadogKeys.py file
	
	3.Provide valid inputs in the dashboardinput.csv according to which dashboard you are going to create                        
	  
		column explains:
	  
			you have 14 cloumns are present in this csv file. 
	  
			1. Provide a proper "dashboard title" and "description" for the dashboard in column1 and column2 and these two columns should be same for the same "name of dashboard"(column8)
	
			2. Provide proper entries in column3, column4 and column6 according to the metrics in that dashboard.
			
					Refer the dashboardinput.csv when you are going to create alert.
					
	4.Execute the dashboardscript.py to create alert.
	
		Execution : python dashboardscript.py

Ref Doc: https://reancloud.atlassian.net/wiki/spaces/RE/pages/155920887/Datadog+Dashboard+Creation+Using+Python+Script
			