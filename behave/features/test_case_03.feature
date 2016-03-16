Feature: Test Case 03 

	Scenario: Test Case 03: User NOT in CR, in EAS at uillinois only

	# Setup: Add person upstream (openCheezAI)
        Given person 111111111 is reset in openCheezAI
	Given person has openCheezAI attribute values
        | attr                  | value 	|
        # ---------------------------------------
	| uiuc_netid		|      		|
	| illinois_netid	|      		|
	| uillinois_netid	| bobbo		|
	| banner_firstname	| Robert	|
	| banner_lastname	| Oppenheimer	|
	| i2s_firstname		| Robert	|
	| i2s_lastname		| Oppenheimer	|
  
	Given person exists in openCheezAI

	# Setup: Remove person from Central Registry
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
	| testMode		| false		|

	Then getNetIDForUINAL succeeds with results
        | attr                  	| value 	|
        # -----------------------------------------------
        | suggestedNetID     		| bobbo	 	|
        | netIDSource     		| uillinois 	|
        | uinFoundInCentralRegistry     | false	 	|
        | needRegisterAtIllinois        | true	 	|
        | needRegisterAtUIUC            | true	 	|
        | needRegisterAtUillinois       | false	 	|

	And person 111111111 exists in openCheezAI with attribute values
        | attr                  | value 	|
        # ---------------------------------------
        | uiuc_netid            | bobbo 	|
	| illinois_netid	| bobbo		|
	| uillinois_netid	| bobbo		|
	| banner_firstname	| Robert	|
	| banner_lastname	| Oppenheimer	|
	| i2s_firstname		| Robert	|
	| i2s_lastname		| Oppenheimer	|

