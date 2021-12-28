import random
from algo.AN import AN
from algo.caesar import caesar
from algo.ABZA import ABZA
from algo.atbash import atbash
from algo.ciphers import ciphers
import utils

class Sigma(ciphers):
    def  __init__(self):
        super().__init__()
    
    #algorithms
    Caesar = caesar()
    Atbash = atbash()
    Abza = ABZA()
    AN = AN()
    
    encoder_class_key = [
    Caesar,
    Atbash,
    Abza,
    AN
    ]

    uppercase_keys = "ABCD"
    lowercase_keys = "abcd"
    symbol_keys = "!#$%"
    space_keys = "\u025A" + "\u025B" + "\u025C" + "\u025D" + "\u025E" + "\u025F" + "\u024F"
    enter_keys = "~"+ "\u027F" + "\u028A"+ "\u018D"

    
    ##CRUCIAL FUNCTION##
    def start_encode(self, text, _token):
        token = _token
        # encode the text with each char of token
        result = text
        for i in range(len(token)):
            # get the encoder class key by token
            algo = self.get_algo_type_from_token(token, i)
            # encode the text with the encoder class key
            result = algo.encode(result)

        #encoding the spaces and enter keys
        for i in range(len(result)):
            if result[i] == " ":
                result = result.replace(result[i], random.choice(self.space_keys), 1)
            elif text[i] == "\n":
                result = result.replace(result[i], random.choice(self.enter_keys), 1)

        return result
    
    def start_decode(self, text, _token):
        reversed_token = self.walik(_token)
        result = text

        #checking for spaces and enters (carriage return) symbols first and encode it
        for i in range(len(text)):
            if text[i] in self.space_keys:
                result = result.replace(text[i], " ")
            elif text[i] in self.enter_keys:
                result = result.replace(text[i], "\n")

        for i in range(len(reversed_token)):
            # get the encoder class key by token
            algo = self.get_algo_type_from_token(reversed_token, i)
            # decode the text with the encoder class key
            result = algo.decode(result)

        return result

    def generate_token(self, _token_length=8):
        # generate a random token from keys with a customable length
        token = ""
        u_keys = self.uppercase_keys
        s_keyss = self.symbol_keys
        l_keys = self.lowercase_keys

        state = ""
        for i in range(_token_length):
            the_keys = random.choice([u_keys, s_keyss, l_keys])
            token += random.choice(the_keys)
            state = the_keys
            # make sure no direct duplicate in token
            if i>0:
                if self.should_i_remove_duplicate(): 
                    #yes i should remove duplicate
                    if token[i] == token[i-1]:
                        temp_keys = state.replace(token[i], "")#removinng duplicated char from keys
                        new_char = random.choice(temp_keys) #choosing a new char from the temp_keys
                        t = list(token)
                        t[i] = new_char #change the char in token
                        token = "".join(t)
                else:
                    #no i should not
                    pass
        return token
    
    def get_algo_type_from_token(self, _token, _index):
        # read the char in token and return the encoder class key by index of char index in keys
        the_char = _token[_index]
        try:
            if the_char not in _token:
                raise Exception("The token is not valid")
            else:
                if the_char in self.uppercase_keys:
                    return self.encoder_class_key[self.uppercase_keys.index(the_char)]
                elif the_char in self.lowercase_keys:
                    return self.encoder_class_key[self.lowercase_keys.index(the_char)]
                elif the_char in self.symbol_keys:
                    return self.encoder_class_key[self.symbol_keys.index(the_char)]
                else:
                    raise Exception("Token keys not found")
                    
        except Exception as e:
            print("Error: {}".format(e))
            return None
    
    ##CRUCIAL FUNCTION##

    ##UTIL FUNCTION##
    def should_i_remove_duplicate(self):
        return (random.randint(1, 100))%2 == 0 # jika nilai genap return true
    
    def walik(self, unreversed_token):
        # reverse the token
        reversed_token = ""
        for i in reversed(unreversed_token):
            reversed_token += i
        return reversed_token
    
    ##UTIL FUNCTION##


        
def test(text, constraint = 257):
    algo = Sigma()
    success_counter = 0
    fail_counter = 0
    for i in range(1, constraint):
        token = algo.generate_token(_token_length=i)
        encoded = algo.start_encode(text, token)
        decoded = algo.start_decode(encoded, token)
        if decoded == text and encoded != text:
            print("Token : {}".format(token))
            print("Test with token length {} : OK \n".format(i))
            success_counter += 1
        else:
            print("Token : {}".format(token))
            print("Test with token length {} : FAIL \n".format(i))
            fail_counter += 1
    
    print("TEST RESULT : ")
    print("Success : {}".format(success_counter))
    print("Fail : {}".format(fail_counter))
    print("Total : {}".format(success_counter+fail_counter))
    print("Success Rate (at least for now): {}".format(success_counter/(success_counter+fail_counter)))
    print()#jarak

if __name__ == "__main__":

    print("\nTESTING SIGMA ALGORITHM \n")
    text = "Never Gonna Give You Up"
    
    #print("testing with text / string")
    #test(text)

    print("testing with file")
    file = "dummy-file.txt"
    #test(main.readFileContent(file))
    #'''
    #playground testing
    #print("## File test ##")
    content = utils.readFileContent(file)
    sigma = Sigma()
    dummy_token = sigma.generate_token(_token_length=8)
    encoded_text = sigma.start_encode(content, dummy_token)
    decoded_text = sigma.start_decode(encoded_text, dummy_token)
    print("Token:", dummy_token)
    #print("Algo from Token index 0: ", algo)
    print("File : ", file)
    print("Content : \n", str(content))
    print()
    print("Encoded Text: \n", encoded_text , "\n")
    print("Decoded Text: \n", decoded_text)
    #main.makeCopyOfFile(file, encoded_text,"")
    #'''
    print("\nTESTING SIGMA ALGORITHM \n")
    
