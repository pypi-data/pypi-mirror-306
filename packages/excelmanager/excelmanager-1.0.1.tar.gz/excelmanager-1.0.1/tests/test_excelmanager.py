import os
from collections import OrderedDict
from typing import Any, Sequence

import openpyxl

import excelmanager

test_file = "tests/data/read.xlsx"
test_file_sheet = "Sheet1"


def test_reads_sheet_as_ordered_dicts():
    data = excelmanager.read_file_sheet(test_file, test_file_sheet)

    assert data == [
        OrderedDict({"Tree": "Maple", "Leaf Color": "Red", "Height (cm)": 549}),
        OrderedDict({"Tree": "Oak", "Leaf Color": "Green", "Height (cm)": 783}),
        OrderedDict({"Tree": "Pine", "Leaf Color": "Green", "Height (cm)": 1204}),
    ]


def test_reads_sheet_as_ordered_dicts_without_headers():
    data = excelmanager.read_file_sheet(test_file, test_file_sheet, has_headers=False)

    assert data == [
        OrderedDict({1: "Tree", 2: "Leaf Color", 3: "Height (cm)"}),
        OrderedDict({1: "Maple", 2: "Red", 3: 549}),
        OrderedDict({1: "Oak", 2: "Green", 3: 783}),
        OrderedDict({1: "Pine", 2: "Green", 3: 1204}),
    ]


def test_reads_sheet_as_lists():
    data = excelmanager.read_file_sheet(test_file, test_file_sheet, "list")

    assert data == [
        ["Tree", "Leaf Color", "Height (cm)"],
        ["Maple", "Red", 549],
        ["Oak", "Green", 783],
        ["Pine", "Green", 1204],
    ]


def test_reads_sheet_as_tuples():
    data = excelmanager.read_file_sheet(test_file, test_file_sheet, "tuple")

    assert data == [
        ("Tree", "Leaf Color", "Height (cm)"),
        ("Maple", "Red", 549),
        ("Oak", "Green", 783),
        ("Pine", "Green", 1204),
    ]


def test_reads_from_specific_range():
    data = excelmanager.read_file_sheet(
        test_file, test_file_sheet, "list", False, ("B3", "C4")
    )

    assert data == [["Green", 783], ["Green", 1204]]


def test_writes_ordered_dicts():
    write_data = [
        OrderedDict({"Tree": "Maple", "Leaf Color": "Red", "Height (cm)": 549}),
        OrderedDict({"Tree": "Oak", "Leaf Color": "Green", "Height (cm)": 783}),
        OrderedDict({"Tree": "Pine", "Leaf Color": "Green", "Height (cm)": 1204}),
    ]
    expected_values = (
        ("Tree", "Leaf Color", "Height (cm)"),
        ("Maple", "Red", 549),
        ("Oak", "Green", 783),
        ("Pine", "Green", 1204),
    )
    file_name = "file1.xlsx"
    file_path = "tests/data"

    try:
        excelmanager.write_file_sheet(file_name, file_path, write_data)

        _validate_expected_values(file_path, file_name, expected_values)
    finally:
        try:
            os.unlink(os.path.join(file_path, file_name))
        except:
            pass


def test_writes_sequence():
    write_data = (
        ("Maple", "Red", 549),
        ("Oak", "Green", 783),
        ("Pine", "Green", 1204),
    )
    expected_values = write_data
    file_name = "file2.xlsx"
    file_path = "tests/data"

    try:
        excelmanager.write_file_sheet(file_name, file_path, write_data)

        _validate_expected_values(
            file_path, file_name, expected_values, bold_headers=False
        )
    finally:
        try:
            os.unlink(os.path.join(file_path, file_name))
        except:
            pass


def test_writes_sequence_with_headers():
    headers = ("Tree", "Leaf Color", "Height (cm)")
    write_data = (
        ("Maple", "Red", 549),
        ("Oak", "Green", 783),
        ("Pine", "Green", 1204),
    )
    expected_values = (
        ("Tree", "Leaf Color", "Height (cm)"),
        ("Maple", "Red", 549),
        ("Oak", "Green", 783),
        ("Pine", "Green", 1204),
    )
    file_name = "file3.xlsx"
    file_path = "tests/data"

    try:
        excelmanager.write_file_sheet(file_name, file_path, write_data, headers=headers)

        _validate_expected_values(file_path, file_name, expected_values)
    finally:
        try:
            os.unlink(os.path.join(file_path, file_name))
        except:
            pass


def test_writes_ordered_dicts_without_bolded_headers():
    write_data = [
        OrderedDict({"Tree": "Maple", "Leaf Color": "Red", "Height (cm)": 549}),
        OrderedDict({"Tree": "Oak", "Leaf Color": "Green", "Height (cm)": 783}),
        OrderedDict({"Tree": "Pine", "Leaf Color": "Green", "Height (cm)": 1204}),
    ]
    expected_values = (
        ("Tree", "Leaf Color", "Height (cm)"),
        ("Maple", "Red", 549),
        ("Oak", "Green", 783),
        ("Pine", "Green", 1204),
    )
    file_name = "file1.xlsx"
    file_path = "tests/data"

    try:
        excelmanager.write_file_sheet(
            file_name, file_path, write_data, bold_headers=False
        )

        _validate_expected_values(
            file_path, file_name, expected_values, bold_headers=False
        )
    finally:
        try:
            os.unlink(os.path.join(file_path, file_name))
        except:
            pass


def _validate_expected_values(
    file_path: str,
    file_name: str,
    expected_values: Sequence[Sequence[Any]],
    bold_headers=True,
):
    workbook = openpyxl.load_workbook(os.path.join(file_path, file_name))
    sheet = workbook["Sheet"]
    write_data = sheet[sheet.dimensions]

    for i, row in enumerate(write_data):
        for j, cell in enumerate(row):
            assert cell.value == expected_values[i][j]

            if i == 0 and bold_headers:
                assert cell.font.bold == True
            elif i == 0:
                assert cell.font.bold == False
