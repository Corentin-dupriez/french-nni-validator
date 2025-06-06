import re
from recover_city_codes import call_geo_api

def national_security_number_validator(ns_number_with_key: str|int):
    """Function that takes the national security number with key (15 chars).
    It splits it into 2 (the number without key and the key itself) and validates the two 
    using validate_with_no_key and comparing the key with a generated key.

    Args:
        ns_number_with_key (str | int): A 15 chars long national security number 

    Raises:
        ValueError: In case the part without the key doesn't match the regex for validation
        ValueError: In case the key from the provided number doesn't match a generated key 
        from the first part of the provided number

    Returns:
        _type_: A message displaying that the national security number is OK.
    """
    ns_number_with_key = str(ns_number_with_key)
    
    if not len(ns_number_with_key) == 15:
        raise ValueError('The length of the number is not 15 characters.')
    
    ns_no_key = ns_number_with_key[:13]
    ns_key_only = ns_number_with_key[13:]
    calculated_key = calculate_key(ns_no_key)
    
    if not validate_with_no_key(ns_no_key) or not ns_key_only == calculated_key: 
        raise ValueError('The format of the national security number is not correct.')
    
    return 'The format of the national security number is correct.'


def validate_with_no_key(ns_number: str) -> bool: 
    """Function that takes the national security number (without key)
    and compares it to the regex for validation.
    
    After regex validation, the function calls find_city_code to find if the region and 
    city codes exist.

    Args:
        ns_number (str): String of the national security number (13 chars)

    Returns:
        bool: Result of the comparison between the number and the regex
    """
    regex = r"^([128])[00-99]{2}([01-12]{2}|[20-99]{2})([01-99]{2})\d{6}$|^([128])[00-99]{2}([01-12]{2})(2[AB])([01-99]{2})\d{4}$"
    
    if not re.match(regex, ns_number): 
        raise ValueError('The format is incorrect')
    
    find_city_code(ns_number)
    
    return True


def find_city_code(ns_number: str) -> str: 
    """Function that calls the geo API from French government (via call_geo_api)
    to see if the geographical information of the individual exists

    Args:
        ns_number (str): The national security number as a string

    Raises:
        ValueError: An error if the city code doesn't exist
        ValueError: An error if any other error is encountered while calling the geo API

    Returns:
        str: The city name
    """
    code = ns_number[5:10]
    response = call_geo_api(code)
    
    if response[0] == 404: 
        raise ValueError('The city code is incorrect')
    elif response[0] == 200: 
        return response[1]
    else: 
        raise ValueError('Technical error')


def calculate_key(nir: str|int) -> str: 
    """Function that takes in the national security number without the key 
    to calculate the 2 digits key. If the number is not only digits, it has 
    to be processed by the replace_corsica_code_function.
    
    The calculation is 97 - (nir % 97)

    Args:
        nir (str|int): The 13 chars national security number

    Returns:
        str: A two chars long key. If the result is less than 10, we have to use zfill 
        to have 2 chars.
    """
    #check that the national security number contains a letter
    if not nir.isdigit():
        nir = replace_corsica_code(nir)
        
    return str(97 - (int(nir) % 97)).zfill(2)


def replace_corsica_code(ns_number:str) -> str: 
    """This helper function is used when the national security number has letters in it.
    It replaces the code (1 digit and 1 letter) with a 2 digits long code.

    Args:
        ns_number (str): The national security number with a letter in it

    Returns:
        str: the national security number with replaced Corsica code (for calculation of the
        key)
    """
    corsica_codes = {'2A': '19', '2B': '18'}
    #replace the code at index 5 and 6 by the corresponding number
    calculated_nir = ns_number[:5] + corsica_codes[ns_number[5:7]] + ns_number[7:]
    
    return calculated_nir


def national_security_number_key_generator(ns_number: int|str) -> str:
    """This function takes in a national security number of 13 characters long 
    and generates a 2 characters long key. It returns a concatenation of the initial value 
    and the key. In case the number has letter in it (for Corsica), it calls a function to 
    to replace the Corsica codes with digits

    Args:
        ns_number (int | str): The 13 chars long national security number in int or str

    Raises:
        ValueError: In case the format is incorrect, raise an error.

    Returns:
        str: The concatenated number with the key
    """
    #Change the number to a string
    ns_number = str(ns_number)
    
    #if the validation is not OK, raise a ValueError
    if not validate_with_no_key(ns_number):
        raise ValueError('The format of the national security number is not correct')
    
    #Check if number is only digit
    if ns_number.isdigit(): 
        key = calculate_key(ns_number)
        
    #In case the person is from Corsica, there are letters in the national security number
    else: 
        # They should be replaced like so: 2A -> 19, 2B -> 18
        calculated_nir = replace_corsica_code(ns_number)
        key = calculate_key(calculated_nir)
        
    return str(ns_number) + key
