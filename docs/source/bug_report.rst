
	

From the log it is obvious that you have successfully compiled & installed SCTP module, however it could NOT be initialized.

Note that is error could must often than not be as a result of other errors in your cfg file.

Few tips:

    Can you run kamailio -c and to be sure there is NO error in your cfg.
    Found error? use this command to monitor what the exact issue is. Run from a different terminal tail -fn200 /var/log/syslog
    On the second terminal try restarting you Kamalio server sudo service kamalio restart
    Revisit terminal 1 and look out for the first line with CRITICAL output like the one below CRITICAL: <core> [core/cfg.y:3413]: yyerror_at(): parse error in config file /usr/local/etc/kamailio/kamailio.cfg, line 366, column 41: syntax error
    Line 366 mostly is the issue so visit that file at that line (366) to fix the proble
    sudo nano +366 /usr/local/etc/kamailio/kamailio.cfg

Let me know if it helps
