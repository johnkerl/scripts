use My_win_glob;

# ----------------------------------------------------------------
# John Kerl
# john dot r dot kerl at lmco dot com
# 2000/11/08
#
# A Windows workalike for the Unix "head" filter.
# ----------------------------------------------------------------

my $head_lines = 10;

if (@ARGV) {
	if ($ARGV[0] =~ m/^[\/-]/) {
		$head_lines = $ARGV[0];
		$head_lines =~ s/^.//;
		shift @ARGV;
	}
}

if (@ARGV) {

	my $globrc;
	($globrc, @ARGV) = my_win_glob(@ARGV);
	exit unless $globrc;

	foreach $filename (@ARGV) {
		next if -d $filename;
		if (open(FILEHANDLE, $filename)) {
			if (@ARGV > 1) {
				print "-" x 64, "\n";
				print "-- $filename --\n";
			}
			head_handle(\*FILEHANDLE, $head_lines);
			close FILEHANDLE;
		}
		else {
			print "Couldn't open file \"$filename\"; skipping.\n";
		}
	}
}
else {
	$filename="stdin";
	head_handle(\*STDIN, $head_lines);
}

# ----------------------------------------------------------------
sub head_handle {
	my ($file_handle, $head_lines) = @_;

	my $num_lines_read = 0;
	while ($line = <$file_handle>) {
		$num_lines_read++;
		chomp $line;
		print "$line\n";
		last if $num_lines_read >= $head_lines;
	}
}
