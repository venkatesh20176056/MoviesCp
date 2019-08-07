package com.paytm.springcassandra.repository;

import java.util.Optional;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

import com.paytm.springcassandra.entities.*;

@Repository
public interface EmployeeRepository extends CrudRepository<Employees, Integer> {
	
//	public Optional<Employees> findByEmpid(int emp_code);
}

	