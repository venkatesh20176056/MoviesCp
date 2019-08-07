package com.paytm.SpringBootSample.services.impl;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import javax.sql.DataSource;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Service;

import com.paytm.SpringBootSample.datasourceConnect.GetDatasource;
import com.paytm.SpringBootSample.services.*;
import com.paytm.SpringBootSample.customexceptions.*;


@Service
public class GetEmployeesUnderParticularDept implements  EmployeesUnderParticularDept{
	
	private GetDatasource getDataSource;
	@Autowired
	public GetEmployeesUnderParticularDept(GetDatasource getDataSource)
	{
		this.getDataSource = getDataSource;
	}
	
	@Override
	public List<Map<String, Object>> getEmployeesUnderParticularDept(int DeptID)
	{
		
		List<Map<String, Object>> employeeList = new ArrayList<>();
		
		DataSource dataSource = getDataSource.datasource();
		JdbcTemplate jdbcTemplate = new JdbcTemplate(dataSource);
		
	    String sql = "SELECT * from employees where DepartmentID = "+DeptID+"";
	    employeeList = (List<Map<String, Object>>) jdbcTemplate.queryForList(sql);
	    if(employeeList.size() == 0) {
	    	throw new MyException("No Employees Under Department With ID:: "+DeptID);
	    }
	    return employeeList;
  
	}
}

