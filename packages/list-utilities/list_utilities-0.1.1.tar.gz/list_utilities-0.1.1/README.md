 List Utilities

List Utilities is a simple Python package that provides utility functions for common list operations, including removing duplicates and flattening nested lists.

Installation

You can install the package using pip:

pip install list_utilities


Functions Descriptions

First Function: remove_duplicates(input_list)
Description: This function takes a list as input and returns a new list that contains the unique elements from the original list, preserving their original order. It effectively removes any duplicate entries without altering the sequence of the remaining items.

Parameters:
input_list (list): A list of elements from which duplicates need to be removed. The elements can be of any data type (e.g., integers, strings).
Returns:

(list): A list containing only unique elements from the input_list.

Example:
 
from list_utilities import remove_duplicates

my_list = [1, 2, 2, 3, 4, 4, 5]
unique_list = remove_duplicates(my_list)
print(unique_list)  

Output:
 
[1, 2, 3, 4, 5]

Second Function: flatten_list(nested_list)
Description: This function flattens a nested list, which may contain other lists at any level of depth, into a single list. It recursively traverses through all elements and sub-elements, collecting them into a single flat structure.

Parameters:

nested_list (list): A list that may contain other lists as elements. The nesting can be at multiple levels.
Returns:

(list): A single list that includes all elements from the nested_list, with no nesting.
Example:

from list_utilities import flatten_list

nested = [[1, 2], [3, 4, [5, 6]], 7]
flat = flatten_list(nested)
print(flat) 

Output:

[1, 2, 3, 4, 5, 6, 7]


License
This project is licensed under the MIT License - see the LICENSE file for details.

 
