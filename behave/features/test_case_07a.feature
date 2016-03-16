Feature: getNetIDForUINAL

#================
    Scenario: Test Case 07a: STUDENT not in CR, not in EAS, force NetID generation
	# Setup: Make sure target netid is not assigned (openCheezAI)
        Given netid 'samkim2' is not assigned in openCheezAI

	# Setup: Add person upstream (openCheezAI)
        Given person 222222222 is reset in openCheezAI
	Given person has openCheezAI attribute values
        | attr                  | value 	|
        # ---------------------------------------
	| banner_firstname	| Sam		|
	| banner_lastname	| Kim		|
	| i2s_firstname		| Sam		|
	| i2s_lastname		| Kim		|
  
	Given person exists in openCheezAI

	# Setup: Make sure UIN not found in Central Registry
	Given uin 222222222 does not exist in Central Registry

	# Setup: Remove person from CentralRegistry
    	Given user 'samkim2' is reset in Central Registry

	# Test: call getNetIDForUINAL
	When getNetIDForUINAL is called with arguments
        | attr                  | value 	|
        # ---------------------------------------
        | uin                   | 222222222 	|
	| firstName		| Sam		|
	| middleName		| X		|
	| lastName		| Kim		|
	| type			| S		|
        | createNetIDIfNotFound | true	        |
	| testMode		| false		|

	Then getNetIDForUINAL succeeds with results
        | attr                  	| value 	|
        # -----------------------------------------------
        | suggestedNetID     		| samkim2 	|
        | netIDSource     		| new	 	|
        | uinFoundInCentralRegistry     | false	 	|
        | needRegisterAtIllinois        | true	 	|
        | needRegisterAtUIUC            | true	 	|
        | needRegisterAtUillinois       | true	 	|

	And person 222222222 exists in openCheezAI with attribute values
        | attr                  | value 	|
        # ---------------------------------------
        | uiuc_netid            | samkim2 	|
	| illinois_netid	| samkim2	|
	| uillinois_netid	| samkim2	|
	| banner_firstname	| Sam		|
	| banner_lastname	| Kim		|
	| i2s_firstname		| Sam		|
	| i2s_lastname		| Kim		|

