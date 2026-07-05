from math import ceil

from fastapi import Query
from pydantic import BaseModel


DEFAULT_PAGE = 1
DEFAULT_LIMIT = 10  # Change this number to alter how many records appear per page.
MAX_LIMIT = 100


class PaginationParams(BaseModel):
    """Validated pagination request values."""

    page: int = DEFAULT_PAGE
    limit: int = DEFAULT_LIMIT

    @property
    def skip(self):
        """Return the number of records to skip."""

        return (self.page - 1) * self.limit


class PaginationMeta(BaseModel):
    """Common pagination metadata returned by list APIs."""

    page: int
    limit: int
    total: int
    total_pages: int
    has_next: bool
    has_previous: bool


def get_pagination_params(
    page: int = Query(DEFAULT_PAGE, ge=1),
    limit: int = Query(DEFAULT_LIMIT, ge=1, le=MAX_LIMIT),
):
    """Read common pagination query parameters."""

    return PaginationParams(
        page=page,
        limit=limit,
    )


def build_pagination_meta(total: int, params: PaginationParams):
    """Build pagination metadata for a list response."""

    total_pages = ceil(total / params.limit) if total else 0

    return PaginationMeta(
        page=params.page,
        limit=params.limit,
        total=total,
        total_pages=total_pages,
        has_next=params.page < total_pages,
        has_previous=params.page > 1 and total_pages > 0,
    )


def apply_pagination(cursor, params: PaginationParams):
    """Apply pagination to a Mongo cursor."""

    return cursor.skip(params.skip).limit(params.limit)
