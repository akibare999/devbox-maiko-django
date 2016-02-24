Feature: Create a user

    Scenario: basic setup
        Given person '111111111' is reset in openCheezAI
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

	Then person has...

