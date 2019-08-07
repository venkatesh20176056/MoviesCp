package com.paytm.springcassandra.services;

import java.util.*;
import com.paytm.springcassandra.entities.*;

public interface EmployeeService {
	
	public List<Employees> GetAllEmployeeDetails();
	
	public Optional<Employees> GetEmployeeByID(int emp_code);
}
