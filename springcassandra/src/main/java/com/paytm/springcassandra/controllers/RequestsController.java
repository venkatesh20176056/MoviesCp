package com.paytm.springcassandra.controllers;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.paytm.springcassandra.services.*;

import java.util.*;
import com.paytm.springcassandra.entities.*;

@RestController
public class RequestsController {
	
	private EmployeeService employeeService;
	
	@Autowired
	public RequestsController(EmployeeService employeeService) {
		this.employeeService = employeeService;	
	}
	
	@RequestMapping(value="/GetAllEmployeesDetails", method = RequestMethod.GET)
	public List<Employees> getAll()
	{
		return employeeService.GetAllEmployeeDetails();
	}
	
	@RequestMapping(value = "/GetEmployeeDetailsByID", method = RequestMethod.GET)
	public Optional<Employees>  getEmployeeDetailsByID(@RequestParam(value = "emp_code", required = true) int emp_code ){
		
		
		return employeeService.GetEmployeeByID(emp_code);
	}
	
}
