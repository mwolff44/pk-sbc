#!/usr/bin/perl -w

# PyFreeBilling


use strict;
use DBI();
use File::Copy;
use Text::CSV_XS;
use POSIX;
use Socket;
use Sys::Hostname;

# set variables
my $host = hostname();
#my $addr = inet_ntoa(scalar(gethostbyname($name)) || 'localhost');
my $addr = '';
#my $pg_host = $ARGV[1]; 
#my $pg_db = $ARGV[2]; 
#my $pg_table = $ARGV[3]; 
#my $pg_user = $ARGV[4]; 
#my $pg_pwd = $ARGV[5];
my $csv = Text::CSV_XS->new({ quote_char => '"', always_quote => 1 }) or die "Cannot use CSV: ".Text::CSV->error_diag ();

#my $pg_host = localhost; 
#my $pg_db = pyfreebilling1;
my $pg_table = "cdr";
my $pg_user = "pyfreebilling";
my $pg_pwd = "password";

# this commands HUPS fs, she creates new cdr.csv files, so we can load the old ones up
my $command  = ("/usr/local/freeswitch/bin/fs_cli -x 'cdr_csv rotate'");
system($command) == 0 or die "$0: system cdr_csv rotate failed: $?";

# Connect to database 
#print "Connecting to database...\n\n"; 

my $dsn="DBI:Pg:dbname=pyfreebilling1;host=localhost;port=5432";
my $dbh=DBI->connect($dsn,$pg_user,$pg_pwd)or die "$0: Couldn't connect to database: " . DBI->errstr;

# Copy Master.cv file
my $mode = 0777;
# this is the standard location of the cdr-csv
my @LS  = `ls -1t /tmp/cdr-csv/Master.csv.*`;
#my @LS  = `ls -1t /usr/local/freeswitch/log/cdr-csv/Master.csv.*`;
foreach my $line (@LS) {
    chop($line);
    chmod $mode, $line;

#	print "Successfully connected to $dsn\n";
	open cdr_log, "< $line" or die "Cannot open cdr_log_file\n";
	while (<cdr_log>) {
            if ($csv->parse($_)) { 
		my (@fields) = $csv->fields(); 
                if (!$fields[7]) {
                    $fields[7] = "NULL";
                }
                else
                {
                $fields[7] = "'".$fields[7]."'"
                }
                if (!$fields[14]) {
                    $fields[14] = "NULL";
                }
                else
                {
                $fields[14] = "'".$fields[14]."'"
                }
                if (!$fields[21]) {
                    $fields[21] = "NULL";
                }
                else
                {
                $fields[21] = "'".$fields[21]."'"
                }
                if (!$fields[22]) {
                    $fields[22] = "NULL";
                }
                else
                {
                $fields[22] = "'".$fields[22]."'"
                }
                if (!$fields[23]) {
                    $fields[23] = "NULL";
                }
                else
                {
                $fields[23] = "'".$fields[23]."'"
                }
# duration, total sell and total cost calculation
# effective duration
                my $effectiveduration = 0;
                my $billsec = 0;
                my $totalcost = 0;
                my $totalsell = 0;
#                print " effectiv_duration : $fields[31] \n\n";
                if (!$fields[31]){
                    $effectiveduration = 0;
                }
                else
                {
                    $effectiveduration = ceil($fields[31]/ 1000.0);
                }
#                print " effective_duration : $effectiveduration\n\n";
# billed duration
#                print " block_min_duration : $fields[20] \n\n";
                if ($effectiveduration != 0 and $fields[20] ){
                    if ($effectiveduration < $fields[20]){
                        $billsec = $fields[20];
                    }
                    else
                    {
                        $billsec = ceil($effectiveduration / $fields[20]) * $fields[20];
                    }
                }
                else
                {
                    $billsec = $effectiveduration;
                }
#                print " billsec : $billsec \n\n";
# total sell 18 -15
#                print " sell rate : $fields[18] \n\n";
#                print " init block rate : $fields[19] \n\n";
                if ($fields[18] and $fields[18] != 0){
                    $totalsell = sprintf("%.6f", ($billsec * $fields[18] / 60.0));
                }
                else
                {
                    $totalsell = sprintf("%.6f", 0);
                }
                if ($fields[19] and $billsec != 0){
                    $totalsell = sprintf("%.6f", ($totalsell + $fields[19]));
                }
#                print " total_sell : $totalsell \n\n";
# total cost
#                print " cost_rate : $fields[15] \n\n";
                if ($fields[15]){
                    $totalcost = sprintf("%.6f", ($billsec * $fields[15] / 60.0));
                }
                else
                {
                    $totalcost = sprintf("%.6f", 0);
                }
#                print " total_cost : $totalcost \n\n";

		my $insert_str = "insert into $pg_table (customer_id, customer_ip, uuid, caller_id_number, destination_number, chan_name, start_stamp, answered_stamp, end_stamp, duration, read_codec, write_codec, hangup_cause, hangup_cause_q850, gateway_id, cost_rate, prefix, country, rate, init_block, block_min_duration, lcr_carrier_id_id, ratecard_id_id, lcr_group_id_id, sip_user_agent, sip_rtp_rxstat, sip_rtp_txstat, bleg_uuid, switchname, switch_ipv4, hangup_disposition, effectiv_duration, sip_hangup_cause, effective_duration, billsec, total_sell, total_cost, sell_destination, cost_destination) values ( \'".$fields[0]."\', \'".$fields[1]."\', \'".$fields[2]."\', \'".$fields[3]."\', \'".$fields[4]."\', \'".$fields[5]."\', \'".$fields[6]."\', ".$fields[7].", \'".$fields[8]."\', \'".$fields[9]."\', \'".$fields[10]."\', \'".$fields[11]."\', \'".$fields[12]."\', \'".$fields[13]."\', ".$fields[14].", \'".$fields[15]."\', \'".$fields[16]."\', \'".$fields[17]."\', \'".$fields[18]."\', \'".$fields[19]."\', \'".$fields[20]."\', ".$fields[21].", ".$fields[22].", ".$fields[23].", \'".$fields[24]."\', \'".$fields[25]."\', \'".$fields[26]."\', \'".$fields[27]."\', \'".$host."\', \'".$addr."\', \'".$fields[30]."\', \'".$fields[31]."\', \'".$fields[32]."\', \'".$effectiveduration."\', \'".$billsec."\', \'".$totalsell."\', \'".$totalcost."\', \'".$fields[33]."\', \'".$fields[34]."\');"; 
#		print $insert_str."\n";
		my $sth = $dbh->prepare($insert_str); 
		$sth->execute(); 
		$sth->finish(); 
	    } else {
	        my $err = $csv->error_input;
#        	print "Failed to parse line: $err";
	    }
 
	} 
	$dbh->disconnect(); 
	close (cdr_log); 

    system("cat $line >> /usr/local/freeswitch/log/cdr-csv/FULL_Master.csv"); # we do this to maintain a single FULL file if needed
    unlink $line;
}

exit 0;
