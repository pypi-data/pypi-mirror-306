# version 0.4
import random
import sys
sys.path.append('../v_console/')


# This Python class generates a list of random numbers or characters based on the input element.
class list_elements:
    def __init__(self, element):
        self.element = element

    def select_num(self):
        """
        The function generates a list of 50 random numbers within a specified range.
        :return: The `select_num` method returns a list of 50 randomly selected numbers from a range of
        numbers based on the `element` attribute of the class. If an error occurs during the process, it
        will return a message indicating the error that occurred.
        """
        try:
            list_num = list(range(self.element))
            list_num = random.sample(list_num, 50)
            return list_num
        except Exception as e:
            return print(f"Error generating list of numbers -> {e}")

    def select_char(self):
        """
        The function `select_char` randomly selects 5 unique characters from a given list and returns
        them.
        :return: A list of unique characters selected randomly from the `element` attribute of the
        object, with a maximum of 5 characters. If an error occurs during the process, a message
        indicating the error is returned.
        """
        try:
            chars = []
            for i in range(5):
                char = random.choice(self.element)
                chars.append(char)
            return list(set(chars))
        except Exception as e:
            return print(f"Error generating character list -> {e}")



def password_generator(list_num: list, list_str: list, list_char: list):
    """
    The function generates a random password using characters, numbers, and strings from the provided
    lists.
    
    :param list_num: A list of numbers that can be used in the password generation process
    :type list_num: list
    :param list_str: A list of strings that will be used to generate the password
    :type list_str: list
    :param list_char: List of special characters such as !@#$%^&*()
    :type list_char: list
    :return: The function `password_generator` is returning a randomly chosen password from a list of
    generated passwords.
    """
    try:
        passwords = []
        for i in range(50):
            password = f"{random.choice(list_char)}{random.choice(list_num)}{random.choice(list_str)}{random.choice(list_char)}{random.choice(list_str).upper()}{random.choice(list_str)}{random.choice(list_num)}{random.choice(list_str)}{random.choice(list_str)}{random.choice(list_char)}"
            if password not in passwords:
                passwords.append(password)
            else:
                continue
        chosen = random.choice(passwords)
        # print(chosen)
        return chosen
    except Exception as e:
        return print(f"Error generating password -> {e}")


def password():
    """
    This Python function generates a password using random numbers, alphabets, and special characters.
    :return: The `password()` function is returning the result of calling the `password_generator()`
    function with the generated `num`, `alphabet`, and `char` elements as arguments. The
    `password_generator()` function is responsible for generating the password based on these elements.
    """
    try:
        num = list_elements(random.randint(51, 4000))
        num = num.select_num()

        alphabet = list_elements(list("abcdefghijklmnopqrstuvwxyz"))
        alphabet = alphabet.select_char()

        char = list_elements(['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<',
                              '=', '>', '?', '@', '[', ']', '^', '_', '`', '{', '|', '}', '~', "¡", "¿", "¿", "¡", "°", "€"])
        char = char.select_char()

        return password_generator(num, alphabet, char)
    except Exception as e:
        return print(f"Error in generating data collection to generate the password -> {e}")


if __name__ == '__main__':
    password()
