Format tabular data in various ways with explicitly defined columns
that can each have their own expected types, formatting and highlighting.

Features
========

-  Specify columns with data types / widths, formatting functions,
   null-value indicators and processing exception indicators.
-  Auto-sizing columns when presented with a full table of data.
-  Ability to format individual rows for output before all data has 
   been gathered.
-  Quick switching of output formats between tabular text, JSON,
   YAML & delimited fields.
-  Value highlighting rules: by ranges, trends, min/max and others.


Quick Start
===========

::

        # pip install vegetable first
        from vegetable import Table

        t = Table()
        t.column("Supplier")
        t.column("Cost", type=float)
        t.row(["Convenience store", 12.99])
        t.row(["Wholesaler", "10.29"])
        t.row(["Internet store", 11.56])
        t.row(["Dodgy pub geezer", 5.00])
        print(t)



Manual Installation From Repo
=============================

::

        $ git clone https://github.com/mousefad/python-vegetable vegetable
        $ cd vegetable
        $ python -m venv .
        $ . bin/activate
        $ pip install --upgrade pip
        $ pip install .
        $ export PYTHONPATH="$PYTHONPATH:$PWD"

To run `examples/network_traffic` you may also need to `pip install click`.


Complete Data Mode
------------------

Values can be added to a `Table()` instace directly row-by-row with `row()`. 
When `__str__()` is invoked, the whole table will be formatted and returned. 
An advantage of this approach is that column widths will be automatically 
re-sized if needed (for columns where `expand=True` was used on column 
creation).

The output format can also be easily switched:

::

        t = Table()
        t.column("Name")
        t.column("Hobby")
        t.row(["'Bob'", "Just having a whale of a time."])
        t.row(["Stang, "Monsterism."])
        print(t, end="\n\n")
        t.formatter = YamlFormat()
        print(t)


Line-by-Line Mode
-----------------

In applications where we want to print data as it is gathered, we can 
get string values for the table headers, separators and rows with 
`header_str()`, `separator_str()` `mast_head()` and `row_str(...)` 
functions:

::

        t = Table()
        t.column("Item Desc")
        t.column("Qty", type=int)
        print(t.mast_head())
        for desc, num in gather_data():
            print(t.row_str([desc, num]))


TODO
====

-  Better unit test coverage
-  Multi-column sorting


