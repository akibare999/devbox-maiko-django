Feature: Test Case 02

	Scenario: User in CR, in EAS with different NetID at UIUC and enterprise

	# Setup: Add person upstream (openCheezAI)
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

	# Setup: Add person to CentralRegistry
    	Given user 'bobbo' is reset in Central Registry
	Given user has uiucEduUIN set to 111111111
	Given user has uiucEduFirstName set to Robert
	Given user has uiucEduLastName set to Oppenheimer
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
	| testMode		| false		|

	Then getNetIDForUINAL succeeds with results
        | attr                  	| value 	|
        # -----------------------------------------------
        | suggestedNetID     		| bobbo	 	|
        | netIDSource     		| illinois 	|
        | uinFoundInCentralRegistry     | true	 	|
        | needRegisterAtIllinois        | false	 	|
        | needRegisterAtUIUC            | false	 	|
        | needRegisterAtUillinois       | false	 	|

	And person 111111111 exists in openCheezAI with attribute values
        | attr                  | value 	|
        # ---------------------------------------
        | uiuc_netid            | bobbo 	|
	| illinois_netid	| bobbo		|
	| uillinois_netid	| robert	|
	| banner_firstname	| Robert	|
	| banner_lastname	| Oppenheimer	|
	| i2s_firstname		| Robert	|
	| i2s_lastname		| Oppenheimer	|


