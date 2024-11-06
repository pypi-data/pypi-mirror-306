# About
hg2-item-parser is a Python package for parsing [Houkai Gakuen 2](https://houkai2nd.miraheze.org/wiki/Houkai_Gakuen_2_Wiki) items data

## Installation
### From PyPi
```shell
pip install hg2-item-parser
```

## Usage
To get help, type `--help` with any command or even package

### Check
To print any item to the console, use:

```shell
hg2-item-parser check item_id               # Prints item using ./extracted/ as data
hg2-item-parser check item_id path/to/data  # Prints item using path/to/data as data
```

### Parse
To parse any item to the file, use:

```shell
hg2-item-parser parse item_id                           # Parses item to ./parsed/items.txt using ./extracted/ as data
hg2-item-parser parse item_id path/to/dir               # Parses item to path/to/dir/items.txt using ./extracted/ as data
hg2-item-parser parse item_id path/to/dir path/to/data  # Parses item to path/to/dir/items.txt using path/to/data as data
```

### Multiple parse
To parse multiple items to the file, use:

```shell
hg2-item-parser parse-from-to item_id1 item_id2                           # Parses items in range to ./parsed/items.txt using ./extracted/ as data
hg2-item-parser parse-from-to item_id1 item_id2 path/to/dir               # Parses items in range to path/to/dir/items.txt using ./extracted/ as data
hg2-item-parser parse-from-to item_id1 item_id2 path/to/dir path/to/data  # Parses items in range to path/to/dir/items.txt using path/to/data as data
```