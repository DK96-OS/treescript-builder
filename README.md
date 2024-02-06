# Treebuilder
Script for Building File Trees

## File Tree Builder
Execute the File Tree Builder with the `ftb` command.
- Creates Files and Directories
- Default Input Reader + Data Arguments
- Data Directory

## File Tree Remover
Execute the File Tree Remover with the `ftr` command.
- Removes Files and Empty Directories
- Default Input Reader
- Data Directory

## Default Input Reader
The Default Input Reader processes one line at a time and calculates a node's depth in the tree, it's name, whether it is a directory, and finally, returns any data argument.

## Builder Data Feature
The Builder provides one additional feature that goes beyond creation of the File Tree. This feature enables Files to be created with data inserted immediately.

### Input Data Argument
The Data Argument specifies what will be inserted into the file that is created. The Data Argument is provided in the Input File, immediately after the File Name (separated by a space). There are two types of Data Arguments:
- Data Label
- Data Content

### Builder Data Label
A `Data Label` is a link to Text content that will be inserted into the file. This Data Label is the name of a File in the Data Directory, containing the Data to insert.

### Builder Data Content
A `Data Content` is Text or other information written directly in the Tree Node Structure Input file. To distinguish `Data Content` from a `Data Label`, the Content must begin with a special character.

Considering that file names should not start with a star character, this is the special char that will be used by the Default Input Reader.

## Remover Data Feature
The Remover provides an additional feature beyond the removal of files in the Tree. This feature enables Files to be saved to a Data Directory when they are removed. Rather than destroying the file data, it is moved to a new directory.

### Remover Discard Feature
By default, if a Data Directory is provided to the Remover, all Files will be moved into the Data Directory. To prevent a File from being moved, add the star character after the file name (separated by a space). The Star indicates that the File will be discarded.