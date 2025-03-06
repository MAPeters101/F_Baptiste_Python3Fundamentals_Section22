'''
Question 1
Alongside this note book, four CSV files are specified (one is in fact a TSV
file).

For each file, load it using the CSV module, and find the smallest and largest
numbers in the data.

All these files contain just lists of numbers - with the exception of a
possible header row

Question 2
Given this data structure consisting of a list of dictionaries, write a
function that will write this data out to a file, where the column headers (in
the first row) are based on the dictionary keys, and the values are flattened
out to one row per dictionary (under the corresponding column header).

Note that not all dictionaries contain all the same keys, nor are the keys
necessarily in the same order when present.

For "missing" values, your function should just write an empty string.

For example, given this data:

data = [
    {'a': '1_a', 'b': '1_b', 'c': '1_c'},
    {'c': '2_c', 'd': '2_d'},
    {'a': '3_a', 'c': '3_c', 'e': '3_e'}
]
Your output file should look like this:
a,b,c,d,e
1_a,1_b,1_c,,,
,,2_c,2_d,
3_a,,3_c,,3_e
The order of the columns and rows is not important - as long as they match up
with respective column headers.
'''