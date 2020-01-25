# Variables lists and usage

## Accounting

src_user : $fU
src_domain : $fd
src_ip : $ci
dst_ouser : $tU
dst_user : $rU
dst_domain : $rd


## Customer

### $avp
src_accountcode
dst_accountcode
src_context

## Caller and Callee ID

### $avp
src_clir
src_callerid
callednumber : initialised with $rU
assertedid : PAI user part : init with $fU
uacreplacefromdisplay
uacreplacefromuri
uacfromdisplay
uacfromuri
uacreplacetodisplay
uacreplacetouri
uactodisplay
uactouri


## Call limit

### $var
channelsinbound
channelsoutbound

### $avp
src_maxchannels
dst_maxchannels

define max channels available for an endpoint. Positive integer. If 0, illimited.

## Others

### $var
contact : init $ct


## usr_preferences attribute list

callerids
callerid
acl
barred_prefix
rewriterurito

And all src_$avp and dst_$avp
src_clir par ex
