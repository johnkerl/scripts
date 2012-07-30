#!/usr/bin/perl

$N = 256;
$kmin =  0;
$kmax = 10;
$a = 0.2;
$pi = 4*atan2(1,1);

$xmin = -0.5;
$xmax =  0.5;
$dx   = ($xmax - $xmin) / $N;

for ($i = 0, $x = $xmin; $i < $N; $i++, $x += $dx) {
	$y = 0.0;
	printf "%11.7e", $x;
	for ($k = $kmin; $k <= $kmax; $k++) {
		$y += mysinc($k) * cos(2 * $pi * $k * $x);
		printf " %11.7e", $y;
	}
	print "\n";
}

sub mysinc
{
	my ($k) = @_;
	my $sk;
	if ($k == 0.0) {
		$sk = 2 * $a;
	}
	else {
		$sk = sin(2 * $pi * $k * $a) / ($pi * $k);
	}
	return $sk;
}
