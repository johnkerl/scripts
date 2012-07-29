# ----------------------------------------------------------------
# John Kerl
# john dot r dot kerl at lmco dot com
# 2000/11/08
#
# A Windows workalike for the Unix "uniq" filter.
# ----------------------------------------------------------------

my $do_counter = 0;
if ((@ARGV >= 1) && ($ARGV[0] =~ m/^[\/-]c$/i)) {
	$do_counter = 1;
	shift @ARGV;
}

# ----------------------------------------------------------------
@lines_in  = <>;
@lines_out = ();

# ----------------------------------------------------------------
for my $line (@lines_in) {
	chomp $line;
}

# ----------------------------------------------------------------
my $at_first   = 1;
my $counts_out = ();

while (@lines_in) {
	if ($at_first) {
		$at_first = 0;
		push @lines_out, shift @lines_in;
		push @counts_out, 1;
	}
	else {
		if ($lines_in[0] eq $lines_out[$#lines_out]) {
			$counts_out[$#counts_out]++;
			shift @lines_in;
		}
		else {
			push @lines_out, shift @lines_in;
			push @counts_out, 1;
		}
	}
}

print "\n";

# ----------------------------------------------------------------
while (@lines_out) {
	printf "%4d: ", $counts_out[0] if ($do_counter);
	print $lines_out[0], "\n";
	shift @lines_out;
	shift @counts_out;
}
