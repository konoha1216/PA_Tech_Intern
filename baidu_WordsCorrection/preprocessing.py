# -*- coding: utf-8 -*-
import copy
def processing(dataset):
    if dataset == "bcmi":
        data = []
        with open('./data/bcmi.txt', 'r') as f:
            for sent in f.readlines():
                data.append(sent)
        print("total sentences number: ", len(data))

        error_list = []
        correct_list = []
        correction = []

        for sent in data:
            # error_list.append(sent.strip('\n'))
            wrong_sent = copy.deepcopy(sent)
            while '（' in wrong_sent:
                cur_position = wrong_sent.find('（')
                wrong_sent = wrong_sent[:cur_position] + wrong_sent[cur_position+5:]
            error_list.append(wrong_sent.strip('\n'))

            new_sent = copy.deepcopy(sent)
            cur_correct_list = []
            while '（' in new_sent:
                cur_position = new_sent.find('（')
                correct_word = new_sent[cur_position+2]
                wrong_word = new_sent[cur_position-1]
                new_start_position = cur_position+5
                new_sent = new_sent[:cur_position-1]+correct_word+new_sent[new_start_position:]
                cur_correct_list.append((wrong_word,correct_word))
            correct_list.append(new_sent.strip('\n'))
            correction.append(cur_correct_list)
        print(len(error_list), len(correct_list), len(correction))
        # print(error_list[0])
        # print(correct_list[0])
        # print(correction[0])
        return error_list, correct_list, correction
# if __name__ == '__main__':
#     processing("bcmi")