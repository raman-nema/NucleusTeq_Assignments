package com.example.spring_core_assignment.component;

import org.springframework.stereotype.Component;

// Component for short message formatting
@Component("SHORT")
public class ShortMessageFormatter implements MessageFormatter {

    // Format message in short style
    public String format() {
        return "Short Message";
    }
}