package com.paytm.SpringBootSample.services;

public interface InsertNewEmployee {

	int insertEmployee(String name, int id,String Designation,String Description,String Address,String contact,int managerID,int DepartmentID);
	
}
