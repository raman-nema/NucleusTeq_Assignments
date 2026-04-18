package com.example.todo_application.client;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

// Handles notification-related operations (acts as a helper/client layer)
@Component
public class NotificationServiceClient {

    // Logger used to track notification activity
    private static final Logger logger = LoggerFactory.getLogger(NotificationServiceClient.class);

    // Sends a notification (currently logs message, can be extended to real services like Email/SMS)
    public void sendNotification(String message) {
        logger.info("Notification sent: {}", message);
    }
}