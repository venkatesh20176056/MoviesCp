package com.paytm.SpringBootSample.services.impl;
import java.util.*;

import javax.sql.DataSource;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;

import org.springframework.stereotype.Service;

import com.paytm.SpringBootSample.datasourceConnect.GetDatasource;
import com.paytm.SpringBootSample.services.*;

@Service
public class GetAllEmployees implements AllEmployees{
	
	private GetDatasource getDataSource;
	@Autowired
	public GetAllEmployees(GetDatasource getDataSource)
	{
		this.getDataSource = getDataSource;
	}
	
	@Override
	public List<Map<String, Object>> getAll()
	{
		List<Map<String, Object>> employeeList = new ArrayList<>();
		DataSource dataSource = getDataSource.datasource();
		JdbcTemplate jdbcTemplate = new JdbcTemplate(dataSource);
		
	    String sql = "SELECT * from employees";
	    employeeList = (List<Map<String, Object>>) jdbcTemplate.queryForList(sql);
	    return employeeList;
  
	}
	

}
