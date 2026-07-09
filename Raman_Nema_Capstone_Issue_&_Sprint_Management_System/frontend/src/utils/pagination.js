export const DEFAULT_PAGE = 1;
export const DEFAULT_PAGE_SIZE = 6; // Change this number to alter how many records appear per page.

export function getDefaultPagination() {
  return {
    page: DEFAULT_PAGE,
    limit: DEFAULT_PAGE_SIZE,
    total: 0,
    total_pages: 0,
  };
}

export function buildPaginationParams(page, limit = DEFAULT_PAGE_SIZE) {
  return {
    page,
    limit,
  };
}
