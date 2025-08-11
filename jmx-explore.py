###################################################
# SCRIPT TO EXPLORE MONITORING LIBERTY USING JMX
# Uses the Liberty RestConnector API and Java JMX
###################################################

''' # NOTE - SHELL COMMANDS YOU NEED TO RUN THIS SCRIPT:
export CLASSPATH=<PATH>/restConnector.jar:/opt/ibm/wlp/lib/com.ibm.ws.kernel.service_1.3.70.jar
${PATH_TO_JYTHON_BINARY} ./jmx-explore.py

Where
<PATH> - is the path to restConnector.jar
${PATH_TO_JYTHON_BINARY} - is the path to the Jython executable.

'''

###########  BEGIN REQUIRED IMPORTS ###############

# Import required packages for JMX etc:
import javax.management.JMX as JMX
import com.ibm.websphere.kernel.server.ServerEndpointControlMBean as ServerEndpointControlMBean

#The restConnector.jar file needs to be on the CLASSPATH:
from restConnector import JMXRESTConnector

#Allow one to create MBean ObjectName instance from string input
from javax.management import ObjectName

########### END REQUIRED IMPORTS ###############


#Set up the trust store for secure communication between client and server:
JMXRESTConnector.trustStore = "/opt/ibm/wlp/usr/servers/defaultServer/resources/security/key.p12"
JMXRESTConnector.trustStorePassword = "change_it"

#Establish connectivity to the server:
connector = JMXRESTConnector()
connector.connect("my-machine.my-domain.test",9443,"admin","change_it")

# get an MBean server connection:
mconnection = connector.getMBeanServerConnection()


#Identify the MBeans to be invoked:
jvmStats = ObjectName("WebSphere:type=JvmStats")
endpointControl = ObjectName("WebSphere:feature=kernel,name=ServerEndpointControl")


#Invoke the MBean operations:

# Get an attribute value (e.g Garbage Collection Time) and convert to string in order to print it:
gctime = mconnection.getAttribute(jvmStats, "GcTime")
print "--------------------------------------"
print "Garbage Collection Time: " +  str(gctime)
print "--------------------------------------"

# THIS INVOKE OPERATION WORKS:
endpoints = mconnection.invoke(endpointControl, "listEndpoints", None, None)
for ep  in endpoints :
  print(ep)
print "--------------------------------------"


# THIS DOES NOT WORK:
# Invoke an operation to determine if the Http endpoint is paused:
'''ep = "defaultHttpEndpoint"
status = mconnection.invoke(endpointControl, "IsPaused", [ep], ["java.lang.string"])
print status'''

# THIS WORKS INSTEAD - MBEAN PROXY (recommended as simpler than the invoke operation above):
mbean = JMX.newMBeanProxy(mconnection, endpointControl, ServerEndpointControlMBean)
status = mbean.isPaused("defaultHttpEndpoint")
if status:
  print "defaultHttpEndpoint is: PAUSED."
else:
  print "defaultHttpEndpoint is: RESUMED."
print "--------------------------------------"




#disconnect from the server:
connector.disconnect()

