#!/usr/bin/env ruby

# ================================================================
# A Ruby option-parse cheat sheet.
# ================================================================

$us = File.basename $0
$ourdir = File.dirname $0

require 'optparse'

options = {}
optparse = OptionParser.new do |o|
   o.banner = "Usage: #{$us} [options]"
   o.separator ""
   o.separator "Options:"
   o.on('-r', '--rlong RARG',   'This is for a required flag with value')     { |arg| options[:rarg] = arg }
   o.on('-o', '--olong [OARG]', 'This is for an optional flag with value')    { |arg| options[:oarg] = arg }
   o.on('-l', '--list',         'This is for an optional flag with no value') { options[:larg] = true }
end
rv = optparse.parse!
puts "parse rv = #{rv.inspect}"
puts "ARGV     = #{ARGV.inspect}"
