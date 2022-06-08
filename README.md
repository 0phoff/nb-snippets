# Notebook Snippets
This repository contains a collection of files which can be loaded into a notebook to provide certain commonly used functionality.
It is catered to my own personal needs, but feel free to look around and copy stuff.


## Usage
The basic idea is to provide small self-sustained files that expose a few related functions.
You can then load that file by using the following command in a notebook cell, which will execute the file as if it was run as a cell in the notebook.

```python
%run path/to/file.py
```

If you ever want to share a notebook with someone who might not have these snippets, you can use the following command to export the file contents as a cell.

```python
%load path/to/file.py
```


## Why no package
The alternative to these snippets is to create a python package and install it locally (eg. in dev mode).  
While this is a clean solution, this means we need to reinstall the package in every environment and it needlessly pollutes your installs with a package only useful for notebooks.
Moreover, when developing packages, I have a tendency to over-engineer things and create complex import systems.  
By using these snippets, I force myself to create small, laser-focused scripts instead of an unmanageable behemoth of a package with unrelated content everywhere.


## Guidelines
A few guidelines I need to consider when writing these snippets:

- Import packages inside of your functions.  
  This is quite controversial, but the reasoning is that everything in the script gets exposed in the notebook (cluttering tab completion).
  By encapsulating my imports inside of the functions, I do not export those modules to the notebook.

- Do not group unrelated functionality in a single snippet file.  
  It is better to `%run` or `%load` multiple files if necessary, than to load a bunch of unused functions.

- Do not forget to add a docstring with *args* and *examples* sections.  
  When we `%run` a file, we do not see its contents, so having proper docstrings gives a much better developer experience.
