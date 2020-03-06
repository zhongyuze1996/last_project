import random,string

def get_random(n):
    code_list=random.sample(string.digits,n)
    code=''.join(code_list)
    return code