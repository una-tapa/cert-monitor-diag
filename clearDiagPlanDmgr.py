# Query to find the DiagnosticPlan MBean and create the objectName
diagPlanMBean = AdminControl.queryNames('WebSphere:type=DiagPlanManager,process=dmgr,*')
diagPlanObjName = AdminControl.makeObjectName(diagPlanMBean)

# Run the getDiagPlan method in the Mbean
ret = AdminControl.invoke_jmx(diagPlanObjName, 'clearDiagPlan',[],[])

# Display the results on the console
print ret

ret = AdminControl.invoke_jmx(diagPlanObjName, 'getDiagPlan',[],[])

print ret
