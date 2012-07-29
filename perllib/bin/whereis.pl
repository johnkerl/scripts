use My_win_glob;

# ----------------------------------------------------------------
# John Kerl
# john dot r dot kerl at lmco dot com
# 2000/11/08
#
# A Windows workalike for the Unix "which" program.
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# Get the semicolon-delimited value of the PATH environment variable,
# splitting it up into an array.  

$path_env_var_name = "PATH";

$colon_dirs = $ENV{$path_env_var_name};
@dirs_array = split /;/, $colon_dirs;

# ----------------------------------------------------------------
# For each file name of interest:
#    For each directory name in the PATH variable, see if the file name of
#    interest is located there.
#
# If no filenames are presented, then just print out the path,
# line-delimited.

if (@ARGV) {
	foreach $sought_filename (@ARGV) {
		print "\n";
		$found = 0;
		foreach $dir (@dirs_array) {
			chomp $dir;
			$possible_location = $dir . "\\" . $sought_filename;

			foreach $globbo (split /\0/, `perlglob $possible_location`) {
				if (-e $globbo) {
					print $globbo, "\n";
					$found = 1;
				}
			}

		}
		if ($found == 0) {
			print "Couldn't find \"$sought_filename\" in $path_env_var_name.\n";
		}
	}
}
else {
	foreach $dir (@dirs_array) {
		chomp $dir;
		print $dir, "\n";
	}
}
