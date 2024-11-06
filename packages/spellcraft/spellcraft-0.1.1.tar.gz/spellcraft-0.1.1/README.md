# PySpellCraft

[![PyPI version](https://img.shields.io/pypi/v/spellcraft.svg)](https://pypi.org/project/spellcraft/)
[![Python versions](https://img.shields.io/pypi/pyversions/spellcraft.svg)](https://pypi.org/project/spellcraft/)
[![Docs Status](https://github.com/rnag/spellcraft/actions/workflows/docs.yml/badge.svg)](https://ritviknag.com/spellcraft/)
[![Build Status](https://github.com/rnag/spellcraft/actions/workflows/build-and-release.yml/badge.svg)](https://github.com/rnag/spellcraft/actions/workflows/build-and-release.yml)
[![License](https://img.shields.io/pypi/l/spellcraft.svg)](https://github.com/rnag/spellcraft/blob/main/LICENSE)

<!-- [![Coverage Status](https://coveralls.io/repos/github/rnag/spellcraft/badge.svg?branch=main)](https://coveralls.io/github/rnag/spellcraft?branch=main) -->
<!-- [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) -->

**SpellCraft** is a helper library that contains useful functions and "spells", primarily designed for use by [Dataclass Wizard].

[Read the documentation.]

[Read the documentation.]: https://ritviknag.com/spellcraft/
[Dataclass Wizard]: https://dataclass-wizard.readthedocs.io

## Installation

```
pip install spellcraft
```

> [!NOTE]
> Requires Python >= 3.9.

## Example

```python
>>> from spellcraft import snake
>>> snake("We carry a new world here, in our hearts.")
'we_carry_a_new_world_here_in_our_hearts'
```

## Development

### Setup

1. Activate a virtual environment:

```sh
python -m venv .venv
source .venv/bin/activate
```

2. Install dev dependencies:

```
pip install .[dev]
```

### Testing

1. Run `maturin develop` to compile the Rust code.
2. Run `make fmt`, `make lint`, and `make test`.

## License

`spellcraft` is distributed under the terms of the MIT License.

See the LICENSE file for full details.

> Copyright (c) 2015 The Rust Project Developers<br>
> Copyright (c) 2022 Kevin Heavey<br>
> Copyright (c) 2024 Ritvik Nag
