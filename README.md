# Scriic

[![Maintainability](https://api.codeclimate.com/v1/badges/895e7208b9dbb07fb8a0/maintainability)](https://codeclimate.com/github/AlphaMycelium/scriic/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/895e7208b9dbb07fb8a0/test_coverage)](https://codeclimate.com/github/AlphaMycelium/scriic/test_coverage)
[![Documentation Status](https://readthedocs.org/projects/scriic/badge/?version=latest)](https://scriic.readthedocs.io/en/latest/?badge=latest)


**For installation instructions, getting started and the Scriic syntax
reference, see [ReadTheDocs](https://scriic.readthedocs.io/en/latest/).**


Scriic is a mini programming language for generating detailed (and more often
than not, overcomplicated) instructions. Here's an example program:

```
HOWTO Type <text"> using <keyboard>

char = LETTERS [text]
  SUB ./look.scriic
  WITH [keyboard] AS thing
  GO

  key = DO Find the key on [keyboard] which displays [char"]

  SUB ./press_button.scriic
  WITH [key] AS button
  GO
END
```

At the time of writing, this generates 110 steps to type "hello world"!
