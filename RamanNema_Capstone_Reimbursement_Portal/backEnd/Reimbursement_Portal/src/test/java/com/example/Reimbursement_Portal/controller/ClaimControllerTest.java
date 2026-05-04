package com.example.Reimbursement_Portal.controller;

import com.example.Reimbursement_Portal.dto.Request.ClaimActionRequestDTO;
import com.example.Reimbursement_Portal.dto.Response.ClaimResponseDTO;
import com.example.Reimbursement_Portal.service.impl.ClaimServiceImpl;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;   // ✅ FIXED
import static org.mockito.Mockito.*;

class ClaimControllerTest {

    //  TEST 1: Get All Claims
    @Test
    void testGetAllClaims() {

        ClaimServiceImpl service = mock(ClaimServiceImpl.class);
        ClaimController controller = new ClaimController(service);

        controller.getAllClaims();

        verify(service).getAllClaims();
    }

    //  TEST 2: Get Claims By Employee
    @Test
    void testGetClaimsByEmployee() {

        ClaimServiceImpl service = mock(ClaimServiceImpl.class);
        ClaimController controller = new ClaimController(service);

        ClaimResponseDTO claim = new ClaimResponseDTO(); //  NO constructor
        claim.setAmount(500.0);

        when(service.getClaimsByEmployee(1L))
                .thenReturn(java.util.List.of(claim));

        var response = controller.getClaimsByEmployee(1L);

        //  SAFE ASSERTIONS (fix NPE warning)
        assertNotNull(response);
        assertEquals(200, response.getStatusCode().value());
        assertNotNull(response.getBody());
        assertNotNull(response.getBody().getData());
        assertEquals(1, response.getBody().getData().size());

        verify(service).getClaimsByEmployee(1L);
    }

    //  TEST 3: Take Action
    @Test
    void testTakeAction() {

        ClaimServiceImpl service = mock(ClaimServiceImpl.class);
        ClaimController controller = new ClaimController(service);

        ClaimActionRequestDTO request = new ClaimActionRequestDTO();
        request.setStatus(
                com.example.Reimbursement_Portal.enums.ClaimStatus.APPROVED
        );

        ClaimResponseDTO responseDTO = new ClaimResponseDTO(); //  NO constructor
        responseDTO.setStatus(
                com.example.Reimbursement_Portal.enums.ClaimStatus.APPROVED
        );

        when(service.takeAction(anyLong(), anyLong(), any()))
                .thenReturn(responseDTO);

        var response = controller.takeAction(1L, 2L, request);

        // SAFE ASSERTIONS
        assertNotNull(response);
        assertEquals(200, response.getStatusCode().value());
        assertNotNull(response.getBody());
        assertNotNull(response.getBody().getData());
        assertEquals("APPROVED",
                response.getBody().getData().getStatus().name());

        verify(service).takeAction(anyLong(), anyLong(), any());
    }
    @Test
    void testTakeAction_NullStatus() {

        ClaimServiceImpl service = mock(ClaimServiceImpl.class);
        ClaimController controller = new ClaimController(service);

        ClaimActionRequestDTO request = new ClaimActionRequestDTO();
        request.setStatus(null); //  invalid case

        when(service.takeAction(anyLong(), anyLong(), any()))
                .thenThrow(new RuntimeException("Invalid"));

        assertThrows(RuntimeException.class,
                () -> controller.takeAction(1L, 2L, request));
    }
}