package com.paytm.SpringBootSample.services.impl;

import java.sql.Types;

import javax.sql.DataSource;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Service;

import com.paytm.SpringBootSample.datasourceConnect.GetDatasource;
import com.paytm.SpringBootSample.services.*;

@Service
public class InsertNewEmployeeImpl implements InsertNewEmployee{
	
	private GetDatasource getDataSource;
	@Autowired
	public InsertNewEmployeeImpl(GetDatasource getDataSource)
	{
		this.getDataSource = getDataSource;
	}
	
	@Override
	public int insertEmployee(String name, int id, String Designation, String Description, String Address,
			String contact, int managerID, int DepartmentID) {
		
		DataSource dataSource = getDataSource.datasource();
		JdbcTemplate jdbcTemplate = new JdbcTemplate(dataSource);
		
		String insert_stmt = "Insert into employees(name, id, Designation, Description, Address, contact, managerID, DepartmentID) VALUES(?,?,?,?,?,?,?,?)";
		Object[] params = new Object[] { name, id, Designation, Description, Address, contact, managerID, DepartmentID };
		int[] types = new int[] { Types.VARCHAR, Types.INTEGER, Types.VARCHAR, Types.VARCHAR,Types.VARCHAR,Types.VARCHAR, Types.INTEGER, Types.INTEGER };
		
		int row = jdbcTemplate.update(insert_stmt, params, types);
		return row;
	}

}
