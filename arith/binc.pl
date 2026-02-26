#!/usr/bin/perl -w

# ================================================================
# John Kerl
# 2005-01-25
#
# This program prints binomial coefficients, optionally reduced mod p.
# Examples:
#
# binc ch 7 4
# 35
# 
# binc -p 3 ch 7 4
# 2
# 
# binc row 7
# 1 7 21 35 35 21 7 1
# 
# binc -p 5 row 7
# 1 2 1 0 0 1 2 1
# 
# binc -p 7 row 7
# 1 0 0 0 0 0 0 1
# 
# binc tri 10 | colprint -r
# 1
# 1  1
# 1  2  1
# 1  3  3   1
# 1  4  6   4   1
# 1  5 10  10   5   1
# 1  6 15  20  15   6   1
# 1  7 21  35  35  21   7   1
# 1  8 28  56  70  56  28   8  1
# 1  9 36  84 126 126  84  36  9  1
# 1 10 45 120 210 252 210 120 45 10 1
#
# binc -p 2 tri 10
# 1
# 1 1
# 1 0 1
# 1 1 1 1
# 1 0 0 0 1
# 1 1 0 0 1 1
# 1 0 1 0 1 0 1
# 1 1 1 1 1 1 1 1
# 1 0 0 0 0 0 0 0 1
# 1 1 0 0 0 0 0 0 1 1
# 1 0 1 0 0 0 0 0 1 0 1
#
# binc -p 7 tri 10
# 1
# 1 1
# 1 2 1
# 1 3 3 1
# 1 4 6 4 1
# 1 5 3 3 5 1
# 1 6 1 6 1 6 1
# 1 0 0 0 0 0 0 1
# 1 1 0 0 0 0 0 1 1
# 1 2 1 0 0 0 0 1 2 1
# 1 3 3 1 0 0 0 1 3 3 1
#
# binc -p 2 -dot tri 30
# .
# ..
# . .
# ....
# .   .
# ..  ..
# . . . .
# ........
# .       .
# ..      ..
# . .     . .
# ....    ....
# .   .   .   .
# ..  ..  ..  ..
# . . . . . . . .
# ................
# .               .
# ..              ..
# . .             . .
# ....            ....
# .   .           .   .
# ..  ..          ..  ..
# . . . .         . . . .
# ........        ........
# .       .       .       .
# ..      ..      ..      ..
# . .     . .     . .     . .
# ....    ....    ....    ....
# .   .   .   .   .   .   .   .
# ..  ..  ..  ..  ..  ..  ..  ..
# . . . . . . . . . . . . . . . .
# ================================================================

$how  = "lucas";
$dots = 0;
$p    = 0;

# ----------------------------------------------------------------
sub usage
{
	die
		"Usage: $0 [options] ch  {n} {k}\n" .
		"Or   : $0 [options] row {n}\n" .
		"Or   : $0 [options] tri {nmax}\n" .
		"Computes binomial coefficients, optionally reduced mod p.\n" .
		"  ch:  compute a single binomial coefficient.\n" .
		"  row: compute a row of Pascal's triangle: n choose k for k = 0 to kmax.\n" .
		"  tri: compute nmax rows of Pascal's triangle.\n" .
		"Options:\n" .
		"  --help:    Print this message.\n" .
		"  -p {p}:    Prime to reduce by.\n" .
		"  -lucas:    Reduce mod p using Lucas Theorem (default).  p must be prime.\n" .
		"  -kerl:     Reduce mod p using Kerl's slow method.  p must be prime.\n" .
		"  -modafter: Reduce mod p after computing n choose k (prone to overflow)\n" .
		"  -dot:      Print just a dot for non-zero values, space for zeroes.\n";
}

# ----------------------------------------------------------------
while (@ARGV && ($ARGV[0] =~ m/^-/)) {
	my $opt = shift @ARGV;
	if ($opt eq "--help") {
		usage();
	}
	elsif ($opt eq "-p") {
		usage() unless @ARGV;
		$p = shift @ARGV;
	}
	elsif ($opt eq "-lucas") {
		$how = "lucas";
	}
	elsif ($opt eq "-kerl") {
		$how = "kerl";
	}
	elsif ($opt eq "-modafter") {
		$how = "modafter";
	}
	elsif ($opt eq "-dot") {
		$dots = 1;
	}
	else {
		usage();
	}
}

usage() unless @ARGV;
$what = shift @ARGV;
if ($what eq "ch") {
	usage() unless (@ARGV == 2);
	$n = shift @ARGV;
	$k = shift @ARGV;
	do_one($n, $k, $p);
	print "\n";
}

elsif ($what eq "row") {
	usage() unless (@ARGV == 1);
	$n    = shift @ARGV;
	for ($k = 0; $k <= $n; $k++) {
		if (($k > 0) && !$dots) {
			print " ";
		}
		do_one($n, $k, $p);
	}
	print "\n";
}

elsif ($what eq "tri") {
	usage() unless (@ARGV == 1);
	$nmax = shift @ARGV;
	for ($n = 0; $n <= $nmax; $n++) {
		for ($k = 0; $k <= $n; $k++) {
			if (($k > 0) && !$dots) {
				print " ";
			}
			do_one($n, $k, $p);
		}
		print "\n";
	}
}

else {
	usage();
}

# ----------------------------------------------------------------
sub do_one
{
	my ($n, $k, $p) = @_;
	my $b;

	if (($p == 0) || ($how eq "z")) {
		$b = binc($n, $k);
	}
	elsif ($how eq "lucas") {
		$b = bincp_lucas($n, $k, $p);
	}
	elsif ($how eq "kerl") {
		$b = bincp_kerl($n, $k, $p);
	}
	elsif ($how eq "modafter") {
		$b = binc($n, $k) % $p;
	}
	else {
		usage();
	}

	if ($dots) {
		if ($b == 0) {
			print " ";
		}
		else {
			#print ".";
			print "o";
		}
	}
	else {
		print $b;
	}
}

# ----------------------------------------------------------------
sub binc
{
	my ($n, $k) = @_;
	return 0 if ($k > $n);
	return 0 if ($k < 0);
	if ($k > int($n/2)) {
		$k = $n - $k;
	}

	my $rv = 1;
	for my $j (0 .. $k-1) {
		$rv *= $n - $j;
		$rv /= $j + 1;
	}
	return $rv;
}

# ----------------------------------------------------------------
# See http://mathworld.wolfram.com/LucasCorrespondenceTheorem.html.
# Write n and k in base-p notation, with digits n_i and k_i.  Then (n choose k)
# is equivalent mod p to the product of the (n_i choose k_i)'s.

sub bincp_lucas
{
	my ($n, $k, $p) = @_;
	if ($k > int($n/2)) {
		$k = $n - $k;
	}
	my $rv = 1;

	while ($n || $k) {
		my $n_i = $n % $p; $n = int($n / $p);
		my $k_i = $k % $p; $k = int($k / $p);
		my $b = binc($n_i, $k_i);
		$rv *= $b;
		$rv %= $p;
	}

	return $rv;
}

# ----------------------------------------------------------------
sub bincp_kerl
{
	my ($n, $k, $p) = @_;
	return 0 if ($k > $n);
	return 0 if ($k < 0);
	if ($k > int($n/2)) {
		$k = $n - $k;
	}

	my $numer = 1;
	my $denom = 1;
	my $pcount = 0;

	my $rv = 1;
	for my $j (0 .. $k-1) {
		my $curnumer = $n - $j;
		while (($curnumer % $p) == 0) {
			$pcount++;
			$curnumer /= $p;
		}
		$numer *= $curnumer;
		$numer %= $p;

		my $curdenom = $j+1;
		while (($curdenom % $p) == 0) {
			$pcount--;
			$curdenom /= $p;
		}
		$denom *= $curdenom;
		$denom %= $p;
	}
	if ($pcount > 0) {
		$rv = 0;
	}
	elsif ($pcount == 0) {
		$rv = $numer * modrecip($denom, $p);
		$rv %= $p;
	}
	else {
		die "$0: coding error; pcount=$pcount.\n";
	}
	return $rv;
}

# ----------------------------------------------------------------
sub modrecip
{
	my ($a, $p) = @_;
	$a %= $p;
	die "modrecip: division by zero.\n" if (($a % $p) == 0);
	my $rv = 1;
	my $e = $p-2;
	while ($e--) {
		$rv *= $a;
		$rv %= $p;
	}
	return $rv;
}
