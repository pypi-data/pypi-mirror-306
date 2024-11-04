ooverpunch
==========

Python wrapper around Rust [overpunch](https://crates.io/crates/overpunch).

Usage:

```
from decimal import Decimal

import ooverpunch

print(ooverpunch.extract("123N", 2))
print(ooverpunch.format(Decimal("29.45"), 2))

print(ooverpunch.convert_from_signed_format("123N", "s9(7)v99"))
print(ooverpunch.convert_to_signed_format(Decimal("29.45"), "s9(7)v99"))
```
