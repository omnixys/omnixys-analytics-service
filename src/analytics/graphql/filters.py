from datetime import date
from typing import Optional

import strawberry


@strawberry.input
class KpiFilter:
    year: Optional[int] = None
    month: Optional[int] = None
    from_date: Optional[date] = None
    to_date: Optional[date] = None
