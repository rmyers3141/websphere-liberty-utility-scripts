# websphere-liberty-utility-scripts
A miscellaneous collection of scripts for managing and monitoring [IBM WebSphere Liberty](https://www.ibm.com/products/liberty) or [Open Liberty](https://openliberty.io/).

Hereafter just referred to as *"Liberty"*.

## jmx-explore.py script
This is a simple Jython script I have created to investigate how to gather monitoring metrics from a Liberty instance over JMX.  

### Overview
The script uses the Liberty JMX REST API connector to make JMX connections to the Liberty MBean server and extract sample monitoring metrics.  For background information, please see [Connecting to Liberty using JMX](https://www.ibm.com/docs/en/was-liberty/core?topic=SSD28V_liberty/com.ibm.websphere.wlp.doc/ae/twlp_admin_jmx.htm).

In particular, it collects and prints out JVM **Garbage Collection Time** statistics (a very important monitoring metric!).  It also checks for available **endpoints** (either HTTP/S or Messaging endpoints), and specifically, checks whether the HTTP/S endpoints on the Liberty's default virtual host are started or not.

These are just a couple of examples of monitoring metrics that can be extracted using this script, but it can be easily be adapted to get any other JMX stats (or even invoke JMX operations) on the Liberty server.


### Prerequisites
The script runs on the same machine as the Liberty server being monitored for convenience, but theoretically could be run remotely as well.  To run it on the same machine as the Liberty server you'll need:

- [x] A Liberty instance set up for remote JMX connections using the REST Connector (see [IBM documentation](https://www.ibm.com/docs/en/was-liberty/core?topic=SSD28V_liberty/com.ibm.websphere.wlp.doc/ae/twlp_admin_restconnector.htm) for further details).  This will include setting up a user with an *admin* role.

- [x] A supported version of Jython installed on the same machine as the Liberty instance.  Currently, this at least Jython 2.5.x, but check IBM documentation for any updates.

- [x] The Liberty instance must be <ins>running</ins> for the script to access its JMX MBean server.

- [x] The script execution (below) assumes the Liberty instance is running on Linux, but it can be adapted to run on other platforms as well.




### Script Execution
Before running the script, you may need to edit the following parts of the script.

Make sure you use the correct path to the Liberty instance's keystore (or external Truststore) containing it's SSL certificate, and the password for the keystore: -

```sh
JMXRESTConnector.trustStore = "/opt/ibm/wlp/usr/servers/defaultServer/resources/security/key.p12"
JMXRESTConnector.trustStorePassword = "change_it"
```
Enter the hostname of the machine hosting the Liberty instance, SSL port of the Liberty instance, admin username, and admin password: -

```sh
connector.connect("my-machine.my-domain.test",9443,"admin","change_it")
```

Save any necessary changes to the script, and then set the following environment variables at the command line (Linux):

```sh
export CLASSPATH=~/restConnector.jar:/opt/ibm/wlp/lib/com.ibm.ws.kernel.service_1.3.70.jar
```
Adjust the paths given above according to the location of the `restConnector.jar` file and Liberty install path.

Then, place the `jython` binary on your `$PATH`, change to the directory where the script exists, and execute the script as follows:

```sh
jython ./jmx-explore.py
```
The script will print out the metrics before disconnecting.


### TO-DO:
This script is very basic but can be developed for more extensive JXM monitoring (or JMX operations) on Liberty instances if desired.




