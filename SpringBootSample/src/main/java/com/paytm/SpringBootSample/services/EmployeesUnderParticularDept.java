package com.paytm.SpringBootSample.services;

import java.util.*;

public interface EmployeesUnderParticularDept {
	
	List<Map<String, Object>> getEmployeesUnderParticularDept( int DeptID);
}
