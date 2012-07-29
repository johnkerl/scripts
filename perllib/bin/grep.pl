# ----------------------------------------------------------------
# John Kerl
# john dot r dot kerl at lmco dot com
# 2001/02/06
#
# A Windows workalike for the Unix "grep" program.
#
# ----------------------------------------------------------------
# Pattern-matching options:
# -i: Case insensitive
# -v: Invert match
# -w: Match on word boundary
#
# Display options (mutually exclusive):
# -c: Print only file_name & count
# -l: Print only matching file names
# -n: Print line numbers in additional to file name
# ----------------------------------------------------------------

# ----------------------------------------------------------------
use My_win_glob;

# ----------------------------------------------------------------
$usage_string = "Usage: $0 [-ivwcln] {pattern} {zero or more file names ...}\n";

$opt_i = 0;
$opt_v = 0;
$opt_w = 0;

$opt_c = 0;
$opt_l = 0;
$opt_n = 0;

# ----------------------------------------------------------------
# Parse options.

while (@ARGV > 0) {

	last unless ($ARGV[0] =~ m/^[-\/]/);

	@opts = split //, $ARGV[0];
	shift @ARGV; # Don't consider this argument to be a filename.
	shift @opts; # Shift off leading "-" or "/".

	foreach $opt (@opts) {

		if    ($opt =~ m/^i$/i) {
			$opt_i = 1;
		}

		elsif ($opt =~ m/^v$/i) {
			$opt_v = 1;
		}

		elsif ($opt =~ m/^w$/i) 
			{ $opt_w = 1;
		}


		elsif ($opt =~ m/^c$/i) {
			$opt_c = 1;
			$opt_l = 0;
			$opt_n = 0;
		}

		elsif ($opt =~ m/^l$/i) {
			$opt_c = 0;
			$opt_l = 1;
			$opt_n = 0;
		}

		elsif ($opt =~ m/^n$/i) {
			$opt_c = 0;
			$opt_l = 0;
			$opt_n = 1;
		}

		else  {
			print "Unrecognized option: $ARGV[0].\n";
			die $usage_string;
		}

	}
}

# ----------------------------------------------------------------
die $usage_string unless (@ARGV > 0);
$pat = shift @ARGV;
if ($opt_w) {
	$pat = "\\b" . $pat . "\\b";
}

# ----------------------------------------------------------------
if (@ARGV) {

	my $globrc;
	($globrc, @ARGV) = my_win_glob(@ARGV);
	exit unless $globrc;

	$my_num_files = @ARGV;
	for my $file_name (@ARGV) {
		next if -d $file_name;
		$quiet_file_name = ($my_num_files > 1 ? $file_name : "");
		if (open(FILE_HANDLE, $file_name)) {
			grep_handle($pat, $file_name, $quiet_file_name, \*FILE_HANDLE);
			close FILE_HANDLE;
		}
		else {
			print "Couldn't open file \"$file_name\"; skipping.\n";
		}
	}
}
else {
	grep_handle($pat, "(stdin)", "", \*STDIN);
}

# ----------------------------------------------------------------
sub grep_handle {
	my ($pat, $file_name, $quiet_file_name, $file_handle) = @_;
	my $line_count = 0;
	my $match_count = 0;

	while ($line = <$file_handle>) {
		my $match;

		chomp $line;
		$line_count++;

		if ($opt_i) {
			$match = ($line =~ m/$pat/i);
		}
		else {
			$match = (uc $line =~ m/$pat/);
		}

		$match = !$match if ($opt_v);

		if ($opt_l) {
			if ($match) {
				print "$file_name\n";
				last;
			}
		}

		elsif ($opt_n) {
			if ($match) {
				print "$file_name:$line_count: $line\n";
			}
		}

		elsif ($opt_c) {
			if ($match && !$opt_v) {
				$match_count++;
			}
			elsif (!$match && $opt_v) {
				$match_count++;
			}
		}

		else {
			if ($match) {
				if ($quiet_file_name) {
					print "$quiet_file_name: ";
				}
				print "$line\n";
			}
		}
	}

	if ($opt_c) {
		print "$file_name:$match_count\n";
	}
}
