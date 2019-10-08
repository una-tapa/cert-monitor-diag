# Traditional WebSphere Certificate Expiration Monitor Diagnostic Plan
- This repository contains sample diagnostic plans. 
- The files are not supported. 
- They are to show how diag plan can be created for Certificate Expiration Monitor issues. 

## Sample diagnostic plans for Dmgr and Standalone AppServer 
The diagnostic plan will monitor the messages in SystemOut.log.  Once the scheduled alarm for the certificate monitor is fired, the trace is turned on. After certificate monitor ended, wait for 5 mins, turn off the trace and dump out the data.  
- setDiagPlanCertMonitorDmgr.py : Enables diag plan for certificate expiration monitor 
- queryDiagPlanDmgr.py          : Queries diag plan status.
- clearDiagPlanDmgr.py          : Clears diag plan 
## Sample diagnostic plans for a faderated nodes
The diagnostic plan will monitor the messages in SystemOut.log.  Once the security.xml and keystores are synchronized from the dmgr and the certificate renewal is detected, the trace is turned on. After SSL initialization is started, wait for 5 mins, turn off the trace and dump out the data.  
- setDiagPlanCertMonitorNode.py : Enables diag plan for certificate expiration monitor 
- queryDiagPlanNode.py          : Queries diag plan status.
- clearDiagPlanNode.py          : Clears diag plan 
