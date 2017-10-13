Datadog monitor alerts creation script that fetch the inputs from CSV file


Configure the script to create the alerts

Requirements

	1.This script needs pre-installed datadog python library files.
	
	  Installation : pip install datadog

	2.Configure the Datadog API key, Application key and Customer name in datadogKeys.py file
	
	3.Provide valid inputs in the alertsInputs.csv according to which alerts you are going to create                        
	  
		column explains:
	  
			you have 14 cloumns are present in this csv file. 
	  
			1. column1 and column4 doesn't affect your alert creation even provide a proper name and message for to the alert
		
			2. All other columns are varies according to the monitor name and alerts type.
			
					Refer the alertsInputs.csv when you are going to create alert.
					
	4.Execute the alertsCreationScript.py to create alert.
	
		Execution : python alertsCreationScript.py

Ref Doc: https://reancloud.atlassian.net/wiki/spaces/RE/pages/155931442/Datadog+Alerts+Creation+Using+Python+Script