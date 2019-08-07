package com.paytm.SpringBootSample.datasourceConnect;


import javax.sql.DataSource;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;

import org.springframework.jdbc.datasource.DriverManagerDataSource;


@Configuration
public class GetDatasource {

    	@Value("${spring.datasource.driver-class-name}")
		private String driverClass;
		@Value("${spring.datasource.url}")
		private String dbURL;
		@Value("${spring.datasource.username}")
		private String userName;
		@Value("${spring.datasource.password}")
		private String password;
		
		
		public GetDatasource() {
			
		}

	    
	    public DataSource datasource(){
	  
	    	DriverManagerDataSource dataSource = new DriverManagerDataSource();
	    	try {	    		
			        dataSource.setDriverClassName(driverClass);
			        dataSource.setUrl(dbURL);
			        dataSource.setUsername(userName);
			        dataSource.setPassword(password);
	    		}
	    	catch(Exception e) {
	    			System.out.println(e);
	    		}
	    	return dataSource;
	    }
}
