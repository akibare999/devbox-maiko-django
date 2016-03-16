Feature: Test Case 10 (ERROR CASE)

    Scenario: User in CR with NetID XXX, in EAS at uiuc/illinois with DIFFERENT NetID YYY (contrived)

    	# Someone changed the user's NetID in CR only and didn't tell EAS

	# Setup: Add person upstream (openCheezAI) with a NetID
        Given person 111111111 is reset in openCheezAI
	Given person has openCheezAI attribute values
        | attr                  | value 	|
        # ---------------------------------------
        | uiuc_netid            | bobbo 	|
	| illinois_netid	| bobbo		|
	| uillinois_netid	| bobbo		|
	| banner_firstname	| Robert	|
	| banner_lastname	| Oppenheimer	|
	| i2s_firstname		| Robert	|
	| i2s_lastname		| Oppenheimer	|
  
	Given person exists in openCheezAI

	# Setup: Add person to CentralRegistry with different NetID
    	Given user 'robert' is reset in Central Registry
	Given user has uiucEduUIN set to 111111111
	Given user has uiucEduFirstName set to Robert
	Given user has uiucEduLastName set to Oppenheimer
	Given user has person in uiucEduType
	Given user has phone in uiucEduType
	Given user has student in uiucEduType
	Given user exists in Central Registry

    	Given user 'bobbo' is reset in Central Registry

	# Test: call getNetIDForUINAL
	When getNetIDForUINAL is called with arguments
        | attr                  | value 	|
        # ---------------------------------------
        | uin                   | 111111111 	|
	| firstName		| Robert	|
	| middleName		| X		|
	| lastName		| Oppenheimer	|
	| type			| S		|
        | createNetIDIfNotFound | true	        |
	| testMode		| false		|

	Then getNetIDForUINAL fails with error code 402

