Feature: Test Case 03 

	Scenario: Test Case 03: User NOT in CR, in EAS at uillinois only

	# Setup: Add person upstream (openCheezAI)
        Given person 111111111 is reset in openCheezAI
	#Given person has openCheezAI attribute values
        #| attr                  | value 	|
        ## ---------------------------------------
	#| uillinois_netid	| bobbo		|
	#| banner_firstname	| Robert	|
	#| banner_lastname	| Oppenheimer	|
	#| i2s_firstname		| Robert	|
	#| i2s_lastname		| Oppenheimer	|
  #
	Given person exists in openCheezAI
