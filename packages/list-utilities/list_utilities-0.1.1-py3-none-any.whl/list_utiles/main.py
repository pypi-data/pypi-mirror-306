def remove_duplicates(input_list):
    """ Remove duplicates from a list while preserving the original order."""
    # Use a dictionary to automatically remove duplicates and preserve order
    return list(dict.fromkeys(input_list))

def flatten_list(nested_list):
    """
    Flatten a nested list into a single list.
    """
    # Initialize an empty list to hold the flattened elements
    flat_list = []
    
    for sublist in nested_list:
        # Check if the current element is a list (i.e., needs further flattening)
        if isinstance(sublist, list):
            # Recursively call flatten_list on the sublist and extend flat_list with the result
            flat_list.extend(flatten_list(sublist))
        else:
            # If the element is not a list, append it directly to flat_list
            flat_list.append(sublist)
    
    # Return the fully flattened list
    return flat_list
