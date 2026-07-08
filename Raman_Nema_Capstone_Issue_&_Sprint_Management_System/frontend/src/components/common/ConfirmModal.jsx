import Button from "./Button";

function ConfirmModal({
  title,
  message,
  confirmText = "Confirm",
  cancelText = "Cancel",
  onConfirm,
  onCancel,
}) {
  return (
    <div className="modal-backdrop" role="presentation">
      <div
        className="confirm-modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="confirm-modal-title"
      >
        <h2 id="confirm-modal-title">{title}</h2>
        <p>{message}</p>

        <div className="confirm-modal-actions">
          <Button
            text={cancelText}
            className="btn-muted"
            onClick={onCancel}
          />
          <Button
            text={confirmText}
            className="btn-danger"
            onClick={onConfirm}
          />
        </div>
      </div>
    </div>
  );
}

export default ConfirmModal;
