Feature: Create a user

    Scenario: basic setup in openCheezAI
        Given person 111111111 is reset in openCheezAI
	Given person has openCheezAI attribute values
        | attr                  | value 	|
        # ---------------------------------------
        | uiuc_netid            | bobbo 	|
	| illinois_netid	| bobbo		|
	| uillinois_netid	| robert	|
	| banner_firstname	| Robert	|
	| banner_lastname	| Oppenheimer	|
	| i2s_firstname		| Robert	|
	| i2s_lastname		| Oppenheimer	|
  
	Given person exists in openCheezAI

	# When we run some thing

	Then person 111111111 has uiuc_netid set to bobbo in openCheezAI

	Then person 111111111 exists in openCheezAI with attribute values
        | attr                  | value 	|
        # ---------------------------------------
        | uiuc_netid            | bobbo 	|
	| illinois_netid	| bobbo		|
	| uillinois_netid	| robert	|
	| banner_firstname	| Robert	|
	| banner_lastname	| Oppenheimer	|
	| i2s_firstname		| Robert	|
	| i2s_lastname		| Oppenheimer	|

    Scenario: basic setup in Central Registry
    	Given user 'bobbo' is reset in Central Registry
	Given user has uiucEduUIN set to 111111111
	Given user has person in uiucEduType
	Given user has phone in uiucEduType
	Given user has student in uiucEduType
	Given user exists in Central Registry
