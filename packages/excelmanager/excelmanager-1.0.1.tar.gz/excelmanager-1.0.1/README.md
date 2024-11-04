# Introduction

`excelmanager` is a stripped-down wrapper around the `openpyxl` package. It exposes two very simple functions (`read_file_sheet` and `write_file_sheet`) that provide quick and easy ways to perform read/write operations against Excel files. This package is ideal for applications where the goal is to be able to quickly and easily get simple tabular data in and out of various Excel files without worrying about things like advanced formatting or charting.

# Installation

```
pip install excelmanager
```

# Usage

The `read_file_sheet` function allows data to be read back from a sheet in multiple formats.

```py
# Outputs a list of ordered dictionaries
results = excelmanager.read_file_sheet(
    "path/to/file.xlsx", "Sheet1", output_row_type="OrderedDict"
)

# Outputs a list of lists
results = excelmanager.read_file_sheet(
    "path/to/file.xlsx", "Sheet1", output_row_type="list"
)

# Outputs a list of tuples
results = excelmanager.read_file_sheet(
    "path/to/file.xlsx", "Sheet1", output_row_type="tuple"
)

# Reads data from a specific range
results = excelmanager.read_file_sheet(
    "path/to/file.xlsx", "Sheet1", range=("B3", "E12")
)
```

The `write_file_sheet` writes data to a specified Excel file and sheet. If the sheet or file don't yet exist, this function will create them.

```py
# Write from sequence data with specified headers
excelmanager.write_file_sheet(
    "output.xlsx",
    "path/to/output",
    (("Value1", "Value2", "Value3"), ("Value4", "Value5", "Value6")),
    headers=("Column1", "Column2", "Column3"),
)

# Write using OrderedDict data. Keys are used as headers unless an empty sequence ([]) is passed.
excelmanager.write_file_sheet(
    "output.xlsx",
    "path/to/output.xlsx",
    [
        OrderedDict({"Column1": "Value1", "Column2": "Value2", "Column3": "Value3"}),
        OrderedDict({"Column1": "Value4", "Column2": "Value5", "Column3": "Value6"}),
    ],
)
```