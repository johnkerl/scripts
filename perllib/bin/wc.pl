use My_win_glob;

# ----------------------------------------------------------------
# John Kerl
# john dot r dot kerl at lmco dot com
# 2000/11/08
#
# A Windows workalike for the Unix "wc" filter.
#
# To do:  Implement -l, -w, -c command-line options.
# ----------------------------------------------------------------

$total_num_lines = 0;
$total_num_words = 0;
$total_num_chars = 0;
$num_files = 0;

if (@ARGV) {
	my $globrc;
	($globrc, @ARGV) = my_win_glob(@ARGV);
	exit unless $globrc;

	foreach $filename (@ARGV) {
		next if -d $filename;
		if (open(FILEHANDLE, $filename)) {
			count_handle(\*FILEHANDLE);
			close FILEHANDLE;
		}
		else {
			print "Couldn't open file \"$filename\"; skipping.\n";
		}
	}
}
else {
	$filename="stdin";
	count_handle(\*STDIN);
}

if ($num_files > 1) {
	printf "%6d %6d %6d %s\n",
		$total_num_lines, $total_num_words, $total_num_chars, "Total";
}

# ----------------------------------------------------------------
sub count_handle {
	my ($file_handle) = @_;
	my $num_lines = 0;
	my $num_words = 0;
	my $num_chars = 0;

	while ($line = <$file_handle>) {
		$num_lines++;
		$num_words += split /\s+/, $line;
		$num_chars += length($line);
	}

	printf "%6d %6d %6d %s\n", $num_lines, $num_words, $num_chars, $filename;

	$total_num_lines += $num_lines;
	$total_num_words += $num_words;
	$total_num_chars += $num_chars;
	$num_files++;
}
