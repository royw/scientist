#!/usr/bin/env python
# coding=utf-8

"""
Split a RST file on sections

This script assumes the top heading uses before and after lines of equal signs while
the next heading level uses just after lines of equal signs.  For example::

    =====================    +
    title section heading    |
    =====================    |
                             |---> file00.rst
    ...                      |
                             +
    regular section          +
    ===============          |
                             |---> file01.rst
    ...                      |
                             +

Example Usage::

    bin/rst_split.py docs/file.rst

This will create docs/file directory.

Each section from docs/slides.rst will be extracted and written to file/fileNN.rst where NN is the section
index in the original file.

To use the generated files, you can included the sections in a toctree with the glob option set::

    .. toctree::
       :maxdepth: 2
       :glob:

       file/*


"""
import os
import sys
import re

__docformat__ = 'restructuredtext en'


TITLE_REGEX = r'(====+\n[^\n]+?\n====+\n)'
SECTION_REGEX = r'([^\n]+?\n====+\n)'

# base_dir is the directory where the source file, given as the command line argument, resides.
# base_name is the name of the source file without path and without extension.
# out_dir is the directory where the section files will be written.  It is named {base_dir}/{base_name}.

base_dir = os.path.dirname(os.path.abspath(sys.argv[1]))
base_name = os.path.splitext(os.path.basename(sys.argv[1]))[0]
out_dir = os.path.join(base_dir, base_name)
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

# file_index is the integer appended to the base_name for section files.  file_index is incremented for each section.
# current_file is the currently opened section file.

file_index = 0
current_file = None


def next_file():
    """
    :return: the file instance for the next section file to write.
    :rtype: file
    """

    # sets globals: current_file and file_index

    global current_file, file_index
    if current_file is not None:
        current_file.close()
        current_file = None
    file_name = "%s%02d.rst" % (base_name, file_index)
    current_file = open(os.path.join(out_dir, file_name), 'w')
    file_index += 1
    return current_file


def main():
    global current_file

    try:
        with open(sys.argv[1]) as in_file:
            source = in_file.read()
        out_file = None

        # split source file on titles
        parts = re.split(TITLE_REGEX, source, flags=re.MULTILINE)
        for part in parts:
            if re.match(TITLE_REGEX, part):
                # write title section
                out_file = next_file()
                out_file.write(part)
            else:
                # split title sections into regular sections
                sections = re.split(SECTION_REGEX, part, flags=re.MULTILINE)
                for section in sections:
                    if re.match(SECTION_REGEX, section):
                        # write regular section
                        out_file = next_file()
                        out_file.write(section)
                    else:
                        # write leftover, skip writing only whitespace sections.
                        if section.strip():
                            if out_file is None:
                                out_file = next_file()
                            out_file.write(section)

    except Exception as ex:
        print(str(ex))

    finally:
        # makes sure last section file is closed
        if current_file is not None:
            current_file.close()
            current_file = None


if __name__ == '__main__':
    main()
