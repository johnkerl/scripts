#!/usr/bin/perl -w

$pi  = 4.0 * atan2(1.0, 1.0);
$xlo = 0.0;
$xhi = 2.0 * $pi;
$nx  = 1000;
$dx  = ($xhi - $xlo) / $nx;

for ($x = $xlo; $x <= $xhi; $x += $dx) {
	$y = cos($x);
	$y2 = $y ** 2;
	$y3 = $y ** 3;
	$y4 = $y ** 4;
	printf "%11.7f %11.7f %11.7f %11.7f %11.7f\n",
		$x, $y, $y2, $y3, $y4;
}
