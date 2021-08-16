# Matching

### Rules for Fuzzy Matching Gene Names (Version 1)

1. Capitalize all letters.
2. Remove spaces from the names.
3. Remove decimal points from the names.
4. Remove the brackets and the contents of the brackets 	in the names.
5. Remove the numbers at the end of the names.
6. If dash can be found in the name.
	- If the dash is followed by numbers, keep only the content before the dash.
	- If the length of the content before the dash is less than the length of the content after the dash, then keep the content after the dash.
	- If the index of dash in the name < 2 (considered as a prefix), keep the content after the dash.
	- *Match once, if the match fails, remove the dash and make another match.


### Rules for Fuzzy Matching Gene Names (Version 2)

1. Capitalize all letters.
2. Remove spaces from the names.
3. Remove decimal points from the names.
4. Remove the brackets and the contents of the brackets 	in the names.
5. Remove the numbers at the end of the names.
6. If dash can be found in the name.
	- If the dash is followed by numbers, keep only the content before the dash.
	- If the length of the content before the dash is less than the length of the content after the dash, then keep the content after the dash.
	- If the index of dash in the name < 2 (considered as a prefix), keep the content after the dash.
	- *Match once, if the match fails, remove the dash and make another match.
7. Make length of the name < 7
8. Remove names with numbers only
9. Remove names that have only one letter
