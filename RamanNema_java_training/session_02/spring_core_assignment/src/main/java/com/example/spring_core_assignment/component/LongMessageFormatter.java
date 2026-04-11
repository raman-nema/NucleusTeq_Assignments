package com.example.spring_core_assignment.component;

import com.example.spring_core_assignment.component.MessageFormatter;
import org.springframework.stereotype.Component;

// Component for long message formatting
@Component("LONG")
public class LongMessageFormatter implements MessageFormatter {

    // Format message in detailed (long) style
    public String format() {
        return "This is a detailed long message format";
    }
}