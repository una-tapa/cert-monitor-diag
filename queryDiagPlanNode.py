# Query to find the DiagnosticPlan MBean and create the objectName
diagPlanMBean = AdminControl.queryNames('WebSphere:type=DiagPlanManager,process=server1,*')
diagPlanObjName = AdminControl.makeObjectName(diagPlanMBean)

# Run the getDiagPlan method in the Mbean
ret = AdminControl.invoke_jmx(diagPlanObjName, 'getDiagPlan',[],[])

# Display the results on the console
print ret
