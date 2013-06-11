// http://static.rust-lang.org/doc/std/files/getopts-rs.html


fn main(args: [str]) {
  let opts = [
    optopt("o"),
    optflag("h"),
    optflag("help")
  ];
  let match = alt getopts(vec::shift(args), opts) {
    ok(m) { m }
    err(f) { fail fail_str(f) }
  };
  if opt_present(match, "h") || opt_present(match, "help") {
    print_usage();
    ret;
  }
  let output = opt_maybe_str(match, "o");
  let input = if !vec::is_empty(match.free) {
    match.free[0]
  } else {
    print_usage();
    ret;
  }
  do_work(input, output);
}

