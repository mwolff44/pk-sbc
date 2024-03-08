<!---
# P-KISS-SBC documentation © 2007-2024 by Mathias WOLFF 
# is licensed under Attribution-NonCommercial-ShareAlike 4.0 International (see https://creativecommons.org/licenses/by-nc-sa/4.0/)
# SPDX-License-Identifier: CC-BY-NC-SA-4.0
--->

# Does PKS do Least Cost Routing (LCR)?

PKS cannot route calls based on the communication costs of SIP providers. This functionality, which is present in PyFreeBilling, has been removed, as it brings greater complexity, both in the scripting part and therefore in debugging, but also in terms of administration.

If this functionality is needed, other solutions will be more appropriate.

Nevertheless, a [discussion](https://github.com/mwolff44/pyfreebilling/discussions/186) exists on the forum to integrate [CGRateS](http://www.cgrates.org/).
