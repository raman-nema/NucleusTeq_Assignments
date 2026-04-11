package com.example.spring_core_assignment.component;

import org.springframework.stereotype.Component;

// Component for handling notifications
@Component
public class NotificationComponent {

    // Send notification
    public String sendNotification() {
        return "Notification sent";
    }
}