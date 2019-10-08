#############################################################
# 
# This is a sample diagnostic plan for Certificate Expiration Monitor on a DeploymentManager. OR standalone server (Please change the server name) 
# 
# The output : {was_install_dir}/profiles/Dmgr01/traceDump_xxxx.log
# If the line that contains "RASTraceMBean" is commented out, the output will be written out to the usual trace.log
# 
##############################################################
# Query to find the TraceService MBean
RASTraceMBean = AdminControl.queryNames('WebSphere:type=TraceService,process=dmgr,*')

# Set the runtime trace output to Memory Buffer
print "\nSetting the Runtime Trace Output to Memory Buffer"
AdminControl.invoke(RASTraceMBean, "setTraceOutputToRingBuffer", [8, "Basic"])

# Query to find the DiagnosticPlan MBean and create the objectName
diagPlanMBean = AdminControl.queryNames('WebSphere:type=DiagPlanManager,process=dmgr,*')
objName = AdminControl.makeObjectName(diagPlanMBean)


# Same instruction x 3 times. This is to capture all possible data in case alarm for the cert monitor fires multiple times within short period of time. 
# From MATCH=TRACE:CWPKI0059I to DUMPBUFFER is one cycle. 

parms =["MATCH=TRACE:CWPKI0059I*,SET_TRACESPEC=*=info:com.ibm.ws.security.core.distSecurityComponentImpl=all:SSL=all:com.ibm.ws.management.repository.FileDocument=all:com.ibm.ws.management.repository.FileRepository=all:com.ibm.ws.management.connector.soap.SOAPServer=all,MATCH=TRACE:CWPKI0060I*,DELAY=300,SET_TRACESPEC=*=info,DUMPBUFFER,MATCH=TRACE:CWPKI0059I*,SET_TRACESPEC=*=info:com.ibm.ws.security.core.distSecurityComponentImpl=all:SSL=all:com.ibm.ws.management.repository.FileDocument=all:com.ibm.ws.management.repository.FileRepository=all:com.ibm.ws.management.connector.soap.SOAPServer=all,MATCH=TRACE:CWPKI0060I*,DELAY=300,SET_TRACESPEC=*=info,DUMPBUFFER,MATCH=TRACE:CWPKI0059I*,SET_TRACESPEC=*=info:com.ibm.ws.security.core.distSecurityComponentImpl=all:SSL=all:com.ibm.ws.management.repository.FileDocument=all:com.ibm.ws.management.repository.FileRepository=all:com.ibm.ws.management.connector.soap.SOAPServer=all,MATCH=TRACE:CWPKI0060I*,DELAY=300,SET_TRACESPEC=*=info,DUMPBUFFER"]

# Run the setDiagPlan method in the MBean with the diagnostic plan string.
AdminControl.invoke_jmx(objName, 'setDiagPlan', parms, ["java.lang.String"])

print "\nCertificate Monitor diagplan is set"


#####  One set of instruction ###############################
# When message matches CWPKI0059I  (= When the scheduler alarm fires to start cert expiration monitor) 
# Trace starts
# once message matches CWPKI0060I  (= The cert monitor ended and all the processing ends)  
# Depaly 300 sec = 5 mins to let SSL update takes place. 
# Put the tracing back to default (*=info)
# Dump out the buffer to ({was_install_dir}/profiles/Dmgr01/traceDump_xxxx.log)
#
# parms =["
# MATCH=TRACE:CWPKI0059I*,
# SET_TRACESPEC=*=info:com.ibm.ws.security.core.distSecurityComponentImpl=all:SSL=all:com.ibm.ws.management.repository.FileDocument=all:com.ibm.ws.management.repository.FileRepository=all:com.ibm.ws.management.connector.soap.SOAPServer=# all
# MATCH=TRACE:CWPKI0060I*,
# DELAY=300,
# SET_TRACESPEC=*=info,
# DUMPBUFFER,
# ...
# "]
#############################################################

