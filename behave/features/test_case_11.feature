Feature: Test Case 11 (ERROR CASE)

    Scenario: User NOT in CR, in EAS at uic/uillinois with NetID XXX, but there is ANOTHER user (UIN) with NetID XXX at uiuc so it conflicts (contrived)

    	# Someone changed the someone ELSE's NetID in CR only and didn't tell EAS
	# Setup: Make sure our UIN will not be found in Central Registry
	Given uin 111111111 does not exist in Central Registry

	# Setup: Add person upstream (openCheezAI) with a NetID
        Given person 111111111 is reset in openCheezAI
	Given person has openCheezAI attribute values
        | attr                  | value 	|
        # ---------------------------------------
	| uillinois_netid	| bobbo		|
	| uic_netid		| bobbo		|
	| banner_firstname	| Robert	|
	| banner_lastname	| Oppenheimer	|
	| i2s_firstname		| Robert	|
	| i2s_lastname		| Oppenheimer	|
  
	Given person exists in openCheezAI

	# Setup: Add ANOTHER person to CentralRegistry with this NetID
    	Given user 'bobbo' is reset in Central Registry
	Given user has uiucEduUIN set to 222222222
	Given user has uiucEduFirstName set to Bobbie
	Given user has uiucEduLastName set to Orlando
	Given user has person in uiucEduType
	Given user has phone in uiucEduType
	Given user has student in uiucEduType
	Given user exists in Central Registry

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

	Then getNetIDForUINAL fails with error code 403

