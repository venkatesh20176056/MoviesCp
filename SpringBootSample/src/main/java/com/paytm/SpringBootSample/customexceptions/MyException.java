package com.paytm.SpringBootSample.customexceptions;

import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.http.HttpStatus;

@ResponseStatus(HttpStatus.NOT_FOUND)
public class MyException extends RuntimeException{

	public MyException(String st)
	{
		super(st);
	}
	
}
