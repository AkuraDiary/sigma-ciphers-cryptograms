from core import Sigma
import utils
import threading

algo = Sigma()

def threaded_File_Test(file, constraint, print_result = False):
    for i in range(constraint):
        print("THREADED TESTING : {}".format(i))
        threading.Thread(target=File_Test, args=(file, i, print_result)).start()

def threaded_test(data, constraint):
    succesCount = 0
    failCount = 0
    res = [False] * constraint
    # test encrypting and decrypting with threading works with file or text     
    for i in range(constraint):
        res[i] = threading.Thread(target=base_test, args=(data, i))

        res[i].start()

        test_result = res[i]
        if test_result:
            succesCount += 1
        else:
            failCount += 1

    succes_fail_summary("Threaded Test ", succesCount, failCount)

def base_test(data, token_leng=8):
    # base encrypting and decrypting test to used it in threaded test
    try:
        token = algo.generate_token(token_leng)
        encoded = algo.start_encode(data, token)
        decoded = algo.start_decode(encoded, token)
        #print()#jarak
        #print("BASE TEST RESULT : ")
        if decoded == text and encoded != text:
            return True 
        else:
            return False 
    except Exception:
        print("Something went wrong : ", Exception)
        return False
    #print()#jarak

def test_text_with_ranged_token_len(text, constraint = 257, print_log_result = False):
    # testing the algorithm with various token length works with file or text (but not recomended for file)
    print("### testing Text with token length ###")
    success_counter = 0
    fail_counter = 0
    try:
        for i in range(1, constraint):
            token = algo.generate_token(_token_length=i)
            encoded = algo.start_encode(text, token)
            decoded = algo.start_decode(encoded, token)
            if decoded == text and encoded != text:
                if print_log_result:
                    print("Token : {}".format(token))
                    print("Test with token length {} : OK \n".format(i))
                success_counter += 1
            else:
                if print_log_result:
                    print("Token : {}".format(token))
                    print("Test with token length {} : FAIL \n".format(i))
                fail_counter += 1
    except Exception:
        print("Something went wrong : ", Exception)

    succes_fail_summary("Text with token length", success_counter, fail_counter)

def File_Test(file_path = "dummy-file.txt", constraint = 8, print_result = False):
    # test encrypting file and decrypting it
    print("### testing with file ###")
    content = utils.readFileContent(file_path)
    dummy_token = algo.generate_token(constraint)
    encoded_text = algo.start_encode(content, dummy_token)
    decoded_text = algo.start_decode(encoded_text, dummy_token)

    print("File : ", file_path)

    if decoded_text == content and encoded_text != content:
        print("Encrypting : OK")
        print("Decrypting : OK")
        if print_result:
            print("Testing {} with token : ".format(file_path) , dummy_token)
            print("Content : \n", str(content), "\n")
            print("Encoded Text: \n", encoded_text , "\n")
            print("Decoded Text: \n", decoded_text)
    print("### testing with file ###")
    print()#jarak


def succes_fail_summary(testName , success_counter, fail_counter):
    print("{} TEST RESULT : ".format(testName))
    print("Success : {}".format(success_counter))
    print("Fail : {}".format(fail_counter))
    print("Total : {}".format(success_counter+fail_counter))
    print("Success Rate (at least for now): {}".format(success_counter/(success_counter+fail_counter)))
    print()#jarak


if __name__ == "__main__":

    print("\nTESTING SIGMA ALGORITHM \n")

    
    text = "Never Gonna Give You Up, Never Gonna Make You Cry, Never Gonna Run Around and Desert You"
    print("Text : ",text, "\n")
    threaded_test(text, 257)
    
    print()#jarak

    file_path = "dummy-file.txt"
    file_content = utils.readFileContent(file_path)
    print("File : ", file_path , "\n")
    threaded_test(file_content, 257)

    print("\nTESTING SIGMA ALGORITHM \n")
