# ================================================================
# John Kerl
# kerl.john.r@gmail.com
# 2005-06-01
#
# This is a Perl library for simple I/O and arithmetic on matrices
# and vectors of floating-point numbers.
#
# Setup information:
# (1) Put this file somewhere, e.g. the $HOME/bin directory;
# (2) Include that directory in the PERLLIB environment variable.
#     For bash, if PERLLIB exists:
#       export PERLLIB=$HOME/bin
#     For bash, if PERLLIB does not exist:
#       export PERLLIB=$PERLLIB:$HOME/bin
#     For csh, if PERLLIB exists:
#       setenv PERLLIB $HOME/bin
#     For csh, if PERLLIB does not exist:
#       setenv PERLLIB ${PERLLIB}:$HOME/bin
# ================================================================

package PMATLIB;
require Exporter;

@ISA = qw(Exporter);

@EXPORT = qw(
	read_matrix
	print_matrix

	read_row_vector
	read_column_vector
	print_row_vector
	print_column_vector
	read_scalar
	print_scalar

	make_I
	make_zero_matrix
	transpose_in_place
	matdet
	matinv
	row_reduce_below
	row_echelon_form
	get_rank
	get_rank_rr

	get_kernel_basis
	check_kernel_basis

	matuneg
	matuneg_in_place

	householder_vector_to_Q
	householder_UT_pass_on_submatrix

	gram_schmidt
	rs_eigensystem

	matmul
	matsmul
	matadd
	dot
	outer
	matrix_times_vector
	vector_times_matrix

	vecadd
	vecsub
	vecadd_with_smul
	vecsub_with_smul
	vector_times_scalar

	get_column
	put_column
	get_row
	put_row
	copy_matrix

	vector_is_zero

	tol_zero
	tol_non_zero

	binc

	pmatlib_opt
	pmatlib_options_string);

$pml_field_width        = 11;
$pml_num_decimal_places =  7;
$pml_printf_style       = "f";
$pml_printf_format      = "%$pml_field_width.$pml_num_decimal_places" .
$pml_printf_style;
$pml_print_brackets           = 0;

$pml_tolerance          = 1e-12;

# ----------------------------------------------------------------
sub read_matrix
{
	my ($mxref, $nrref, $ncref, $filename) = @_;
	my $mincols = 9999999999;
	my $maxcols = 0;
	my @lines;

	die "read_matrix():  Need as arguments matrix reference and dimensions.\n"
		unless defined $ncref;

	if (defined $filename) {
		if (!open(HANDLE, $filename)) {
			die "read_matrix:  Couldn't open file \"$filename\".\n";
		}
		@lines = <HANDLE>;
		close(HANDLE);
	}
	else {
		@lines = <>;
	}

	$$nrref = 0;
	$$ncref = 0;
	for ($i = 0; $i < @lines; $i++) {
		$line = $lines[$i];
		chomp $line;
		$line =~ s/^\s+//;
		$line =~ s/\s+$//;
		next if $line =~ m/^$/;
		my @fields = split /\s+/, $line;
		$maxcols = @fields if @fields > $maxcols;
		$mincols = @fields if @fields < $mincols;
		for ($j = 0; $j < @fields; $j++) {
			my $string = $fields[$j];
			my $val = read_scalar($string);
			$$mxref[$$nrref][$j] = $val;
		}
		$$nrref++;
	}
	if (@lines == 0) {
		die "read_matrix:  empty input.\n";
	}
	if ($maxcols != $mincols) {
		die "read_matrix:  ragged input matrix:  min cols $mincols, max cols $maxcols.\n";
	}
	$$ncref = $maxcols;
}

# ----------------------------------------------------------------
sub print_matrix
{
	my ($mxref, $nr, $nc) = @_;
	my $i;
	my $j;

	die "print_matrix():  Need as arguments matrix reference and dimensions.\n"
		unless defined $nc;

	if ($pml_print_brackets) {
		for $i (0 .. $nr - 1) {
			print "[" if ($i == 0);
			print " " if ($i > 0);
			for $j (0 .. $nc - 1) {
				printf $pml_printf_format, $$mxref[$i][$j];
				print ", " if ($j < $nc - 1)
			}
			print ";" if ($i < $nr-1);
			print "]" if ($i == $nr-1);
			print "\n";
		}
	}

	else {
		for $i (0 .. $nr - 1) {
			for $j (0 .. $nc - 1) {
				printf $pml_printf_format, $$mxref[$i][$j];
				print " " if ($j < $nc - 1)
			}
			print "\n";
		}
	}
}

# ----------------------------------------------------------------
sub read_row_vector
{
	my ($vecref, $nref, $filename) = @_;
	my (@tempmat, $tempnr, $tempnc, $j);

	read_matrix(\@tempmat, \$tempnr, \$tempnc, $filename);
	if ($tempnr != 1) {
		die "read_column_vector:  too many rows ($tempnr) in input.\n";
	}
	for ($j = 0; $j < $tempnc; $j++) {
		$$vecref[$j] = $tempmat[0][$j];
	}
	$$nref = $tempnc;
}

# ----------------------------------------------------------------
sub read_column_vector
{
	my ($vecref, $nref, $filename) = @_;
	my (@tempmat, $tempnr, $tempnc, $i);

	read_matrix(\@tempmat, \$tempnr, \$tempnc, $filename);
	if ($tempnc != 1) {
		die "read_row_vector:  too many columns ($tempnc) in input.\n";
	}
	for ($i = 0; $i < $tempnr; $i++) {
		$$vecref[$i] = $tempmat[$i][0];
	}
	$$nref = $tempnr;
}

# ----------------------------------------------------------------
sub print_row_vector
{
	my ($vecref, $n) = @_;
	my $j;

	die "print_row_vector():  Need as arguments vector reference and dimension.\n"
		unless defined $n;

	for $j (0 .. $n - 1) {
		printf $pml_printf_format, $$vecref[$j];
		print " " if ($j < $n - 1)
	}
	print "\n";
}

# ----------------------------------------------------------------
sub print_column_vector
{
	my ($vecref, $n) = @_;
	my $i;

	die "print_column_vector():  Need as arguments vector reference and dimension.\n"
		unless defined $n;

	for $i (0 .. $n - 1) {
		printf $pml_printf_format, $$vecref[$i];
		print "\n";
	}
}

# ----------------------------------------------------------------
sub read_scalar
{
	my ($string) = @_;
	my $value;

	die "read_scalar():  Need string as argument.\n"
		unless defined $string;

	if ($string =~ m:/:) {
		# Allow fractional input, e.g "2/3".
		my ($numer, $denom) = split /\//, $string;
		$value = $numer / $denom;
	}
	else {
		$value = $string
	}

	return $value;
}

# ----------------------------------------------------------------
sub print_scalar
{
	my ($s) = @_;

	die "print_scalar():  Need scalar as argument.\n"
		unless defined $s;

	printf $pml_printf_format, $s;
}

# ----------------------------------------------------------------
sub make_I
{
	my ($n) = @_;
	my (@A, $i, $j);

	die "make_I():  Need n as argument.\n"
		unless defined $n;
	for ($i = 0; $i < $n; $i++) {
		for ($j = 0; $j < $n; $j++) {
			$A[$i][$j] = 0.0;
		}
	}
	for ($i = 0; $i < $n; $i++) {
		$A[$i][$i] = 1.0;
	}

	return @A;
}

# ----------------------------------------------------------------
sub make_zero_matrix
{
	my ($nr, $nc) = @_;
	my (@A, $i, $j);

	die "make_zero_matrix():  Need dimensions as arguments.\n"
		unless defined $nc;
	for ($i = 0; $i < $nr; $i++) {
		for ($j = 0; $j < $nc; $j++) {
			$A[$i][$j] = 0.0;
		}
	}

	return @A;
}

# ----------------------------------------------------------------
sub transpose_in_place
{
	my ($mxref, $nrref, $ncref) = @_;
	my ($i, $j, $nr, $nc);
	my @T;

	die "transpose_in_place():  Need as arguments matrix reference and dimension references.\n"
		unless defined $ncref;

	$nr = $$nrref;
	$nc = $$ncref;
	for $i (0 .. $nr - 1) {
		for $j (0 .. $nc - 1) {
			$T[$j][$i] = $$mxref[$i][$j];
		}
	}
	@$mxref = copy_matrix(\@T, $nc, $nr);
	$$nrref = $nc;
	$$ncref = $nr;
}

# ----------------------------------------------------------------
sub matdet
{
	my ($aref, $n, $verbose) = @_;
	my @A = copy_matrix($aref, $n, $n);

	die "matdet():  Need as arguments matrix reference and dimensions.\n"
		unless defined $n;
	# verbose is an optional argument.

	# Use Householder transformations to put the matrix into upper-triangular
	# form.  Each transformation is (effectively) a pre-multiplication by a
	# Householder matrix with determinant -1.  Account for this below.
	for ($i = 0; $i < $n; $i++) {
		householder_UT_pass_on_submatrix(\@A, $n, $n, $i);
	}

	# Take the product along the diagonal.  The negative sign accounts for the
	# factors of -1 introduced by the Householder transformations.
	my $det = 1.0;
	for ($i = 0; $i < $n; $i++) {
		$det *= -$A[$i][$i];
	}
	return $det;
}

# ----------------------------------------------------------------
sub matinv
{
	my ($aref, $bref, $n) = @_;
	my ($row_start, $i, $j);
	my $twon = $n + $n;
	my @ai;

	die "matinv():  Need as arguments two matrix references and dimensions.\n"
		unless defined $n;

	# First, paste the input and the identity side by side.
	$row_start = 0;
	for ($i = 0; $i < $n; $i++) {
		for ($j = 0; $j < $n; $j++) {
			$ai[$i][$j] = $$aref[$i][$j];
		}
	}
	for ($i = 0; $i < $n; $i++) {
		for ($j = 0; $j < $n; $j++) {
			$ai[$i][$j+$n] = 0.0;
		}
	}
	for ($i = 0; $i < $n; $i++) {
		$ai[$i][$i+$n] = 1.0;
	}

	# Second, use Householder transformations to put it into upper-triangular
	# form.
	for ($i = 0; $i < $n; $i++) {
		householder_UT_pass_on_submatrix(\@ai, $n, $twon, $i);
	}

	# Third, put 1 on the left diagonal.
	for ($i = 0; $i < $n; $i++) {
		my $d = $ai[$i][$i];
		if ($d == 0.0) {
			die "Singular.\n";
		}
		elsif (tol_zero($d)) {
			die "Nearly singular.\n";
		}
		for ($j = 0; $j < $twon; $j++) {
			$ai[$i][$j] = $ai[$i][$j] / $d;
		}
	}

	# Fourth, clear out the rest of the left-hand side.
	# 1 . . . .  . . . . .
	# 0 1 . . .  . . . . .
	# 0 0 1 . .  . . . . .
	# 0 0 0 1 .  . . . . .  <-- i
	# 0 0 0 0 1  . . . . .  <-- i2

	for ($i = $n-2; $i >= 0; $i--) {
		for ($i2 = $n-1; $i2 > $i; $i2--) {
			$mul = $ai[$i][$i2];
			for ($j = 0; $j < $twon; $j++) {
				$ai[$i][$j] -= $ai[$i2][$j] * $mul;
			}
		}
	}

	# Fifth, obtain the inverse from the right-hand side.
	for ($i = 0; $i < $n; $i++) {
		for ($j = 0; $j < $n; $j++) {
			$$bref[$i][$j] = $ai[$i][$j+$n];
		}
	}
}

# ----------------------------------------------------------------
# This is a general row-reduction routine.  It operates on the matrix in-place.

sub row_reduce_below
{
	my ($aref, $nr, $nc) = @_;
	my ($top_row, $left_col, $cur_row, $j);

	for ($top_row = 0, $left_col = 0; ($top_row < $nr) && ($left_col < $nc); ) {

		# Find the nearest row with a non-zero value in this column;
		# exchange that row with this one.
		my $pivot_row = $top_row;
		my $pivot_successful = 0;
		while (!$pivot_successful && ($pivot_row < $nr)) {
			# At the moment, this is naive pivoting, appropriate for
			# exact arithmetic (e.g. finite fields).
			# For floating-point (here), this needs to work harder to
			# find the best row to pivot in.
			if (tol_non_zero($$aref[$pivot_row][$left_col])) {
				if ($top_row != $pivot_row) {
					# Swap top row and pivot row
					my @temp = @$aref[$top_row];
					@$aref[$top_row] = @$aref[$pivot_row];
					@$aref[$pivot_row] = @temp;
				}
				$pivot_successful = 1;
			}
			else {
				$pivot_row++;
			}
		}
		if (!$pivot_successful) {
			$left_col++;
			next; # Work on the next column.
		}

		# We can have a zero leading element in this row if it's
		# the last row and full of zeroes.
		my $top_row_lead = $$aref[$top_row][$left_col];
		if (tol_non_zero($top_row_lead)) {
			# Normalize this row.
			my $inv = 1.0 / $top_row_lead;
			for ($j = 0; $j < $nc; $j++) {
				$$aref[$top_row][$j] *= $inv;
			}

			# Clear this column.
			$top_row_lead = $$aref[$top_row][$left_col];
			for ($cur_row = $top_row + 1; $cur_row < $nr; $cur_row++) {
				my $current_row_lead = $$aref[$cur_row][$left_col];
				for ($j = 0; $j < $nc; $j++) {
					$$aref[$cur_row][$j] =
						$$aref[$cur_row][$j] * $top_row_lead -
						$$aref[$top_row][$j] * $current_row_lead;
				}
			}
		}
		$left_col++;
		$top_row++;
	}
}

# ----------------------------------------------------------------
# Operates on the matrix in-place.

sub row_echelon_form
{
	my ($aref, $nr, $nc) = @_;
	my ($row, $row2, $row2_leader_pos);
	my ($row_clear_val, $row2_leader_val, $mul, $j);

	row_reduce_below($aref, $nr, $nc);

	for ($row = 0; $row < $nr; $row++) {
		for ($row2 = $row+1; $row2 < $nr; $row2++) {
			my @row2copy = get_row($aref, $nr, $nc, $row2);
			last if !find_leader_pos(\@row2copy, $nc, \$row2_leader_pos);

			$row2_leader_val = $$aref[$row2][$row2_leader_pos];
			$row_clear_val = $$aref[$row][$row2_leader_pos];
			next if (tol_zero($row_clear_val));

			$mul = $row_clear_val / $row2_leader_val;
			for ($j = 0; $j < $nc; $j++) {
				$$aref[$row][$j] -= $$aref[$row2][$j] * $mul;
			}
		}
	}
}

# ----------------------------------------------------------------
# This routine makes a copy of the matrix and row-reduces it.  To save
# CPU cycles, use get_rank_rr() if the matrix is already row-reduced.

sub get_rank
{
	my ($aref, $nr, $nc) = @_;
	my @Arr = copy_matrix($aref, $nr, $nc);
	row_reduce_below(\@Arr, $nr, $nc);
	return get_rank_rr(\@Arr, $nr, $nc);
}

# ----------------------------------------------------------------
# This routine assumes the matrix is already row-reduced.  If not,
# use get_rank() instead.

sub get_rank_rr
{
	my ($aref, $nr, $nc) = @_;
	my $rank = 0;
	my ($i, $j);

	for ($i = 0; $i < $nr; $i++) {
		my $row_is_zero = 1;
		for ($j = 0; $j < $nc; $j++) {
			if (tol_non_zero($$aref[$i][$j])) {
				$row_is_zero = 0;
				last;
			}
		}
		$rank++ if (!$row_is_zero);
	}
	return $rank;
}

# ----------------------------------------------------------------
sub get_kernel_basis
{
	my ($aref, $nr, $nc, $basisref, $dimref) = @_;
	my ($i, $j);

	my @rr = copy_matrix($aref, $nr, $nc);
	row_echelon_form(\@rr, $nr, $nc);
	my $rank = get_rank_rr(\@rr, $nr, $nc);
	my $dimker = $nc - $rank;

	return 0 if ($dimker == 0);

	my @kerbas = make_zero_matrix($dimker, $nc);

	my @free_flags;
	my @free_indices;
	my $nfree = 0; # == dimker but I'll compute it anyway
	my $dep_pos;

	for ($i = 0; $i < $nc; $i++) {
		$free_flags[$i] = 1;
	}

	for ($i = 0; $i < $rank; $i++) {
		my @rowcopy = get_row(\@rr, $nr, $nc, $i);
		if (find_leader_pos(\@rowcopy, $nc, \$dep_pos)) {
			$free_flags[$dep_pos] = 0;
		}
	}

	for ($i = 0; $i < $nc; $i++) {
		if ($free_flags[$i]) {
			$free_indices[$nfree++] = $i;
		}
	}

	# For each free coefficient:
	#   Let that free coefficient be 1 and the rest be zero.
	#   Also set any dependent coefficients which depend on that
	#   free coefficient.
	for ($i = 0; $i < $dimker; $i++) {
		$kerbas[$i][$free_indices[$i]] = 1.0;

		# Matrix in row echelon form:
		#
		# 0210     c0 = ??      c0 = 1  c0 = 0
		# 1000     c1 = -2 c2   c1 = 0  c1 = 5
		# 0000     c2 = ??      c2 = 0  c2 = 1
		# 0000     c3 = 0       c3 = 0  c3 = 0
 
		# j  = 0,1
		# fi = 0,2
 
		# i = 0:
		#   j = 0  row 0 fi 0 = row 0 c0 = 0
		#   j = 1  row 1 fi 0 = row 1 c0 = 0
		# i = 1:
		#   j = 0  row 0 fi 1 = row 0 c2 = 2 dep_pos = 1
		#   j = 1  row 1 fi 1 = row 1 c2 = 0
 
		# 0001
		# 01?0
 
		for ($j = 0; $j < $rank; $j++) {
			next if (tol_zero($rr[$j][$free_indices[$i]]));

			my @rowcopy = get_row(\@rr, $nr, $nc, $j);
			if (!find_leader_pos(\@rowcopy, $nc, \$dep_pos)) {
				die "Coding error in get_kernel_basis!\n";
			}

			$kerbas[$i][$dep_pos] = -$rr[$j][$free_indices[$i]];
		}
	}

	# #ifdef KERBAS_DEBUG
	#	std::cout << "start check:\n";
	#	std::cout << "A  =\n" << *this << "\n";
	#	std::cout << "rr =\n" << rr << "\n";
	# 
	#	for (i = 0; i < dimker; i++) {
	#		std::cout << "v  = " << kerbas.rows[i] << "\n";
	#	}
	#	std::cout << "\n";
	#	for (i = 0; i < dimker; i++) {
	#		tvector Av = *this * kerbas.rows[i];
	#		std::cout << "Av = " << Av << "\n";
	#	}
	#	std::cout << "end check.\n";
	#	std::cout << "\n";
	# #endif # KERBAS_DEBUG

	check_kernel_basis($aref, $nr, $nc, \@kerbas, $dimker);

	@$basisref = @kerbas;
	$$dimref = $dimker;

	return 1;
}

# ----------------------------------------------------------------
sub check_kernel_basis
{
	my ($aref, $nr, $nc, $basisref, $dimker) = @_;
	my $i;
	for ($i = 0; $i < $dimker; $i++) {
		my @v = get_row($basisref, $dimker, $nc, $i);
		my @Av = matrix_times_vector($aref, $nr, $nc, \@v, $nc);
		if (!vector_is_zero(\@Av, $nr)) {
			print "Coding error in kernel basis.\n";
			print "Matrix:\n";
			print_matrix($aref, $nr, $nc);
			print "Basis:\n";
			print_matrix($basisref, $dimker, $nc);
			print "Product at row $i:\n";
			print_row_vector(\@Av, $nr);
			die;
		}
	}
}

# ----------------------------------------------------------------
sub matuneg
{
	my ($aref, $nr, $nc) = @_;
	my ($i, $j, @N);

	die "matuneg():  Need as arguments matrix reference and dimensions.\n"
		unless defined $nc;

	for ($i = 0; $i < $nr; $i++) {
		for ($j = 0; $j < $nc; $j++) {
			$N[$i][$j] = -$$aref[$i][$j];
		}
	}
	return @N;
}

# ----------------------------------------------------------------
sub matuneg_in_place
{
	my ($aref, $nr, $nc) = @_;
	my ($i, $j);

	die "matuneg_in_place():  Need as arguments matrix reference and dimensions.\n"
		unless defined $nc;

	for ($i = 0; $i < $nr; $i++) {
		for ($j = 0; $j < $nc; $j++) {
			$$aref[$i][$j] = -$$aref[$i][$j];
		}
	}
}

# ----------------------------------------------------------------
# Q = I - 2 v v^t / (v^t v)

sub householder_vector_to_Q
{
	my ($vref, $n) = @_;
	die "householder_vector_to_Q():  Need as arguments vector reference and length.\n"
		unless defined $n;
	my $v_dot_v = dot($vref, $vref, $n);
	my @Q = make_I($n);
	if ($v_dot_v >= $pml_tolerance) {
		my ($i, $j);
		$two_over_v_dot_v = 2.0 / $v_dot_v;
		for ($i = 0; $i < $n; $i++) {
			for ($j = 0; $j < $n; $j++) {
				$Q[$i][$j] -= $$vref[$i]*$$vref[$j] * $two_over_v_dot_v;
			}
		}
	}
	return @Q
}

# ----------------------------------------------------------------
# Applies a Householder transformation.

sub householder_UT_pass_on_submatrix
{
	my ($aref, $nr, $nc, $a) = @_;
	my $height = $nr - $a;
	my $i;
	my $j;
	my $k;
	my $ia;
	my $ja;
	my $ka;

	die "householder_UT_pass_on_submatrix():  Need as arguments matrix reference, dimensions, and start column.\n"
		unless defined $a;

	# Get column 0
	my @col0 = get_submatrix_column($aref, $nr, $nc, $a, $a);

	# Compute ||col0|| and Qcol0.
	my $Qcol00 = sqrt(dot(\@col0, \@col0, $height));
	if ($col0[0] >= 0) {
		$Qcol00 = -$Qcol00;
	}
	$Qcol0[0] = $Qcol00;
	for ($j = 1; $j < $height; $j++) {
		$Qcol0[$j] = 0.0;
	}

	# Compute axis = col0 - Qcol0.
	my @axis = vecsub(\@col0, \@Qcol0, $height);

	# Compute the Householder transformation
	my @Q = householder_vector_to_Q(\@axis, $height);

	# Apply the Householder transformation
	my @tmp = make_zero_matrix($nr-$a, $nc-$a);
	for ($i = $a; $i < $nr; $i++) {
		$ia = $i - $a;
		for ($j = $a; $j < $nc; $j++) {
			$ja = $j - $a;
			for ($k = $a; $k < $nr; $k++) {
				$ka = $k - $a;
				$tmp[$ia][$ja] += $Q[$ia][$ka] * $$aref[$k][$j];
	 		}
	 	}
	}
	for ($i = $a; $i < $nr; $i++) {
		$ia = $i - $a;
		for ($j = $a; $j < $nc; $j++) {
			$ja = $j - $a;
			$$aref[$i][$j] = $tmp[$ia][$ja];
		}
	}
}

# ----------------------------------------------------------------
# Gram-Schmidt orthonormalization:
#
# Orthogonality step:
#   Input  {a_0 .. a_{n-1}}
#   Output {q_0 .. q_{n-1}}
#   q_0 = a_0
#   q_j = a_j - sum_{k=0}^{j-1} (a_j dot q_k)/(q_k dot q_k) q_k
# Normalization: q_j *= 1 / ||q_j||

sub gram_schmidt
{
	my ($aref, $nr, $nc) = @_;
	my (@Q, $i, $j, $k, @aj, @qj, @qk);

	die "gram_schmidt():  Need as arguments matrix reference and dimensions.\n"
		unless defined $nc;

	# Orthogonality
	for ($j = 0; $j < $nc; $j++) {
		@aj = get_column($aref, $nr, $nc, $j);
		@qj = @aj;

		# q_j = a_j - sum_{k=0}^{j-1} (a_j dot q_k)/(q_k dot q_k) q_k

		for ($k = 0; $k < $j; $k++) {
			@qk = get_column(\@Q, $nr, $nc, $k);
			my $numer = dot(\@aj, \@qk, $nr);
			my $denom = dot(\@qk, \@qk, $nr);
			if ($denom == 0.0) {
				die "Column $k of Q is zero in PMATLIB::gram_schmidt.\n";
			}
			my $quot = $numer / $denom;
			@qj = vecsub_with_smul(\@qj, \@qk, $nr, $quot);
		}
		put_column(\@Q, $nr, $nc, $j, \@qj);
	}

	# Normalization
	for ($j = 0; $j < $nc; $j++) {
		@qj = get_column(\@Q, $nr, $nc, $j);
		my $dot = dot(\@qj, \@qj, $nr);
		my $norm_recip = 1.0 / sqrt($dot);
		@qj = vector_times_scalar(\@qj, $nr, $norm_recip);
		put_column(\@Q, $nr, $nc, $j, \@qj);
	}

	return @Q;
}

# ----------------------------------------------------------------
# At present, this is coded very naively.  Loosely adapted from Numerical Recipes.

sub rs_eigensystem
{
	my ($aref, $n, $dref, $vref) = @_;
	my ($p, $q);
	my @A = copy_matrix($aref, $n, $n);
	my @V = make_I($n);
	my $maxiter = 20;

	for ($iter = 1; ; $iter++) {
		my $sum = 0.0;
		for ($i = 1; $i < $n; $i++) {
			for ($j = 0; $j < $i; $j++) {
				$sum += abs($A[$i][$j]);
			}
		}
		#printf "sum at iteration $iter is %11.7e\n", $sum; printf "\n";
		last if (tol_zero($sum**2));

		if ($iter > $maxiter) {
			die "Jacobi eigensolver: max iterations ($maxiter) exceeded.  Non-symmetric input?\n";
		}

		for ($p = 0; $p < $n; $p++) {
			for ($q = $p+1; $q < $n; $q++) {

				my $numer = $A[$p][$p] - $A[$q][$q];
				my $denom = $A[$p][$q] + $A[$q][$p];
				next if (tol_zero($denom));
				my $theta = $numer / $denom;
				my $sign_theta = ($theta < 0.0) ? -1 : 1;
				my $t = $sign_theta / (abs($theta) + sqrt($theta**2 + 1));
				my $c = 1.0 / sqrt($t**2 + 1);
				my $s = $t * $c;
				my @P = make_I($n);
				$P[$p][$p] =  $c;
				$P[$p][$q] = -$s;
				$P[$q][$p] =  $s;
				$P[$q][$q] =  $c;

				my $foo = $n;
				my $bar = $n;

				my @PT = @P;
				transpose_in_place(\@PT, \$foo, \$bar);

				matmul(\@PT, $n, $n, \@A, $n, $n, \@A, \$foo, \$bar);
				matmul(\@A,  $n, $n, \@P, $n, $n, \@A, \$foo, \$bar);
				matmul(\@V,  $n, $n, \@P, $n, $n, \@V, \$foo, \$bar);

				#printf "theta=%11.7f sign_theta=%11.7f\n", $theta, $sign_theta;
				#printf "c=%11.7f s=%11.7f\n", $c, $s;
				#print "P^t[$p][$q]:\n"; print_matrix(\@PT, $n, $n); print "\n";
				#print "P[$p][$q]:\n";   print_matrix(\@P,  $n, $n); print "\n";
				#print "A[$p][$q]:\n";   print_matrix(\@A,  $n, $n); print "\n";
				#print "V[$p][$q]:\n";   print_matrix(\@V,  $n, $n); print "\n";

			}
		}
	}

	@$dref = copy_matrix(\@A, $n, $n);
	@$vref = copy_matrix(\@V, $n, $n);
}

# ----------------------------------------------------------------
sub matmul
{
	my ($aref, $anr, $anc, $bref, $bnr, $bnc, $cref, $cnrref, $cncref) = @_;

	my $i;
	my $j;
	my $k;
	my @C;

	die "matmul():  Need as arguments two matrix references and dimensions.\n"
		unless defined $cncref;
	die "matmul():  Incompatible dimensions $anr x $anc, $bnr x $bnc.\n"
		unless ($anc == $bnr);

	for $i (0 .. $anr - 1) {
		for $j (0 .. $bnc - 1) {
			$C[$i][$j] = 0.0;
			for $k (0 .. $bnr - 1) {
				$C[$i][$j] += $$aref[$i][$k] * $$bref[$k][$j];
			}
		}
	}

	for $i (0 .. $anr - 1) {
		for $j (0 .. $bnc - 1) {
			$$cref[$i][$j] = $C[$i][$j];
		}
	}

	$$cnrref = $anr;
	$$cncref = $bnc;

}

# ----------------------------------------------------------------
sub matsmul
{
	my ($aref, $anr, $anc, $scalar, $cref) = @_;
	my ($i, $j);

	die "matsmul():  Need as arguments two matrix references and dimensions.\n"
		unless defined $cref;
	for ($i = 0; $i < $anr; $i++) {
		for ($j = 0; $j < $anc; $j++) {
			$$cref[$i][$j] = $scalar * $$aref[$i][$j];
		}
	}
}

# ----------------------------------------------------------------
sub matadd
{
	my ($aref, $anr, $anc, $bref, $bnr, $bnc, $cref, $cnrref, $cncref) = @_;

	my $i;
	my $j;

	die "matadd():  Need as arguments two matrix references and dimensions.\n"
		unless defined $cncref;
	die "matadd():  Incompatible dimensions $anr x $anc, $bnr x $bnc.\n"
		unless (($anr == $bnr) && ($anr == $bnr));

	for $i (0 .. $anr - 1) {
		for $j (0 .. $bnc - 1) {
			$$cref[$i][$j] = $$aref[$i][$j] + $$bref[$i][$j];
		}
	}
	$$cnrref = $anr;
	$$cncref = $bnc;
}

# ----------------------------------------------------------------
# Input  matrix is         nr x nc
# Input  vector has length nc
# Output vector has length nr

sub matrix_times_vector {
	my ($aref, $nr, $nc, $xref, $n) = @_;
	my (@b, $i, $j);

	die "matrix_times_vector():  Need as arguments matrix reference, dimensions, vector reference, and length.\n"
		unless defined $n;
	die "matrix_times_vector():  Incompatible dimensions $nr x $nc, $n.\n"
		unless ($nc == $n);

	for $i (0 .. $nr - 1) {
		$b[$i] = 0.0;
		for $j (0 .. $nc - 1) {
			$b[$i] += $$aref[$i][$j] * $$xref[$j];
		}
	}

	return @b;
}

# ----------------------------------------------------------------
# Input  vector has length nr
# Input  matrix is         nr x nc
# Output vector has length nc

sub vector_times_matrix {
	my ($xref, $n, $aref, $nr, $nc) = @_;
	my (@b, $i, $j);

	die "vector_times_matrix():  Need as arguments vector reference, length, matrix reference, and dimensions.\n"
		unless defined $nc;
	die "vector_times_matrix():  Incompatible dimensions $n, $nr x $nc.\n"
		unless ($n == $nr);

	for $j (0 .. $nc - 1) {
		$b[$j] = 0.0;
		for $i (0 .. $nr - 1) {
			$b[$j] += $$aref[$i][$j] * $$xref[$i];
		}
	}

	return @b;
}

# ----------------------------------------------------------------
sub vecadd
{
	my ($uref, $vref, $n) = @_;
	my (@w, $i);

	die "vecadd():  Need as arguments two vector references and length.\n"
		unless defined $n;

	for ($i = 0; $i < $n; $i++) {
		$w[$i] = $$uref[$i] + $$vref[$i];
	}
	return @w;
}

# ----------------------------------------------------------------
sub vecsub
{
	my ($uref, $vref, $n) = @_;
	my (@w, $i);

	die "vecsub():  Need as arguments two vector references and length.\n"
		unless defined $n;

	for ($i = 0; $i < $n; $i++) {
		$w[$i] = $$uref[$i] - $$vref[$i];
	}
	return @w;
}

# ----------------------------------------------------------------
sub vecadd_with_smul
{
	my ($uref, $vref, $n, $c) = @_;
	my (@w, $i);

	die "vecadd_with_smul():  Need as arguments two vector references, length, "
		. "and scalar.\n"
		unless defined $c;

	for ($i = 0; $i < $n; $i++) {
		$w[$i] = $$uref[$i] + $$vref[$i] * $c;
	}
	return @w;
}

# ----------------------------------------------------------------
sub vecsub_with_smul
{
	my ($uref, $vref, $n, $c) = @_;
	my (@w, $i);

	die "vecsub_with_smul():  Need as arguments two vector references, length, "
		. "and scalar.\n"
		unless defined $c;

	for ($i = 0; $i < $n; $i++) {
		$w[$i] = $$uref[$i] - $$vref[$i] * $c;
	}
	return @w;
}

# ----------------------------------------------------------------
sub vector_times_scalar
{
	my ($uref, $n, $c) = @_;
	my (@v, $i);

	die "vector_times_scalar():  Need as arguments vector reference, length, "
		. "and scalar.\n"
		unless defined $c;

	for ($i = 0; $i < $n; $i++) {
		$v[$i] = $$uref[$i] * $c;
	}
	return @v;
}

# ----------------------------------------------------------------
sub dot
{
	my ($uref, $vref, $n) = @_;

	die "dot():  Need as arguments two vector references and length.\n"
		unless defined $n;

	my $sum = 0.0;
	my $i;
	for ($i = 0; $i < $n; $i++) {
		$sum += $$uref[$i] * $$vref[$i];
	}
	return $sum;
}

# ----------------------------------------------------------------
sub outer
{
	my ($uref, $vref, $m, $n) = @_;

	die "outer():  Need as arguments two vector references and lengths.\n"
		unless defined $n;

	my ($i, $j, @uv);
	for ($i = 0; $i < $m; $i++) {
		for ($j = 0; $j < $n; $j++) {
			$uv[$i][$j] = $$uref[$i] * $$vref[$j];
		}
	}
	return @uv;
}

# ----------------------------------------------------------------
sub get_submatrix_column
{
	my ($aref, $nr, $nc, $colidx, $start_row) = @_;
	my ($src, $dst);
	my @submatrix_column;
	for ($src = $start_row, $dst = 0; $src < $nr; $src++, $dst++) {
		$submatrix_column[$dst] = $$aref[$src][$colidx];
	}
	return @submatrix_column;
}

# ----------------------------------------------------------------
sub put_submatrix_column
{
	my ($aref, $nr, $nc, $colidx, $start_row, $pcolref) = @_;
	my ($src, $dst);
	for ($src = 0, $dst = $start_row; $dst < $nr; $src++, $dst++) {
		$$aref[$dst][$colidx] = $$pcolref[$src];
	}
}

# ----------------------------------------------------------------
sub get_column
{
	my ($aref, $nr, $nc, $colidx) = @_;
	my $i;
	my @column;
	for ($i = 0; $i < $nr; $i++) {
		$column[$i] = $$aref[$i][$colidx];
	}
	return @column;
}

# ----------------------------------------------------------------
sub put_column
{
	my ($aref, $nr, $nc, $colidx, $pcolref) = @_;
	my $i;
	for ($i = 0; $i < $nr; $i++) {
		$$aref[$i][$colidx] = $$pcolref[$i];
	}
}

# ----------------------------------------------------------------
sub get_row
{
	my ($aref, $nr, $nc, $rowidx) = @_;
	my $j;
	my @row;
	for ($j = 0; $j < $nc; $j++) {
		$row[$j] = $$aref[$rowidx][$j];
	}
	return @row;
}

# ----------------------------------------------------------------
sub put_row
{
	my ($aref, $nr, $nc, $rowidx, $prowref) = @_;
	my $j;
	for ($j = 0; $j < $nc; $j++) {
		$$aref[$rowidx][$j] = $$prowref[$j];
	}
}

# ----------------------------------------------------------------
sub copy_matrix
{
	my ($aref, $nr, $nc) = @_;
	my ($i, $j, @C);
	for ($i = 0; $i < $nr; $i++) {
		for ($j = 0; $j < $nc; $j++) {
			$C[$i][$j] = $$aref[$i][$j];
		}
	}
	return @C;
}

# ----------------------------------------------------------------
sub vector_is_zero
{
	my ($vref, $n) = @_;
	my $i;
	for ($i = 0; $i < $n; $i++) {
		if (tol_non_zero($$vref[$i])) {
			return 0;
		}
	}
	return 1;
}

# ----------------------------------------------------------------
# Return value:  True/false.  rpos:  index, if found.

sub find_leader_pos
{
	my ($vref, $n, $posref) = @_;
	my $j;
	$$posref = -999; # temp
	for ($j = 0; $j < $n; $j++) {
		if (tol_non_zero($$vref[$j])) {
			$$posref = $j;
			return 1;
		}
	}
	return 0;
}

# ----------------------------------------------------------------
sub tol_zero
{
	my ($f) = @_;
	if (abs($f) < $pml_tolerance) {
		return 1;
	}
	else {
		return 0;
	}
}

# ----------------------------------------------------------------
sub tol_non_zero
{
	my ($f) = @_;
	if (abs($f) < $pml_tolerance) {
		return 0;
	}
	else {
		return 1;
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
sub pmatlib_options_string
{
	return
		"  -w:  specify field width\n" .
		"  -p:  specify number of decimal places\n" .
		"  -f:  use %f format\n" .
		"  -d:  use %d format\n";
}

sub pmatlib_opt
{
	my ($argvref) = @_;

	if ($$argvref[0] eq "-w") {
		shift @$argvref;
		return 0 unless @$argvref;
		$pml_field_width = $$argvref[0];
		$pml_printf_format = "%$pml_field_width.$pml_num_decimal_places" . $pml_printf_style;
		shift @$argvref;
		return 1;
	}
	elsif ($$argvref[0] eq "-p") {
		shift @$argvref;
		return 0 unless @$argvref;
		$pml_num_decimal_places = $$argvref[0];
		$pml_printf_format = "%$pml_field_width.$pml_num_decimal_places" . $pml_printf_style;
		shift @$argvref;
		return 1;
	}
	elsif ($$argvref[0] eq "-e") {
		$pml_printf_style = "e";
		$pml_printf_format = "%$pml_field_width.$pml_num_decimal_places" . $pml_printf_style;
		shift @$argvref;
		return 1;
	}
	elsif ($$argvref[0] eq "-f") {
		$pml_printf_style = "f";
		$pml_printf_format = "%$pml_field_width.$pml_num_decimal_places" . $pml_printf_style;
		shift @$argvref;
		return 1;
	}
	elsif ($$argvref[0] eq "-d") {
		$pml_printf_format = "%d";
		shift @$argvref;
		return 1;
	}
	elsif ($$argvref[0] eq "-fmt") {
		shift @$argvref;
		return 0 unless @$argvref;
		$pml_printf_format = $$argvref[0];
		shift @$argvref;
		return 1;
	}
	elsif ($$argvref[0] eq "-bracket") {
		$pml_print_brackets = 1;
		shift @$argvref;
		return 1;
	}
	elsif ($$argvref[0] eq "-tol") {
		shift @$argvref;
		return 0 unless @$argvref;
		$pml_tolerance = $$argvref[0];
		shift @$argvref;
		return 1;
	}
	else {
		return 0;
	}
}

1;

