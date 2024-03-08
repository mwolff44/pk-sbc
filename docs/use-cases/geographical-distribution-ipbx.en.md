<!---
# P-KISS-SBC documentation © 2007-2024 by Mathias WOLFF 
# is licensed under Attribution-NonCommercial-ShareAlike 4.0 International (see https://creativecommons.org/licenses/by-nc-sa/4.0/)
# SPDX-License-Identifier: CC-BY-NC-SA-4.0
--->

# Geographical distribution of IPBX with centralised telecom operator connection

For reasons of flow optimisation, availability or load distribution, IPBX instances can be deployed on different sites. P-KISS-SBC enables a single connection to an operator and the calls to be routed simply to the desired instance: 

Call to site 1 : 

SIP PROVIDER ==== P-KISS-SBC ==== IPBX 1
                             ---- IPBX 2

Call to site 2 : 

SIP PROVIDER ==== P-KISS-SBC ---- IPBX 1
                             ==== IPBX 2
