from math import ceil
from fastapi import Query
from pydantic import BaseModel

DEFAULT_PAGE = 1
DEFAULT_LIMIT = 10
MAX_LIMIT = 100

class PaginationParams(BaseModel):
    """Validated pagination query parameters."""

    page: int
    limit: int

    @property
    def skip(self) -> int:
        return (self.page - 1) * self.limit


class PaginationMeta(BaseModel):
    """Pagination metadata returned with list responses."""

    page: int
    limit: int
    total: int
    total_pages: int


def get_pagination_params(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
) -> PaginationParams:
    """Build pagination parameters from query params."""

    return PaginationParams(page=page, limit=limit)


def build_pagination_meta(total: int, params: PaginationParams) -> PaginationMeta:
    """Build response metadata for a paginated result set."""

    total_pages = ceil(total / params.limit) if total else 0

    return PaginationMeta(
        page=params.page,
        limit=params.limit,
        total=total,
        total_pages=total_pages,
    )


def apply_pagination(query, params: PaginationParams):
    """Apply pagination to a Mongo cursor."""

    return query.skip(params.skip).limit(params.limit)
