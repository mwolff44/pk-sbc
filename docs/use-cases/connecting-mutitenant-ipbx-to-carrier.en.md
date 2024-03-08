<!---
# P-KISS-SBC documentation © 2007-2024 by Mathias WOLFF 
# is licensed under Attribution-NonCommercial-ShareAlike 4.0 International (see https://creativecommons.org/licenses/by-nc-sa/4.0/)
# SPDX-License-Identifier: CC-BY-NC-SA-4.0
--->

# Connecting an IPBX to more than one operator

For administrations or sites hosting several companies, it is common to use a multi-tenant IPBX, i.e. hosting separate entities that are hermetically sealed from each other. Apart from a hack, it is impossible to connect this multi-tenant IPBX to a telecoms operator via a single trunk. P-KISS-SBC makes this possible:

SIP PROVIDER ==== P-KISS-SBC ==tenant 1== IPBX tenant 1
                             ==Holder 2== IPBX holding 2
