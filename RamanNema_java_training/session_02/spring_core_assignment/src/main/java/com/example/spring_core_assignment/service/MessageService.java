package com.example.spring_core_assignment.service;

import com.example.spring_core_assignment.component.MessageFormatter;
import org.springframework.stereotype.Service;

import java.util.Map;

// Service for selecting appropriate message formatter
@Service
public class MessageService {

    private final Map<String, MessageFormatter> formatterMap; // Available formatters

    // Constructor-based injection of all MessageFormatter beans
    public MessageService(Map<String, MessageFormatter> formatterMap) {
        this.formatterMap = formatterMap;
    }

    // Return formatted message based on type
    public String getMessage(String type) {
        MessageFormatter formatter = formatterMap.get(type);
        return formatter != null ? formatter.format() : "Invalid type";
    }
}