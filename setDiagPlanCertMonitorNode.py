##############################################################
# 
# This is a sample diagnostic plan for Certificate Expiration Monitor on a federated node. 
# Please update the server name.
# 
# The output : {was_install_dir}/profiles/AppSvr01/traceDump_xxxx.log (example)
# If the line that contains RASTraceMBean is commented out, the output will be written to trace.log 
# 
##############################################################
# Query to find the TraceService MBean
RASTraceMBean = AdminControl.queryNames('WebSphere:type=TraceService,process=server1,*')

# Set the runtime trace output to Memory Buffer
print "\nSetting the Runtime Trace Output to Memory Buffer"
AdminControl.invoke(RASTraceMBean, "setTraceOutputToRingBuffer", [8, "Basic"])

# Query to find the DiagnosticPlan MBean and create the objectName
#diagPlanMBean = AdminControl.queryNames('WebSphere:type=DiagPlanManager,process=dmgr,*')
diagPlanMBean = AdminControl.queryNames('WebSphere:type=DiagPlanManager,process=server1,*')
objName = AdminControl.makeObjectName(diagPlanMBean)

# Same instruction x 3 times.  This is to capture all possible data in case alarm for the cert monitor fires multiple times within short period of time. 
# Pass the diagnostic plan string as a parameter

parms =["MATCH=TRACE:SECJ0446I*,SET_TRACESPEC=*=info:com.ibm.ws.security.core.distSecurityComponentImpl=all:SSL=all:com.ibm.ws.management.repository.FileDocument=all: com.ibm.ws.management.repository.FileRepository=all: com.ibm.ws.management.connector.soap.SOAPServer=all:com.ibm.ws.sm.workspace.*=all,MATCH=TRACE:SECJ0056I*,DELAY=300,DUMPBUFFER,RESTORE_TRACESPEC,MATCH=TRACE:SECJ0446I*,SET_TRACESPEC=*=info:com.ibm.ws.security.core.distSecurityComponentImpl=all:SSL=all:com.ibm.ws.management.repository.FileDocument=all: com.ibm.ws.management.repository.FileRepository=all: com.ibm.ws.management.connector.soap.SOAPServer=all:com.ibm.ws.sm.workspace.*=all,MATCH=TRACE:SECJ0056I*,DELAY=300,DUMPBUFFER,RESTORE_TRACESPEC,MATCH=TRACE:SECJ0446I*,SET_TRACESPEC=*=info:com.ibm.ws.security.core.distSecurityComponentImpl=all:SSL=all:com.ibm.ws.management.repository.FileDocument=all: com.ibm.ws.management.repository.FileRepository=all: com.ibm.ws.management.connector.soap.SOAPServer=all:com.ibm.ws.sm.workspace.*=all,MATCH=TRACE:SECJ0056I*,DELAY=300,DUMPBUFFER,RESTORE_TRACESPEC"]

# Run the setDiagPlan method in the MBean with the diagnostic plan string.
AdminControl.invoke_jmx(objName, 'setDiagPlan', parms, ["java.lang.String"])

print "\nCertificate Monitor diagplan is set"

###############################################################
# Federated nodes do not receive alarms, but syncNode changes the configuration. 
#
# When message matches SECJ0446I (= SSL configuration change is detected)
# Trace starts
# Once message matches SECJ0056I (= SSL initialization starts)
# Delay 300 sec = 5 mins to let SSL update takes place
# Put the tracing back to default 
# Dump out the buffer to {was_install_dir}/profiles/AppSvr01/traceDump_xxxx.log (example)
#
# MATCH=TRACE:SECJ0446I*,
# SET_TRACESPEC=*=info:com.ibm.ws.security.core.distSecurityComponentImpl=all:SSL=all:com.ibm.ws.management.repository.FileDocument=all: com.ibm.ws.management.repository.FileRepository=all: com.ibm.ws.management.connector.soap.SOAPServer=all,
# MATCH=TRACE:SECJ0056I*,
# DELAY=300,
# DUMPBUFFER,
# RESTORE_TRACESPEC
#
################################################################
