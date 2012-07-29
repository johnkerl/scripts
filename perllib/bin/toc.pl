use My_win_glob;

# ================================================================
# Please see perl-on-windows-notes.txt for background.
# John Kerl
# 12/27/2000 
# ================================================================

my $globrc;
($globrc, @ARGV) = my_win_glob(@ARGV);
exit unless $globrc;

foreach $arg (@ARGV) {
	print "\n";

	# If argument ends in .pl, take it off.
	$base = $arg;
	if ($arg =~ m/\.pl$/) {
		$base =~ s/\.pl$//;
	}

	$pl_name    = $base . ".pl";
	$cmd_name   = $base . ".cmd";
	$c_cmd_path = "c:\\bin\\" . $cmd_name;

	print "$pl_name:\n";

	open (C_CMD_HANDLE, ">$c_cmd_path") or die "Couldn't open $c_cmd_path: $!\n";
	print C_CMD_HANDLE "\@echo off\n";
	print C_CMD_HANDLE "c:\\bin\\perl.exe c:\\bin\\$pl_name %*\n";
	close(C_CMD_HANDLE);

	system("copy $pl_name c:\\bin");
}
