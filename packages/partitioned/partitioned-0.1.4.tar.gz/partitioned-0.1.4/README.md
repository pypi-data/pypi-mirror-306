The `partitioned` package is a simple Python script to check if a sequence of lines is partitioned (all duplicate lines are sequential). 

Example of partitioned lines (where `partitioned` exits 0):
WORLD
WORLD
HELLO
HELLO

Note the above are not sorted, only partitioned! The `partitioned` tool does not detect if its input is sorted.

Example of unpartitioned lines (where `partitioned` exits 1):
HELLO
WORLD
HELLO
WORLD


The original motive for `partitioned` was for bioinformatics, specifically to determine if a .sam/.bam file was partitioned by readID, permitting a time-consuming sort by name that is usually unnecessary. An example of how it can be used for this is:

`samtools view demo.bam | awk -F'\\t' '{ print \$1 }' | partitioned && echo "demo.bam is partitioned by readID" || echo "demo.bam is not partitioned by readID"`

Details:
+ `partitioned` exits 0 (success) if the file is partitioned, 1 otherwise.
+ It uses a temporary SQLite3 database cache previously seen lines. This starts primarily in memory and spills to disk if necessary and is cleaned up automatically when the command terminates.
+ It can also read from a file with `-i` (streams from stdin if unspecified).
+ Pragmas can be set with `--pragmas` as a space-separated list.
+ The number of lines read in at once is configurable with `--chunk-size` (default is 1 million lines).


