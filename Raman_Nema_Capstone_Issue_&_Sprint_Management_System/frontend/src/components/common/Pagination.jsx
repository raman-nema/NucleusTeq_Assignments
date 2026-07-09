import Button from "./Button";

function Pagination({ pagination, onPageChange, disabled = false }) {
  if (!pagination || pagination.total_pages <= 1) {
    return null;
  }

  const hasPrevious = pagination.page > 1;
  const hasNext = pagination.page < pagination.total_pages;

  return (
    <div className="pagination-bar">
      <Button
        text="Previous"
        className="btn-muted"
        disabled={disabled || !hasPrevious}
        onClick={() => onPageChange(pagination.page - 1)}
      />

      <span className="pagination-summary">
        Page {pagination.page} of {pagination.total_pages}
      </span>

      <Button
        text="Next"
        className="btn-muted"
        disabled={disabled || !hasNext}
        onClick={() => onPageChange(pagination.page + 1)}
      />
    </div>
  );
}

export default Pagination;
