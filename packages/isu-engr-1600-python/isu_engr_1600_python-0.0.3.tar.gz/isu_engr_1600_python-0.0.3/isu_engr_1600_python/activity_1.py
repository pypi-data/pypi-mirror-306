import random
import re
pattern = r'(?=(?:.*\d.*){2})^\D*\d+\D*\d+\D*$'
number_hash={1:"one",2:"two",3:"three",4:"four",5:"five",6:"six",7:"seven",8:"eight",9:"nine"}
letter_hash = {i: chr(96 + i) for i in range(1, 27)}
def create_file(file_name):
    length=random.randint(100,2000)
    file=open(file_name,"w")
    for i in range(length):
        local_length=random.randint(5,10)
        string=""
        for j in range(local_length):
            choose=random.randint(0,2)
            if choose==0:
                next_char=letter_hash[random.randint(1,26)]
            elif choose==1:
                next_char=number_hash[random.randint(1,9)]
            else:
                next_char=str(random.randint(1,9))
            string+=next_char
        string+="\n"
        if re.match(pattern,string):
            file.write(string)
    file.flush()
    file.close()



if __name__ == "__main__":
    create_file("hello")