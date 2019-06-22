import pycorrector
from preprocessing import processing

error_list, correct_list, correction = processing('bcmi')
pyc = []
flag = 0
num = 0

for text in error_list:
    corrected_sent, detail = pycorrector.correct(text)
    pyc.append(corrected_sent)
    if corrected_sent == correct_list[flag]:
        num+=1
    print("wrong sent: ", text)
    print("correct sent: ", correct_list[flag])
    print("jiucuo sent: ", corrected_sent)
    flag += 1
    print("total sent: ", flag, ", right correction: ", num, ", current precision: ", num/flag)
    print()
    with open("bcmi_pycorrect.txt", 'a') as f:
        f.write(corrected_sent)
        f.write('\n')
    f.close()