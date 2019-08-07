package com.paytm.springcassandra.enums;

import org.springframework.http.HttpStatus;

public enum ErrorMessages {

	EMPTY_EMPLOYEE_ID(HttpStatus.BAD_REQUEST,"Please provide Employee ID");
	
	private String message;
	private HttpStatus status;
	
	ErrorMessages(HttpStatus status, String message){
		this.status = status;
		this.message = message;
	}

	public String getMessage() {
		return message;
	}

	public void setMessage(String message) {
		this.message = message;
	}

	public HttpStatus getStatus() {
		return status;
	}

	public void setStatus(HttpStatus status) {
		this.status = status;
	}
}
