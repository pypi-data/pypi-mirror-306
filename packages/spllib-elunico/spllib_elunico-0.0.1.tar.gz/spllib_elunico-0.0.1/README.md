# SPLLib

#### This is bespoke to another one of my projects and is currently very alpha-software. I intend to improve it

Library for interacting with `.spl` files. A format created by me

SPL files stands for special property list


## Format

An SPL file can be written according to the following specification
  -  any line matching "^\s*#" is ignored
  -  Anything matching "#\s*\n" is ignored
  -  all other lines should begin with a tag name
  -  then an equal sign with optional whitespace on either side
  -  then either (1) a comma separated list of tags or (2) an asterisk

In general, you can have comments starting with # until the new line

Keys are to the left of the `=` and values are to the right. Keys and values can contain any character except neither can contain `=`, `\n`, nor `\r\n`