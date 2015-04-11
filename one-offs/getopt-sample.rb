#!/usr/bin/env ruby

# ================================================================
# A Ruby option-parse cheat sheet.
# ================================================================

$us = File.basename $0
$ourdir = File.dirname $0

require 'getoptlong'

def usage()
   $stderr.puts "Usage: #{File.basename $0} {-a aarg} {-f farg} {-i iarg} {-l}"
   exit 1
end

# ----------------------------------------------------------------
aarg = "adefault"
farg = nil
iarg = nil
lopt = 0

opts = GetoptLong.new(
    [ '-a', GetoptLong::REQUIRED_ARGUMENT ],
    [ '-f', GetoptLong::REQUIRED_ARGUMENT ],
    [ '-i', GetoptLong::REQUIRED_ARGUMENT ],
    [ '-l', GetoptLong::NO_ARGUMENT ],
    [ '--help', GetoptLong::NO_ARGUMENT ]
)

begin
    opts.each do |opt, arg|
   case opt
      when '-a'; aarg = arg
      when '-f'; farg = Float(arg)   # arg.to_f won't raise ArgumentError for invalid forma
      when '-i'; iarg = Integer(arg) # arg.to_i won't raise ArgumentError for invalid forma
      when '-l'; lopt = 1
      when '--help'; usage
   end
    end
rescue GetoptLong::Error
    usage
end

non_option_args      = ARGV
non_option_arg_count = ARGV.length

puts "aarg = #{aarg}"
puts "farg = #{farg}"
puts "iarg = #{iarg}"
puts "lopt = #{lopt}"
puts "# non-option args: #{non_option_arg_count}"
for arg in non_option_args
   puts "Non-option arg: #{arg}"
end
