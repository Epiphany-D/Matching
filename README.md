# Matching

### Rules for Fuzzy Matching Gene Names (Version 1)

1. Capitalize all letters.
2. Remove spaces from the names.
3*. Remove decimal points from the names.
4. Remove the brackets and the contents of the brackets 	in the names.
5*. Remove the numbers at the end of the names.
6. If dash can be found in the name.
	6.1 If the dash is followed by numbers, keep only the content 					before the dash.
	6.2 If the length of the content before the dash is less than the length of 		the content after the dash, then keep the content after the dash.
	6.3 If the index of dash in the name < 2 (considered as a prefix), 				keep the content after the dash.
	6.4 *Match once, if the match fails, remove the dash and make 					another match.
