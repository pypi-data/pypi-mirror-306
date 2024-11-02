from typing import TypeAlias, Optional

Integer: TypeAlias = int
Decimal: TypeAlias = float
Complex: TypeAlias = complex
Number: TypeAlias = Integer | Decimal | Complex
Irrational: TypeAlias = Number


# None types
Null: TypeAlias = Optional[None]
