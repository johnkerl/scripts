#!/usr/bin/env ruby

# Like uniq but accepts out-of-order input. Much faster than sort | uniq or sort -u.

require 'set'
lines_seen = Set.new
ARGF.each do |line|
   unless lines_seen.include? line
      puts line
      lines_seen << line
   end
end
