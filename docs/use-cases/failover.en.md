<!---
# P-KISS-SBC documentation © 2007-2024 by Mathias WOLFF 
# is licensed under Attribution-NonCommercial-ShareAlike 4.0 International (see https://creativecommons.org/licenses/by-nc-sa/4.0/)
# SPDX-License-Identifier: CC-BY-NC-SA-4.0
--->

# Fail over from a primary to a secondary IPBX

Another simple use case to implement with P-KISS-SBC is IPBX high availability. 2 scenarios are possible. Firstly, failover enabling requests to be sent from the main IPBX to the secondary IPBX without any manual action. The telecoms operator(s) see no change and have no knowledge of the internal telephone infrastructure. 

Nominal operation: 

SIP PROVIDER ==== P-KISS-SBC ==== Main IPBX
                             ---- Secondary IPBX

In the event of loss of the main IPBX, flows are redirected to the secondary IPBX.

SIP PROVIDER ==== P-KISS-SBC ---- Main IPBX
                             ==== Secondary IPBX

The return to nominal operation is automatic as soon as P-KISS-SBC detects that the main IPBX is back in working order.
