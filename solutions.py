'''
Question 1
Alongside this note book, four CSV files are specified (one is in fact a TSV file).

For each file, load it using the CSV module, and find the smallest and largest numbers in the data.

All these files contain just lists of numbers - with the exception of a possible header row

Solution
The first file file1.csv looks like a standard CSV file:

import csv
with open('file1.csv') as f:
    for row in f:
        print(row.strip())
col1,col2,col3
10,20,30
30,40,50
60,70,80
We should be able to load this up without any issues using a csv reader:

with open('file1.csv') as f:
    reader = csv.reader(f)
    # skip header row
    next(reader)
    # load remaining data
    data = list(reader)
print(data)
[['10', '20', '30'], ['30', '40', '50'], ['60', '70', '80']]
We now have a list of lists, and we need to recover the min and max of the numbers in those lists. Notice how the data is actually containing strings, not numbers, so we need to fix that first.

with open('file1.csv') as f:
    reader = csv.reader(f)
    # skip header row
    next(reader)
    # load remaining data
    data = list(reader)
data = [[float(x) for x in row] for row in data]
print(data)
[[10.0, 20.0, 30.0], [30.0, 40.0, 50.0], [60.0, 70.0, 80.0]]
Since we'll need to perform this calculation multiple times (and all our csv files contain just rows of numbers), we'll make a function that can do this for us repeatedly:

def min_max(data):
    row_maxes = [max(row) for row in data]
    row_mins = [min(row) for row in data]

    max_ = max(row_maxes)
    min_ = min(row_mins)
    return min_, max_
min_max(data)
(10.0, 80.0)
Next we'll look at file2.csv

with open('file2.csv') as f:
    for row in f:
        print(row.strip())
1, 3.14, 500
20, 1, -2
-1.1, -2.2, -3.3
So this one has no header row.

with open('file2.csv') as f:
    reader = csv.reader(f)
    # load remaining data
    data = list(reader)
data = [[float(x) for x in row] for row in data]
print(data)
[[1.0, 3.14, 500.0], [20.0, 1.0, -2.0], [-1.1, -2.2, -3.3]]
And now we can just call our function for min/max:

min_max(data)
(-3.3, 500.0)
Let's move on to the third file:

with open('file3.tsv') as f:
    for row in f:
        print(row.strip())
col1	col2	col3
10	20	30
40	50	60
100	200	300
This one contains a header row, and tab separated values.

If we just try to load it using the default settings for the CSV reader, we won't end up with what we need.

with open('file3.tsv') as f:
    reader = csv.reader(f)
    next(reader)  # skip header row
    # load remaining data
    data = list(reader)
data
[['10\t20\t30'], ['40\t50\t60'], ['100\t200\t300']]
As you can see, the items were not split on the \t character. So, we just need to instruct the CSV reader that \t characters are the item separators using the delimiter argument:

with open('file3.tsv') as f:
    reader = csv.reader(f, delimiter='\t')
    next(reader)  # skip header row
    # load remaining data
    data = list(reader)
data
[['10', '20', '30'], ['40', '50', '60'], ['100', '200', '300']]
We still need our numeroic conversion to happen:

data = [[float(x) for x in row] for row in data]
data
[[10.0, 20.0, 30.0], [40.0, 50.0, 60.0], [100.0, 200.0, 300.0]]
And now we can find the min/max:

min_max(data)
(10.0, 300.0)
Finally,let's look at the last file, file4.csv:

with open('file4.csv') as f:
    for row in f:
        print(row.strip())
-col1-|-col2-|-col3-
10|20|30
-3.14-|-25-|-100-
---3.14-|20|-30-
Here you can see that we have a header row, the item separators are the pipe character |, and the "quotechar" is actually - - weird, but we can handle that!

with open('file4.csv') as f:
    reader = csv.reader(f, delimiter='|', quotechar='-')
    next(reader)  # skip header row
    # load remaining data
    data = list(reader)
data
[['10', '20', '30'], ['3.14', '25', '100'], ['-3.14', '20', '30']]
We can then make all these items into numbers and find the min/max:

data = [[float(x) for x in row] for row in data]
min_max(data)
(-3.14, 100.0)
You'll notice that the way we handle all these files were as follows:

Assumptions:

assume that all rowes contain numeric values
except, possibly, for initial header row
Approach:

specify whether we skip header row or not
specify delimiter and quotechar optionally
load data
convert all items to floats
find min_max
We could actually package all this up into a single function, as long as we allow passing arguments such as delimiter and quotechar to, ultimately, the csv reader.

def find_min_max(f_name, has_header_row, **kwargs):
    # **kwargs will be passed straight on to the csv reader
    with open(f_name) as f:
        reader = csv.reader(f, **kwargs)
        if has_header_row:
            next(reader)  # skip header row
        # load remaining data
        data = list(reader)
    data = [[float(x) for x in row] for row in data]
    return min_max(data)
We can simplify this a bit:

def find_min_max(f_name, has_header_row=True, **kwargs):
    with open(f_name) as f:
        reader = csv.reader(f, **kwargs)
        if has_header_row:
            next(reader)  # skip header row
        # load remaining data
        data = [[float(x) for x in row] for row in reader]
    return min_max(data)
And then we can call it this way:

find_min_max('file1.csv')
(10.0, 80.0)
find_min_max('file2.csv', has_header_row=False)
(-3.3, 500.0)
find_min_max('file3.tsv', delimiter='\t')
(10.0, 300.0)
find_min_max('file4.csv', delimiter='|', quotechar='-')
(-3.14, 100.0)
Question 2
Given this data structure consisting of a list of dictionaries, write a function that will write this data out to a file, where the column headers (in the first row) are based on the dictionary keys, and the values are flattened out to one row per dictionary (under the corresponding column header).

Note that not all dictionaries contain all the same keys, nor are the keys necessarily in the same order when present.

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
The order of the columns and rows is not important - as long as they match up with respective column headers.

Solution
First thing is we need to get the set of all the keys in all the dictionaries:

keys = {}
for d in data:
    keys = keys | d.keys()
keys
{'a', 'b', 'c', 'd', 'e'}
Now we can loop through each dictionary and create a list of all the values for the corresponding keys.

Before we do that however, we want to be sure that the keys will be in the same order, and using a set for the keys doers not guarantee order, so we'll make that into a list first:

keys = list(keys)
keys
['a', 'c', 'd', 'e', 'b']
Now we can go ahead and create our list of lists - one list per row, and one value (possibly an empty string), for each item in the row.

flattened = []
for d in data:
    row_list = []
    for key in keys:
        row_list.append(d.get(key, ''))
    flattened.append(row_list)

flattened
[['1_a', '1_c', '', '', '1_b'],
 ['', '2_c', '2_d', '', ''],
 ['3_a', '3_c', '', '3_e', '']]
We can probably use some comprehensions here, let's try it:

flattened = []
for d in data:
    row_list = [d.get(key, '') for key in keys]
    flattened.append(row_list)

flattened
[['1_a', '1_c', '', '', '1_b'],
 ['', '2_c', '2_d', '', ''],
 ['3_a', '3_c', '', '3_e', '']]
And one more!

flattened = [[d.get(key, '') for key in keys] for d in data]
flattened
[['1_a', '1_c', '', '', '1_b'],
 ['', '2_c', '2_d', '', ''],
 ['3_a', '3_c', '', '3_e', '']]
And now we could write this to a CSV file using the CSV writer method.

Let's go ahead and package all this up, including the CSV writing into a function:

def flatten_to_csv(data, out_file):
    keys = {}
    for d in data:
        keys = keys | d.keys()
    keys = list(keys)
    flattened = [[d.get(key, '') for key in keys] for d in data]

    with open(out_file, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(keys)
        for row in flattened:
            writer.writerow(row)
flatten_to_csv(data, 'test.csv')
'''