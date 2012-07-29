# John Kerl
# 2001-02-06

# Windows shells don't glob for you; commands must do it themselves.
# However, that globbing is suboptimal:
# * dir *\*.c does not work; the dir command uses a Windows routine which
#   globs only the last *.
# * fc *.txt doesn't work at all, even if you have a.txt and b.txt, since the
#   fc command doesn't glob its arguments.
#
# This command globs its arguments, then executes them.  E.g.:
# * w dir *\*.c
# * w fc *.txt

use My_win_glob;

my $globrc;
($globrc, @ARGV) = my_win_glob(@ARGV);
system(join " ", @ARGV)
	if $globrc;
