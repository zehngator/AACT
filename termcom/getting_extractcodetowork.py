

def extract_code(mess):
    start = mess.find("```")
    print(start)
    #codetype = mess[start+3:].split()[0]
    code = mess[start+3:]
    end = code.find("```")
    code = code[:end-1]
    return code

if __name__ == "__main__":
    with open('last_response.txt', "r") as f:
        mess = f.read()
    code = extract_code(mess)
    print(code)
