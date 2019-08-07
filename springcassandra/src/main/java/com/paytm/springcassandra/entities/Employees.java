package com.paytm.springcassandra.entities;

import javax.persistence.*;

@Entity
@Table(name = "employees")
public class Employees {
	
	@Id
	@Column(name = "empid")
	int empid;
	
	@Column(name = "age")
	int age;
	
	@Column(name = "designation")
	String designation;
	
	@Column(name = "name")
	String name;


	public int getEmpid() {
		return empid;
	}

	public void setEmpid(int empid) {
		this.empid = empid;
	}

	public int getAge() {
		return age;
	}

	public void setAge(int age) {
		this.age = age;
	}

	public String getDesignation() {
		return designation;
	}

	public void setDesignation(String designation) {
		this.designation = designation;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}	
}
