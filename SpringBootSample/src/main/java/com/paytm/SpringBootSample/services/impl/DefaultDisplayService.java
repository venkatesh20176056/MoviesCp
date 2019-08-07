package com.paytm.SpringBootSample.services.impl;

import org.springframework.stereotype.Service;

import com.paytm.SpringBootSample.services.DisplayService;

@Service
public class DefaultDisplayService implements DisplayService {

	@Override
	public String welcomeNote(String st)
	{
		return "Hello "+st;
	}
}