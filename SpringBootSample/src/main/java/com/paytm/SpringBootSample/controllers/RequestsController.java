package com.paytm.SpringBootSample.controllers;

import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestMapping;

import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.beans.factory.annotation.Autowired;


import com.paytm.SpringBootSample.services.*;

import java.util.*;



@RestController
public class RequestsController {
	
	private DisplayService ds;
	private AllEmployees allEmployees;
	private EmployeesUnderParticularDept employeesUnderParticularDept;
	private ManagerOfParticularDept managerOfParticularDept;
	private EmployeesUnderParticularManager employeesUnderParticularManager;
	private InsertNewEmployee insertNewEmployee;

	
	@Autowired
	public RequestsController(DisplayService ds, AllEmployees allEmployees, EmployeesUnderParticularDept employeesUnderParticularDept, ManagerOfParticularDept managerOfParticularDept, EmployeesUnderParticularManager employeesUnderParticularManager, InsertNewEmployee insertNewEmployee) {
		this.ds = ds;
		this.allEmployees = allEmployees;
		this.employeesUnderParticularDept = employeesUnderParticularDept;
		this.managerOfParticularDept = managerOfParticularDept;
		this.employeesUnderParticularManager = employeesUnderParticularManager;
		this.insertNewEmployee = insertNewEmployee;
	}
	
	@RequestMapping(method = RequestMethod.GET, value = "/getWelcomeNote") 
	public String getAllEmployees(@RequestParam(value = "name", required = true) String name) {
		return ds.welcomeNote(name);
	}
	
	@RequestMapping(method = RequestMethod.GET, value = "/getAll") 
	public List<Map<String, Object>> getAll() {
		
	    return allEmployees.getAll();
	}
	
	@RequestMapping(method = RequestMethod.GET, value = "/GetEmployeesUnderParticularDept") 
	public List<Map<String, Object>> getEmployeesUnderParticularDept(@RequestParam(value = "DepartmentID", required = true) String DepartmentID) {
		return employeesUnderParticularDept.getEmployeesUnderParticularDept(Integer.parseInt(DepartmentID));
	}
	
	@RequestMapping(method = RequestMethod.GET, value = "/GetManagerOfParticularDept") 
	public List<Map<String, Object>> getManagerOfParticularDept(@RequestParam(value = "DepartmentID", required = true) String DepartmentID) {
		return managerOfParticularDept.getManagerOfParticularDept(Integer.parseInt(DepartmentID));
	}
	
	@RequestMapping(method = RequestMethod.GET, value = "/GetEmployeesUnderParticularManager") 
	public List<Map<String, Object>> getEmployeesUnderParticularManager(@RequestParam(value = "name", required = true) String name) {
		return employeesUnderParticularManager.getEmployeesUnderParticularManager(name);
	}
	
	@RequestMapping(method = RequestMethod.GET, value = "/InsertNewEmployee") 
	public int InsertNewEmployeeInDB(@RequestParam(value = "name", required = true) String name, @RequestParam(value = "id", required = true) int id, @RequestParam(value = "Designation", required = true) String Designation, @RequestParam(value = "Description", required = true) String Description, @RequestParam(value = "Address", required = true) String Address, @RequestParam(value = "contact", required = true) String contact, @RequestParam(value = "managerID", required = true) int managerID,@RequestParam(value = "DepartmentID", required = true) int DepartmentID) {
		return insertNewEmployee.insertEmployee(name, id, Designation, Description, Address, contact, managerID, DepartmentID);
	}
	
}
