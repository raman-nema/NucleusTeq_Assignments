import Button from "./Button";

function Pagination({ pagination, onPageChange, disabled = false }) {
  if (!pagination || pagination.total_pages <= 1) {
    return null;
  }

  return (
    <div className="pagination-bar">
      <Button
        text="Previous"
        className="btn-muted"
        disabled={disabled || !pagination.has_previous}
        onClick={() => onPageChange(pagination.page - 1)}
      />

      <span className="pagination-summary">
        Page {pagination.page} of {pagination.total_pages}
      </span>

      <Button
        text="Next"
        className="btn-muted"
        disabled={disabled || !pagination.has_next}
        onClick={() => onPageChange(pagination.page + 1)}
      />
    </div>
  );
}

export default Pagination;
