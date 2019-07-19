#############################################################
# 
# This is for DeploymentManager. For AppSrv, change dmgr -> server1 in the queryNames below. 
# 
# The output 
# If the line that contains "RASTraceMBean" is removed, the trace will be written out to the usual trace. 
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


# This parameter contains the same instruction x 3 times, in case the certificate expiration monitor is kicked off unexpectedly multiple times.  
# From MATCH=TRACE:CWPKI0059I to DUMPBUFFER is one cycle. 

parms =["MATCH=TRACE:CWPKI0059I*,SET_TRACESPEC=*=info:com.ibm.ws.security.core.distSecurityComponentImpl=all:SSL=all:com.ibm.ws.management.repository.FileDocument=all:com.ibm.ws.management.repository.FileRepository=all:com.ibm.ws.management.connector.soap.SOAPServer=all,MATCH=TRACE:CWPKI0060I*,DELAY=300,SET_TRACESPEC=*=info,DUMPBUFFER,MATCH=TRACE:CWPKI0059I*,SET_TRACESPEC=*=info:com.ibm.ws.security.core.distSecurityComponentImpl=all:SSL=all:com.ibm.ws.management.repository.FileDocument=all:com.ibm.ws.management.repository.FileRepository=all:com.ibm.ws.management.connector.soap.SOAPServer=all,MATCH=TRACE:CWPKI0060I*,DELAY=300,SET_TRACESPEC=*=info,DUMPBUFFER,MATCH=TRACE:CWPKI0059I*,SET_TRACESPEC=*=info:com.ibm.ws.security.core.distSecurityComponentImpl=all:SSL=all:com.ibm.ws.management.repository.FileDocument=all:com.ibm.ws.management.repository.FileRepository=all:com.ibm.ws.management.connector.soap.SOAPServer=all,MATCH=TRACE:CWPKI0060I*,DELAY=300,SET_TRACESPEC=*=info,DUMPBUFFER"]

# Run the setDiagPlan method in the MBean with the diagnostic plan string.
AdminControl.invoke_jmx(objName, 'setDiagPlan', parms, ["java.lang.String"])

print "\nCertificate Monitor diagplan is set"

###############################################################
# Following is the break down of actions. 

# parms =["
# MATCH=TRACE:CWPKI0059I*,
# SET_TRACESPEC=*=info:com.ibm.ws.security.core.distSecurityComponentImpl=all:SSL=all:com.ibm.ws.management.repository.FileDocument=all:com.ibm.ws.management.repository.FileRepository=all:com.ibm.ws.management.connector.soap.SOAPServer=al#l,
# MATCH=TRACE:CWPKI0060I*,
# DELAY=300,
# SET_TRACESPEC=*=info,
# DUMPBUFFER,
# ...
# "]
#

# Trace that is currently in the diag plan  
# com.ibm.ws.security.core.distSecurityComponentImpl=all:SSL=all:com.ibm.ws.management.repository.FileDocument=all:com.ibm.ws.management.repository.FileRepository=all:com.ibm.ws.management.connector.soap.SOAPServer=all

# Reduced trace in the SSL=all
# com.ibm.ws.security.core.distSecurityComponentImpl=all: com.ibm.ws.ssl.commands.WSCertExpMonitor.*=all: com.ibm.ws.security.config.SSLConfigCompare=all: com.ibm.ws.management.repository.FileDocument=all: com.ibm.ws.management.repository.FileRepository=all: com.ibm.ws.management.connector.soap.SOAPServer=all: com.ibm.ws.ssl.config.SSLConfigManager=all: com.ibm.websphere.ssl.JSSEHelper=all
# *=info:com.ibm.ws.crypto.config.WSScheduler=all

# Reduced startup trace. 
# com.ibm.ws.crypto.config.WSScheduler=all
