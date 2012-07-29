use My_win_glob;

# ----------------------------------------------------------------
# John Kerl
# john dot r dot kerl at lmco dot com
# 2000/11/08
#
# A Windows workalike for the Unix "tail" filter.
# ----------------------------------------------------------------

my $tail_lines = 10;

if (@ARGV) {
	if ($ARGV[0] =~ m/^[\/-]/) {
		$tail_lines = $ARGV[0];
		$tail_lines =~ s/^.//;
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
			tail_handle(\*FILEHANDLE, $tail_lines);
			close FILEHANDLE;
		}
		else {
			print "Couldn't open file \"$filename\"; skipping.\n";
		}
	}
}
else {
	$filename="stdin";
	tail_handle(\*STDIN, $tail_lines);
}

# ----------------------------------------------------------------
sub tail_handle {
	my ($file_handle, $tail_lines) = @_;
	my @lines = <$file_handle>;
	my $file_lines = @lines;
	my $start = ($tail_lines > $file_lines) ? 0 : $file_lines - $tail_lines;
	my $i;

	for ($i = $start; $i < $file_lines; $i++) {
		chomp $lines[$i];
		print $lines[$i] , "\n";
	}
}
