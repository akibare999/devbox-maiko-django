Feature: Test Case 12 (ERROR CASE)

    Scenario: User in EAS at uiuc with NetID XXX, but illinois with NetID YYY (contrived)

    	# EAS is straight up corrupted.

	# Setup: Make sure our UIN will not be found in Central Registry
	# (doesn't matter)
	Given uin 111111111 does not exist in Central Registry

	# Setup: Add person upstream (openCheezAI) with a NetID
        Given person 111111111 is reset in openCheezAI
	Given person has openCheezAI attribute values
        | attr                  | value 	|
        # ---------------------------------------
	| uiuc_netid		| robert	|
	| illinois_netid	| bobbo		|
	| uillinois_netid	| bobbo		|
	| banner_firstname	| Robert	|
	| banner_lastname	| Oppenheimer	|
	| i2s_firstname		| Robert	|
	| i2s_lastname		| Oppenheimer	|
  
	Given person exists in openCheezAI

	# Setup: Remove user from Central Registry (doesn't matter)
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

	Then getNetIDForUINAL fails with error code 401

