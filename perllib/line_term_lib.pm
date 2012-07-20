# ================================================================
# John Kerl
# 2010-06-23
#
# ================================================================
# At my desk, I have a Windows machine.  I spend most of my time ssh'ed into
# Linux machines.  Yet, directories are mounted back and forth between Windows
# and Linux.  All my Perl scripts run on Linux, yet I may wish to store, read,
# and/or write DOS-format files on a Linux machine, or vice versa.
# Furthermore, I want my filters to preserve the file line endings.
#
# DOS format:   Line ends in \015\012, also known as CR/LF, also known
#               as \r\n.
# Unix format:  Line ends in \012, also known as LF, also known as \n.
#
# What I want:
#
# * Processing a DOS  file on Unix machine:  use DOS  terminators.
# * Processing a DOS  file on DOS  machine:  use DOS  terminators.
# * Processing a Unix file on Unix machine:  use Unix terminators.
# * Processing a Unix file on DOS  machine:  use Unix terminators.
#
# Perl has $/ and $\, which are record separators (line terminators) for input
# and output, respectively.  However, these tell me the preferences for the
# machine, not the current file being operated on.  Perl's chomp removes $/
# from input.  Likewise, "\n" in output translates to $\, which will turn out
# to be "\r\n" or "\n" depending on whether the Perl script is running on
# Windows or Linux, respectively.
#
# This module is one solution.  Example use of a catter which preserves
# line endings:
#
# use line_term_lib;
# while ($line = <>) {
#     # Get this line's ending and remember it ...
#     ($line, $term) = split_line_ending($line);
#     # ... print it back out with that ending.
#     print "$line$term";
# }

# ================================================================

package line_term_lib;
require Exporter;

@ISA = qw(Exporter);

@EXPORT = qw(
	split_line_ending
);

# ----------------------------------------------------------------
# Splits line into unterminated_line and terminator.
# Think of this as a chomp which tells you what it chomped off.

sub split_line_ending {
	my ($line) = @_;
	if ($line =~ m/\015\012$/) {
		$line =~ s/\015\012$//;
		$term = "\015\012";
	}
	elsif ($line =~ m/\012$/) {
		$line =~ s/\012$//;
		$term = "\012";
	}
	else {
		$term = "";
	}
	return ($line, $term);
}
