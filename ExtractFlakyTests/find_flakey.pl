#!/usr/bin/perl -w

use strict;
use warnings;
use DBI;
use Data::Dumper;
use List::MoreUtils qw(uniq);

#my $dbh_ref = DBI->connect("dbi:Pg:dbname=firefox_build_crash;host=localhost", "rupak", "karmadhar", {AutoCommit => 0});
#my $select = $dbh_ref->prepare(q{
#	select build_id, test_name, info from fx_build_tests where info ~ E'FAIL|PASS' group by build_id, test_name, info order by build_id asc
#});
#
#my @result = $select->execute();
#
#open my $fh, '>>', 'output.txt' or die "Could not open file output.txt: $!";
#print $fh qq{build_id|test_name|info\n};
#while (my $result = $select->fetchrow_hashref) {
#	print $fh qq{$result->{'build_id'}|$result->{'test_name'}|$result->{'info'}\n};
#}
#
#close $fh;
#
my @flakey;
my @flakeyBuilds;
my $i = 0;
my $j = 0;
my $prev_line = "";
my $file = 'output.txt';

open my $fin, $file or die "Could not open $file: $!";
while( my $line = <$fin>)  {
	$line =~ s/(\s|\n)+$//;
	
	if($i > 0) {
		if($i == 1){
			$prev_line = $line;
		}
		else{
			my @a_prev = split /\|/, $prev_line;
			my $build_prev = $a_prev[0];
			my $test_prev = $a_prev[1];
			my $info_prev = $a_prev[2];
			
			my @a = split /\|/, $line;
			my $build = $a[0];
                        my $test = $a[1];
                        my $info = $a[2];
			#print $build_prev."-".$test_prev."-".$info_prev." -- ".$build."-".$test."-".$info."\n";
			if($build_prev eq $build && $test_prev eq $test && $info_prev ne $info){
				$flakey[$j] = $line; 
				$flakeyBuilds[$j] = $build; $j++;
				print $prev_line." - ".$line."\n";
			}
			$prev_line = $line;
		}
	}
	$i++;
}

close $fin;

@flakeyBuilds = uniq(@flakeyBuilds);
my $outfile;
my $scal = "";

open $outfile, '>>', "flakey_builds.txt" or die "Could not create file.\n";
$scal = join(",", @flakey);
print {$outfile} $scal;
close $outfile; 
#
#$select->finish();
#$dbh_ref->disconnect;
