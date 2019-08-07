package com.paytm.springcassandra.services.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.paytm.springcassandra.services.*;
import com.paytm.springcassandra.repository.*;
import com.paytm.springcassandra.entities.*;

import java.util.*;

@Service
public class DefaultEmployeeService implements EmployeeService{
	
	@Autowired
	private EmployeeRepository employeeRepository;
	
	@Override
	public List<Employees> GetAllEmployeeDetails() {
		
		List<Employees> list = new ArrayList<>();
		Iterable<Employees> employee_list = employeeRepository.findAll();
		for (Employees e:employee_list) {
			list.add(e);
		}
		return list;
		
	}

	@Override
	public Optional<Employees> GetEmployeeByID(int emp_code) {
		
		Optional<Employees> employee_list = employeeRepository.findById(emp_code);
		
		return employee_list;
		
	}

}
