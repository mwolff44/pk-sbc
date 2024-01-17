# Securing a telephony system

This first use case is the simplest: use P-KISS-SBC between the outside world and the IPBX to protect it. The diagram will be as follows: 

SIP Provider ==== P-KISS-SBC ===== IPBX

An SBC has more advanced and powerful security features than an IPBX, which must be considered as an application server. An IPBX exposes a large number of services, making its attack surface large. It is also not very robust to Denial of Service attacks. P-KISS-SBC by design offers a very low attack surface, detects and blocks attack attempts before they reach the IPBX and is very resilient due to its ability to support a large number of requests.

TODO: detail security features and implementation
