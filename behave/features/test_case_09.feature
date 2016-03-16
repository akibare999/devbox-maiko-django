Feature: Test Case 09

    Scenario: User NOT in CR, in EAS with same NetID at uiuc/illinois and uillinois (contrived)

	# Setup: Add person upstream (openCheezAI)
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

	# Setup: Make sure UIN not found in Central Registry
	Given uin 222222222 does not exist in Central Registry  

	# Setup: REMOVE person from CentralRegistry
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
        | suggestedNetID     		| bobbo	 	|
        | netIDSource     		| illinois 	|
        | uinFoundInCentralRegistry     | false	 	|
        | needRegisterAtIllinois        | false	 	|
        | needRegisterAtUIUC            | false	 	|
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

