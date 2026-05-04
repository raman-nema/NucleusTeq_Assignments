package com.example.Reimbursement_Portal.service.impl;

import com.example.Reimbursement_Portal.dto.Request.UserRequestDTO;
import com.example.Reimbursement_Portal.dto.Response.UserResponseDTO;
import com.example.Reimbursement_Portal.entity.User;
import com.example.Reimbursement_Portal.enums.Role;
import com.example.Reimbursement_Portal.exception.BadRequestException;
import com.example.Reimbursement_Portal.repository.UserRepository;
import com.example.Reimbursement_Portal.service.impl.UserServiceImpl;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

import java.util.Arrays;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

/**
 * Unit tests for UserServiceImpl.
 *
 * We use Mockito to "mock" (fake) the database interactions.
 * This means we don't need a real database to run these tests!
 *
 * @Mock     = creates a fake version of the class
 * @InjectMocks = creates the real service and injects the fakes into it
 */
@ExtendWith(MockitoExtension.class)
class UserServiceImplTest {

    @Mock
    private UserRepository userRepository;

    @Mock
    private BCryptPasswordEncoder passwordEncoder;

    @InjectMocks
    private UserServiceImpl userService;

    // Helper: builds a basic employee user
    private User makeEmployee(Long id, String name, String email) {
        User u = new User();
        u.setId(id);
        u.setName(name);
        u.setEmail(email);
        u.setRole(Role.EMPLOYEE);
        u.setPassword("encoded_pass");
        return u;
    }

    // Helper: builds a manager user
    private User makeManager(Long id, String name) {
        User u = new User();
        u.setId(id);
        u.setName(name);
        u.setEmail(name.toLowerCase().replace(" ", "") + "@company.com");
        u.setRole(Role.MANAGER);
        u.setPassword("encoded_pass");
        return u;
    }

    // ─── createUser() tests ───────────────────────────────────────────────

    @Test
    void createUser_validEmployee_shouldSucceed() {
        // GIVEN: A valid employee request
        UserRequestDTO req = new UserRequestDTO();
        req.setName("Alice");
        req.setEmail("alice@company.com");
        req.setPassword("password123");
        req.setRole(Role.EMPLOYEE);

        User saved = makeEmployee(1L, "Alice", "alice@company.com");

        // GIVEN: Mock the database responses
        when(userRepository.existsByEmail("alice@company.com")).thenReturn(false);
        when(passwordEncoder.encode("password123")).thenReturn("hashed_pass");
        when(userRepository.save(any(User.class))).thenReturn(saved);

        // WHEN: We call createUser
        UserResponseDTO result = userService.createUser(req);

        // THEN: Result should have correct fields
        assertNotNull(result);
        assertEquals("Alice", result.getName());
        assertEquals(Role.EMPLOYEE, result.getRole());

        // THEN: verify save was called once
        verify(userRepository, times(1)).save(any(User.class));
    }

    @Test
    void createUser_duplicateEmail_shouldThrowBadRequestException() {
        // GIVEN: Email already exists in the database
        UserRequestDTO req = new UserRequestDTO();
        req.setName("Bob");
        req.setEmail("bob@company.com");
        req.setPassword("pass123");
        req.setRole(Role.EMPLOYEE);

        when(userRepository.existsByEmail("bob@company.com")).thenReturn(true);

        // WHEN + THEN: Should throw an exception
        BadRequestException ex = assertThrows(BadRequestException.class,
                () -> userService.createUser(req));

        assertEquals("Email already exists", ex.getMessage());
    }

    @Test
    void createUser_invalidEmailDomain_shouldThrowBadRequestException() {
        // GIVEN: Gmail email (not a company email)
        UserRequestDTO req = new UserRequestDTO();
        req.setName("Charlie");
        req.setEmail("charlie@gmail.com");
        req.setPassword("pass123");
        req.setRole(Role.EMPLOYEE);

        // WHEN + THEN: Should fail email domain validation
        BadRequestException ex = assertThrows(BadRequestException.class,
                () -> userService.createUser(req));

        assertEquals("Email must be @company.com", ex.getMessage());
    }

    @Test
    void createUser_employeeWithValidManager_shouldSucceed() {
        // GIVEN: A valid manager exists
        User manager = makeManager(10L, "Mandy Manager");

        UserRequestDTO req = new UserRequestDTO();
        req.setName("Dave");
        req.setEmail("dave@company.com");
        req.setPassword("pass123");
        req.setRole(Role.EMPLOYEE);
        req.setManagerId(10L);

        User saved = makeEmployee(2L, "Dave", "dave@company.com");
        saved.setManager(manager);

        when(userRepository.existsByEmail("dave@company.com")).thenReturn(false);
        when(passwordEncoder.encode("pass123")).thenReturn("hashed");
        when(userRepository.findById(10L)).thenReturn(Optional.of(manager));
        when(userRepository.save(any(User.class))).thenReturn(saved);

        // WHEN: Create employee with manager
        UserResponseDTO result = userService.createUser(req);

        // THEN: Should succeed
        assertNotNull(result);
        assertEquals("Dave", result.getName());
    }

    @Test
    void createUser_employeeWithNonManagerRole_shouldThrow() {
        // GIVEN: Trying to assign an ADMIN as the manager (not allowed)
        User adminAsManager = new User();
        adminAsManager.setId(99L);
        adminAsManager.setRole(Role.ADMIN); // ADMIN, not MANAGER!

        UserRequestDTO req = new UserRequestDTO();
        req.setName("Eve");
        req.setEmail("eve@company.com");
        req.setPassword("pass123");
        req.setRole(Role.EMPLOYEE);
        req.setManagerId(99L);

        when(userRepository.existsByEmail("eve@company.com")).thenReturn(false);
        when(passwordEncoder.encode("pass123")).thenReturn("hashed");
        when(userRepository.findById(99L)).thenReturn(Optional.of(adminAsManager));

        // WHEN + THEN: Should throw because admin can't be a manager
        BadRequestException ex = assertThrows(BadRequestException.class,
                () -> userService.createUser(req));

        assertTrue(ex.getMessage().contains("MANAGER role"));
    }

    @Test
    void createUser_managerNotFound_shouldThrow() {
        // GIVEN: Manager ID doesn't exist in the database
        UserRequestDTO req = new UserRequestDTO();
        req.setName("Frank");
        req.setEmail("frank@company.com");
        req.setPassword("pass123");
        req.setRole(Role.EMPLOYEE);
        req.setManagerId(999L); // Non-existent ID

        when(userRepository.existsByEmail("frank@company.com")).thenReturn(false);
        when(passwordEncoder.encode("pass123")).thenReturn("hashed");
        when(userRepository.findById(999L)).thenReturn(Optional.empty()); // Not found!

        // WHEN + THEN: Should throw
        assertThrows(BadRequestException.class, () -> userService.createUser(req));
    }

    // ─── getAllUsers() tests ───────────────────────────────────────────────

    @Test
    void getAllUsers_shouldReturnListOfDTOs() {
        // GIVEN: Two users in the database
        User u1 = makeEmployee(1L, "Alice", "alice@company.com");
        User u2 = makeEmployee(2L, "Bob", "bob@company.com");

        when(userRepository.findAll()).thenReturn(Arrays.asList(u1, u2));

        // WHEN: Get all users
        List<UserResponseDTO> result = userService.getAllUsers();

        // THEN: Should return 2 users
        assertEquals(2, result.size());
    }

    @Test
    void getAllUsers_emptyDatabase_shouldReturnEmptyList() {
        when(userRepository.findAll()).thenReturn(List.of());

        List<UserResponseDTO> result = userService.getAllUsers();

        assertTrue(result.isEmpty());
    }

    // ─── getUserById() tests ───────────────────────────────────────────────

    @Test
    void getUserById_existingId_shouldReturnUser() {
        User user = makeEmployee(1L, "Alice", "alice@company.com");
        when(userRepository.findById(1L)).thenReturn(Optional.of(user));

        UserResponseDTO result = userService.getUserById(1L);

        assertEquals("Alice", result.getName());
    }

    @Test
    void getUserById_notFound_shouldThrow() {
        when(userRepository.findById(999L)).thenReturn(Optional.empty());

        assertThrows(BadRequestException.class, () -> userService.getUserById(999L));
    }

    // ─── getEmployeesByManager() tests ────────────────────────────────────

    @Test
    void getEmployeesByManager_validManager_shouldReturnEmployees() {
        User emp = makeEmployee(1L, "Alice", "alice@company.com");

        when(userRepository.existsById(10L)).thenReturn(true);
        when(userRepository.findByManagerId(10L)).thenReturn(List.of(emp));

        List<UserResponseDTO> result = userService.getEmployeesByManager(10L);

        assertEquals(1, result.size());
    }

    @Test
    void getEmployeesByManager_managerNotFound_shouldThrow() {
        when(userRepository.existsById(999L)).thenReturn(false);

        assertThrows(BadRequestException.class,
                () -> userService.getEmployeesByManager(999L));
    }

    // ─── deleteUser() tests ───────────────────────────────────────────────

    @Test
    void deleteUser_withNoEmployees_shouldSucceed() {
        User user = makeEmployee(1L, "Alice", "alice@company.com");

        when(userRepository.findById(1L)).thenReturn(Optional.of(user));
        when(userRepository.existsByManagerId(1L)).thenReturn(false);

        // WHEN: Delete the user — should NOT throw
        assertDoesNotThrow(() -> userService.deleteUser(1L));

        // THEN: verify delete was called
        verify(userRepository, times(1)).delete(user);
    }

    @Test
    void deleteUser_managerWithEmployees_shouldThrow() {
        User manager = makeManager(10L, "Bob Manager");

        when(userRepository.findById(10L)).thenReturn(Optional.of(manager));
        when(userRepository.existsByManagerId(10L)).thenReturn(true); // has employees!

        BadRequestException ex = assertThrows(BadRequestException.class,
                () -> userService.deleteUser(10L));

        assertTrue(ex.getMessage().contains("Cannot delete manager"));

        // THEN: Delete should NOT have been called
        verify(userRepository, never()).delete(any());
    }

    @Test
    void deleteUser_notFound_shouldThrow() {
        when(userRepository.findById(999L)).thenReturn(Optional.empty());

        assertThrows(BadRequestException.class, () -> userService.deleteUser(999L));
    }
}