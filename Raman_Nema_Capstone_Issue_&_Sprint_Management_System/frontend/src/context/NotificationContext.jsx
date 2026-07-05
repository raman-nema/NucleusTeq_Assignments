import { useEffect, useState } from "react";
import NotificationContext from "./notification-context";
import "../styles/ToastMessage.css";

export function NotificationProvider({ children }) {
  const [notification, setNotification] = useState(null);

  function showNotification(message, type = "success") {
    setNotification({
      message,
      type,
    });
  }

  useEffect(() => {
    if (!notification) return undefined;

    const timerId = window.setTimeout(() => {
      setNotification(null);
    }, 3000);

    return () => window.clearTimeout(timerId);
  }, [notification]);

  return (
    <NotificationContext.Provider value={{ showNotification }}>
      {children}

      {notification && (
        <div className={`toast-message toast-${notification.type}`}>
          {notification.message}
        </div>
      )}
    </NotificationContext.Provider>
  );
}
