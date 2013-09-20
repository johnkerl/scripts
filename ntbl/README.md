These are some little utility scripts for manipulating CSV files.

Formats are CSV, CSKV, horizontal, and vertical.  Examples:

CSV:
```
a,b,c
1,2,3
4,5,6
```

CSKV:
```
a=1,b=2,c=3
a=4,b=5,c=6
```

Horizontal:
```
a b c
- - -
1 2 3
4 5 6
```

Vertical:
```
a 1 4
b 2 5
c 3 6
```

* CSV is best for storage and piping to various programs -- i.e. for machine-readability.
* CSKV has the same benefits, at the cost of column names appearing on each row. The chief advantage of CSKV is for heterogeneous data.  Namely, I can print different schema lines interleaved -- a=1,b=2,c=3 on one line, and x=7,y=9 on another -- then pipe to grep, sort, etc. This is very handy in log files.
* I prefer horizontal format for viewing not-too-wide tables.
* I prefer vertical format for viewing the top few columns of very wide tables.

Converters include `c2h`, `c2v`, `h2c`, `h2v`, `v2c`, `v2h`, `c2kv`, `kv2c`,
`kv2h`, `kv2v`.  Depending on the data (e.g. data containing whitespace or
commas) they are not always invertible transformations.

Data transformers, on the other hand, don't just reshape; they make the data
different by adding or removing rows/colums, or aggregating (e.g. mean, count,
min, max). These scripts begin with `cs-` in deference to the `recs` tool suite
(http://search.cpan.org/~bernard/App-RecordStream-3.7.3/doc/RecordStreamStory.pod).

One might ask, why not just use recs?
* You can and should
* recs is Perl and JSON, with other formats layered on
* I prefer Ruby and CSV/CSKV
* These cs-tools are smaller, simpler, and just what I want.

John Kerl
2013-02-03
