# Does PKS do Least Cost Routing (LCR)?

PKS cannot route calls based on the communication costs of SIP providers. This functionality, which is present in PyFreeBilling, has been removed, as it brings greater complexity, both in the scripting part and therefore in debugging, but also in terms of administration.

If this functionality is needed, other solutions will be more appropriate.

Nevertheless, a [discussion](https://github.com/mwolff44/pyfreebilling/discussions/186) exists on the forum to integrate [CGRateS](http://www.cgrates.org/).
