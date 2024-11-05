# Gmine
This program simulates the `where` expression in SQL using pandas.

The program filters data in a csv file based on if certain texts exist in some columns.
For example, one may want to find the data where the column 'details of the story' contains the words 'cat' and 'dog', but not 'wolf'.
One may use the programme as follows:

    python -m gmine my_data.csv -c "details of the story" " ( cat and dog ) and ( not wolf )"

The spaces between parenthesis and words are crucial.
The output of the programme is a file called `my_data_filtered.csv` which only holds data that satisfy the condition.
Alternatively, if one want to specify a custom out put file name, one can use the `-o` flag followed by the output file name.
## Basic usage
    python -m gmine [-c COLUMN-NAME] [-o OUTPUT-FILE-NAME] <path_to_file> <cnf> 

If `-c` flag is not used, the default column name is `Report Details/Describe the event that happened`.
One may also write the command line argument in to a text file,

```text
# my_options.txt

my_data.csv
-c "fruit catagory"
" banana and ( not apple ) "
-o "haha.csv"
```

and simply type

    python3 -m gmine @my_options.txt




    


    