Mark packets TOS in freeswitch

iptables -t mangle -A OUTPUT -p udp -m udp --sport 16384:32768 -j DSCP --set-dscp-class ef
iptables -t mangle -A OUTPUT -p udp --sport 5060 -j DSCP --set-dscp-class af31
