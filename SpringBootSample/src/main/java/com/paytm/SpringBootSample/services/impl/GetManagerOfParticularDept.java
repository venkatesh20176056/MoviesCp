package com.paytm.SpringBootSample.services.impl;

import java.util.*;

import javax.sql.DataSource;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Service;

import com.paytm.SpringBootSample.customexceptions.MyException;
import com.paytm.SpringBootSample.datasourceConnect.*;

import com.paytm.SpringBootSample.services.*;

@Service
public class GetManagerOfParticularDept implements ManagerOfParticularDept{

	
	private GetDatasource getDatasource;
	
	@Autowired
	GetManagerOfParticularDept(GetDatasource getDatasource)
	{
		this.getDatasource = getDatasource;
	}
	
	@Override
	public List<Map<String, Object>> getManagerOfParticularDept(int DeptID)
	{
		List<Map<String, Object>> manager = new ArrayList<>();
		DataSource dataSource = getDatasource.datasource();
		JdbcTemplate jdbcTemplate = new JdbcTemplate(dataSource);
		
	    String sql = "SELECT * from managers where DepartmentID = "+DeptID+"";
	    manager = (List<Map<String, Object>>) jdbcTemplate.queryForList(sql);
	    if(manager.size() == 0) {
	    	throw new MyException("There is No Department With ID:: "+DeptID);
	    }
		return manager;	
	}
}
