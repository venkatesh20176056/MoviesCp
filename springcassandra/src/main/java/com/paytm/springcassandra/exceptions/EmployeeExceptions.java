package com.paytm.springcassandra.exceptions;


import com.paytm.springcassandra.enums.*;

public class EmployeeExceptions extends Exception{
	
	ErrorMessages errorMessage;

	public EmployeeExceptions() {
		super();
	}
	
	public EmployeeExceptions(String message) {
		super(message);
	}
	
	public EmployeeExceptions(Throwable cause) {
		super(cause);
	}
	
	public EmployeeExceptions(String message, Throwable cause) {
		super(message, cause);
	}

	public EmployeeExceptions(ErrorMessages errorMessage) {
		super(errorMessage.getMessage());
		this.errorMessage = errorMessage;
	}
	
	public EmployeeExceptions(ErrorMessages errorMessage, Throwable cause) {
		super(errorMessage.getMessage(),cause);
		this.errorMessage = errorMessage;
	}
		
	public ErrorMessages getErrorMessages() {
		return errorMessage;
	}
	
}
