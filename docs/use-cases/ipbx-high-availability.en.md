<!---
# P-KISS-SBC documentation © 2007-2024 by Mathias WOLFF 
# is licensed under Attribution-NonCommercial-ShareAlike 4.0 International (see https://creativecommons.org/licenses/by-nc-sa/4.0/)
# SPDX-License-Identifier: CC-BY-NC-SA-4.0
--->

# High availability of an IPBX with 2 or more instances

In addition to fail over, P-KISS-SBC also supports high availability where the IPBX operates with 2 or more simultaneously active instances. In this case, P-KISS-SBC routes requests equally between the instances: 

SIP PROVIDER ==== P-KISS-SBC ==50%== IPBX instance 1
                             ==50%== IPBX instance 2

