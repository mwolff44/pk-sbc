# Connecting an IPBX to more than one operator

For administrations or sites hosting several companies, it is common to use a multi-tenant IPBX, i.e. hosting separate entities that are hermetically sealed from each other. Apart from a hack, it is impossible to connect this multi-tenant IPBX to a telecoms operator via a single trunk. P-KISS-SBC makes this possible:

SIP PROVIDER ==== P-KISS-SBC ==tenant 1== IPBX tenant 1
                             ==Holder 2== IPBX holding 2
