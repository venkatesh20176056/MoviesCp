package com.paytm.SpringBootSample.services.impl;

import java.util.*;

import javax.sql.DataSource;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Service;

import com.paytm.SpringBootSample.services.*;
import com.paytm.SpringBootSample.customexceptions.MyException;
import com.paytm.SpringBootSample.datasourceConnect.*;


@Service
public class GetEmployeesUnderParticularManager implements EmployeesUnderParticularManager{
	
	GetDatasource getDataSource;
	
	@Autowired
	GetEmployeesUnderParticularManager(GetDatasource getDataSource)
	{
		this.getDataSource = getDataSource;
	}
	
	@Override
	public List<Map<String,Object>> getEmployeesUnderParticularManager(String name)
	{
		List<Map<String, Object>> employeeList = new ArrayList<>();
		DataSource dataSource = getDataSource.datasource();
		JdbcTemplate jdbcTemplate = new JdbcTemplate(dataSource);
		
	    String sql = "SELECT * from employees where managerID  = (select id from managers where name = '"+name+"')";
	    employeeList = (List<Map<String, Object>>) jdbcTemplate.queryForList(sql);
	    if(employeeList.size() == 0) {
	    	throw new MyException("There is No Manager With Name:: "+name);
	    }
	    return employeeList;
	}

}
