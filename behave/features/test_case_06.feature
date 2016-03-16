Feature: getNetIDForUINAL

#================
    Scenario: Test Case 06: User NOT in CR, in EAS at uic ONLY (contrived)

	# Setup: Add person upstream (openCheezAI)
        Given person 111111111 is reset in openCheezAI
	Given person has openCheezAI attribute values
        | attr                  | value 	|
        # ---------------------------------------
        | uic_netid    	        | bobbo	 	|
	| banner_firstname	| Robert	|
	| banner_lastname	| Oppenheimer	|
	| i2s_firstname		| Robert	|
	| i2s_lastname		| Oppenheimer	|
  
	Given person exists in openCheezAI

	# Setup: Remove person from CentralRegistry
	Given uin 111111111 does not exist in Central Registry
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

	Then getNetIDForUINAL succeeds with results
        | attr                  	| value 	|
        # -----------------------------------------------
        | suggestedNetID     		| bobbo 	|
        | netIDSource     		| uic	 	|
        | uinFoundInCentralRegistry     | false	 	|
        | needRegisterAtIllinois        | true	 	|
        | needRegisterAtUIUC            | true	 	|
        | needRegisterAtUillinois       | true	 	|

	And person 111111111 exists in openCheezAI with attribute values
        | attr                  | value 	|
        # ---------------------------------------
        | uiuc_netid            | bobbo 	|
	| illinois_netid	| bobbo		|
	| uillinois_netid	| bobbo		|
        | uic_netid	        | bobbo 	|
	| banner_firstname	| Robert	|
	| banner_lastname	| Oppenheimer	|
	| i2s_firstname		| Robert	|
	| i2s_lastname		| Oppenheimer	|

