#!/usr/bin/perl -w

use strict;
use warnings;
use File::Find;
use DBI;
use Data::Dumper;
use File::Basename;
use Try::Tiny;

my @files;
my $start_dir = "/media/rupak/SmallBackup/firefox_crashs/TBPL/tbpl-logs-2012/";
#my $start_dir = "/home/taj/Documents/firefox_data/tbpl-logs-2011/";  # top level dir to search
my $start_dir = "/home/rupak/Documents/2010-11/";
find( 
    sub { push @files, $File::Find::name unless -d; }, 
    $start_dir
);

my @log_files;
for my $file (@files) {
	if ($file =~ /gz$/ ) {
		push (@log_files, $file);
    	}    
}
#print "Total: ".@log_files; exit;

my $dbh_ref = DBI->connect("dbi:Pg:dbname=firefox_build_crash;host=localhost", "rupak", "karmadhar", {AutoCommit => 0});
my $insert = $dbh_ref->prepare(q{
	INSERT INTO fx_build_tests(build_id, info, test_case, test_desc, test_name) 
	VALUES(?, ?, ?, ?, ?);
});

for my $gzipfile (@log_files) {
	my $file = remove_extension($gzipfile);

	if (-e $file) {
	    print "Already Extracted: ".$file."\nDo not unzip.\n";
	}
	else{
		system("gunzip ".$gzipfile);
	}
	
	print "Processing: ".$file."\n";

	my $buildid = ""; 
	my @testing = ();
	
	if (-e $file) {
	    my $i = 0;
	    open my $fh, '<', $file or die "Can't open $file: $!";
	    while (<$fh>) {
	    	#print "$.> $_";
		my @m;

		### Searching for build id
		@m = ( $_ =~ /^buildid:\s([0-9]+)/ );
		
		if(@m){
			$buildid = $m[0];
			#print "Build ID: ".$buildid."\n";
		}
		
		# Searching for test case
		if ( $_ =~ /TEST\-UNEXPECTED/ or $_ =~ /TEST\-FAIL/ or $_ =~ /TEST\-PASS/ or $_ =~ /TEST\-KNOWN/ ) {
			
			my @exploded = split / \| /, $_;
			#print Dumper(@exploded);
			if(@exploded) {
				# 0 = test_info; 1 = test_case; 2 = test_desc; 3 = test_name;
				if(scalar @exploded > 0 ) {
					
					my @match = ( $exploded[0] =~ /TEST\-(.*)/ );
					
					if(scalar @match > 0 && defined $match[0]){
						$testing[$i][0] = $match[0];
					} else {
						$testing[$i][0] = "";
					}

					if($exploded[1] && defined $exploded[1]) {
						$testing[$i][1] = $exploded[1] =~ s/\r+|\t+|\n+$//r;
					} else {
						$testing[$i][1] = "";
					}
					if(scalar @exploded > 1 && defined $exploded[2]) {
						$testing[$i][2] = $exploded[2] =~ s/\r+|\t+|\n+$//r;
					} else {
						$testing[$i][2] = "";
					}
					
					# Extract the test name
					my @tmp; my $test_name;
					if($exploded[1] && defined $exploded[1]){
						$test_name = basename($exploded[1]);
						
						if($test_name =~ /^test_/){
							$test_name =~ s/^test_//;
						}
						if($test_name =~ /\.[^.]+$/){
							$test_name =~ s/\.[^.]+$//;
						}
					} 
					$testing[$i][3] = $test_name;
					$i++;
				}
			}
		}
	    }
	}
	
	if(-e $file){
		system("gzip ".$file);
		system("mv ".$file.".gz /media/rupak/SmallBackup/firefox_crashs/TBPL/extracted-2012/");
	}
	
	# Load into database
	if (length($buildid) > 0){
		foreach my $t (@testing){
			try{
				if(length($t->[0]) > 0 && length($t->[1]) > 0 && length($t->[2]) > 0 && length($t->[3]) > 0){
					$insert->execute($buildid, $t->[0], $t->[1], $t->[2], $t->[3]);
				}
			} catch {
			        warn "caught error: $_";
				continue;
			};
		}
		$dbh_ref->commit;
	}
}

#$dbh_ref->commit;
$insert->finish();
$dbh_ref->disconnect;

sub remove_extension {
    my $filename = shift @_;

    $filename =~ s/(.)\.[^.]+$/$1/x;

    return $filename;
}
