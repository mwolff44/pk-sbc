# Use cases

## Securing a telephony system

This first use case is the simplest: use P-KISS-SBC between the outside world and the IPBX to protect it. The diagram will be as follows: 

SIP Provider ==== P-KISS-SBC ===== IPBX

An SBC has more advanced and powerful security features than an IPBX, which must be considered as an application server. An IPBX exposes a large number of services, making its attack surface large. It is also not very robust to Denial of Service attacks. P-KISS-SBC by design offers a very low attack surface, detects and blocks attack attempts before they reach the IPBX and is very resilient due to its ability to support a large number of requests.

TODO: detail security features and implementation

## Fail over from a primary to a secondary IPBX

Another simple use case to implement with P-KISS-SBC is IPBX high availability. 2 scenarios are possible. Firstly, failover enabling requests to be sent from the main IPBX to the secondary IPBX without any manual action. The telecoms operator(s) see no change and have no knowledge of the internal telephone infrastructure. 

Nominal operation: 

SIP PROVIDER ==== P-KISS-SBC ==== Main IPBX
                             ---- Secondary IPBX

In the event of loss of the main IPBX, flows are redirected to the secondary IPBX.

SIP PROVIDER ==== P-KISS-SBC ---- Main IPBX
                             ==== Secondary IPBX

The return to nominal operation is automatic as soon as P-KISS-SBC detects that the main IPBX is back in working order.

## High availability of an IPBX with 2 or more instances

In addition to fail over, P-KISS-SBC also supports high availability where the IPBX operates with 2 or more simultaneously active instances. In this case, P-KISS-SBC routes requests equally between the instances: 

SIP PROVIDER ==== P-KISS-SBC ==50%== IPBX instance 1
                             ==50%== IPBX instance 2


## Geographical distribution of IPBX with centralised telecom operator connection

For reasons of flow optimisation, availability or load distribution, IPBX instances can be deployed on different sites. P-KISS-SBC enables a single connection to an operator and the calls to be routed simply to the desired instance: 

Call to site 1 : 

SIP PROVIDER ==== P-KISS-SBC ==== IPBX 1
                             ---- IPBX 2

Call to site 2 : 

SIP PROVIDER ==== P-KISS-SBC ---- IPBX 1
                             ==== IPBX 2

## Connecting a multi-tenant IPBX to a telecom operator

For administrations or sites hosting several companies, it is common to use a multi-tenant IPBX, i.e. hosting separate entities that are hermetically sealed from each other. Apart from a hack, it is impossible to connect this multi-tenant IPBX to a telecoms operator via a single trunk. P-KISS-SBC makes this possible:

SIP PROVIDER ==== P-KISS-SBC ==tenant 1== IPBX tenant 1
                             ==Holder 2== IPBX holding 2


## Connecting an IPBX to more than one operator

In order to save money on subscriptions and telephone communications, it may be advisable to use different operators depending on the destinations or numbers required, particularly for international calls. P-KISS-SBC makes it possible to connect several operators to an IPBX and to route incoming calls to the IPBX, whatever the original operator, and to route outgoing calls to the desired operator. Although it is possible to connect several operators directly to an IPBX, it is complex to route calls to the desired operator while integrating a failover function. P-KISS-SBC incorporates a function that allows you to attempt to route the call to a preferred operator and, if this fails, to attempt to terminate the call on a second operator.

SIP PROVIDER 1
              ===== P-KISS-SBC ==== IPBX
SIP PROVIDER 2                            