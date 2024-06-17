# sub

`sub` is a simple command line tool that allows you to substitute text between files.

## Installation

Save the script somewhere in your PATH. There are no dependencies beyond Python.

## Motivation

For some simple websites, I've been working directly in HTML and CSS, with no static site generator or build processes. This is convenient except when I need to make a change that affects multiple files, typically for a header or footer, copyright notice, or similar. The `sub` script lets me label sections of files and reuse them elsewhere. The key is that the labeling is done within the file's native comment syntax, so there is no separate input/output.

## Usage

Mark the beginning and end of a section with comments denoted with `@` and a label, and then reuse them in a similar manner with `#`:

```html
...
<!-- @foo -->
This will be captured and named "foo".
<!-- end -->

...
<!-- #foo -->
This will be replaced with the contents of "foo".
<!-- end -->
```

The script is run as:

```sh
sub [-r] [dir]  # -r recursively process files
```

## Notes

- The processing flow is: 1) look for labeled secions across all files, 2) replace referenced sections across all files. You can reference any section anywhere, even within the same file, before the defintion, etc.
- Files are edited in place.
- HTML and CSS are supported, but it could easily be extended to other formats.
- There are checks for duplicate or unknown labels, but overall it is pretty basic without a lot of extra validation. Nesting things and forgetting to close tags will cause surprises. I played around with nested definitions, but it added a lot of complexity for what is likely a rare use case.
- The goals for this are simple, and for more complex tasks you should look at a more full-featured templating system or static site generator.
