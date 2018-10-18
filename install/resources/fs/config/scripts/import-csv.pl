#!/usr/bin/perl -w
#
# PyFreeBilling v2.0
# v1.21
#


use strict;
use DBI();
use File::Basename;
use File::Copy;
use Text::CSV_XS;
use POSIX;
use Socket;
use Sys::Hostname;

# set variables
my $host = hostname();
my $addr = '';
my $csv = Text::CSV_XS->new({ quote_char => '"', always_quote => 1 }) or die "Cannot use CSV: ".Text::CSV->error_diag ();

my $cdr_files = "/tmp/cdr-csv/Master.csv.*";
my $cdr_archive_dir = "/var/log/freeswitch/cdr-csv/";

my $pg_db = "pyfreebilling";
my $pg_host = "localhost";
my $pg_port = "5432";
my $pg_table = "cdr";
my $pg_user = "pyfreebilling";
my $pg_pwd = undef; # read password from  ~/.pgpass

# this commands HUPS fs, she creates new cdr.csv files, so we can load the old ones up
# debian package : /usr/bin/fs_cli
my $command  = ("fs_cli -x 'cdr_csv rotate'");
system($command) == 0 or die "$0: system cdr_csv rotate failed: $?";

# Connect to database
my $dsn="DBI:Pg:dbname=$pg_db;host=$pg_host;port=$pg_port";
my $dbh=DBI->connect($dsn,$pg_user,$pg_pwd)or die "$0: Couldn't connect to database: " . DBI->errstr;

my $insert_str = "insert into $pg_table (customer_id, customer_ip, uuid, caller_id_number, destination_number, chan_name, start_stamp, answered_stamp, end_stamp, duration, read_codec, write_codec, hangup_cause, hangup_cause_q850, gateway_id, cost_rate, prefix, country, rate, init_block, block_min_duration, lcr_carrier_id_id, ratecard_id_id, lcr_group_id_id, sip_user_agent, sip_rtp_rxstat, sip_rtp_txstat, bleg_uuid, switchname, switch_ipv4, hangup_disposition, effectiv_duration, sip_hangup_cause, effective_duration, billsec, total_sell, total_cost, sell_destination, cost_destination, customerdirectory_id, sip_charge_info) values ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);";
my $sth = $dbh->prepare($insert_str) or die "$0: Couldn't prepare statement\n$insert_str\n" . $dbh->errstr;

my @files = glob($cdr_files);
foreach my $file (@files) {
    print "Processing $file\n";
    open cdr_log, "< $file" or die "Cannot open cdr_log_file ".$file."\n";
    while (<cdr_log>) {
        if ($csv->parse($_)) {
            my (@fields) = $csv->fields();
            $fields[7] = undef unless $fields[7];
            $fields[14] = undef unless $fields[14];
            $fields[21] = undef unless $fields[21];
            $fields[22] = undef unless $fields[22];
            $fields[23] = undef unless $fields[23];
            $fields[357] = undef unless $fields[35];

            # duration, total sell and total cost calculation
            # effective duration
            my $effectiveduration = 0;
            my $billsec = 0;
            my $totalcost = 0;
            my $totalsell = 0;
#            print " effectiv_duration : $fields[31] \n\n";
            if (!$fields[31]){
                $effectiveduration = 0;
            }
            else
            {
                $effectiveduration = ceil($fields[31]/ 1000.0);
            }
#            print " effective_duration : $effectiveduration\n\n";
#            billed duration
#            print " block_min_duration : $fields[20] \n\n";
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
#            print " billsec : $billsec \n\n";
#            total sell 18 -15
#            print " sell rate : $fields[18] \n\n";
#            print " init block rate : $fields[19] \n\n";
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
#            print " total_sell : $totalsell \n\n";
#            total cost
#            print " cost_rate : $fields[15] \n\n";
            if ($fields[15]){
                $totalcost = sprintf("%.6f", ($billsec * $fields[15] / 60.0));
            }
            else
            {
                $totalcost = sprintf("%.6f", 0);
            }
#            print " total_cost : $totalcost \n\n";

            $sth->execute($fields[0], $fields[1], $fields[2], $fields[3], $fields[4], $fields[5], $fields[6], $fields[7], $fields[8], $fields[9], $fields[10], $fields[11], $fields[12], $fields[13], $fields[14], $fields[15], $fields[16], $fields[17], $fields[18], $fields[19], $fields[20], $fields[21], $fields[22], $fields[23], $fields[24], $fields[25], $fields[26], $fields[27], $host, $addr, $fields[30], $fields[31], $fields[32], $effectiveduration, $billsec, $totalsell, $totalcost, $fields[33], $fields[34], $fields[35], $fields[36]) or print "$0: Couldn't execute statement: " . $dbh->errstr;
        } else {
            my $err = $csv->error_input;
            print "Failed to parse line: $err";
        }
    }
    close (cdr_log);
    move($file, $cdr_archive_dir);
    unlink $file;
}
$sth->finish();
$dbh->disconnect() or warn "Disconnection failed: $DBI::errstr\n";

exit 0;
