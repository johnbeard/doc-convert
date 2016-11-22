# doc-devhelp

This is a way to add devhelp indexes to other projects' documentation.

This can be done in a variety of ways, from manually scrubbing through the
documentation and building a devhelp file, or using XSLT to transform some
existing documentation XML index.

## Converters

Each library might have more than one way to convert its documentation.

### XSL

XSL converters are used when a good XML source of documentation metadata exists
and can be usefully converted with `xsltproc`.

For XSL converters, they normally expect parameters:

- `book_title`: the human-readable title, e.g. "FooLib 5.6 Reference Manual"
- `book_name`: the devhelp book name, e.g. "foo-doc-en"
- `book_base`: the root of the documentation tree, usually under `/usr/share/doc`
  or similar

## Available converters

### JUCE

- JUCE project: https://github.com/julianstorer/JUCE

An XSL converter is provided that converts Doxygen XML into devhelp2 format. The
JUCE Doxyfile doesn't output XML by default, so it needs to be turned on. Then
run the XSL file on the `xml/index.xml` file that is produced.
