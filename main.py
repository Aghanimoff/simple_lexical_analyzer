import re
import string

# Входной язык содержит операторы выбора типа case … of … end, разделенные
# символом ; (точка с запятой). Операторы выбора содержат идентификаторы, знак двоеточия (:),
# знаки операций +, -, римские числа, знак присваивания (:=).

# определяем объекты для распознавания лексическим анализатором, исходя из варианта
words_of_choise = {'case': 'start', 'of': 'of', 'end': 'end', ';': 'separator', ':': 'is'}
symbols_roman_number = ['I', 'V', 'X', 'L', 'C', 'D', 'M']

symbols_arifmetic = ['+', '-']
symbol_comment = '~'
symbol_equal = ':='

# все одиночные символы языка
symbols_all_language = symbols_roman_number + symbols_arifmetic + [symbol_comment]
# все предопределенные языком операторы и зарезервированные слова
all_language = list(words_of_choise.keys()) + symbols_all_language + [symbol_equal]
# все некорректные символы языка, которых не должно быть: арабские числа и знаки припенания
disable_symbol_list = [i for i in string.digits] + [i for i in string.punctuation if i not in all_language]


def load_file(file_name):
    with open(file_name, 'r') as file:
        code = file.read().splitlines()
    return code


def lexical_analyzer(lexical_result):

    # цикл для формирования соответствий объектов из исходного кода и лексического анализатора языка
    result = []
    for line_number, line in enumerate(lexical_result):
        result += [[]]
        if line == tuple([]):
            result[line_number] += ['пустая строка']
        for word in line:
            result[line_number] += [
                'ОШИБКА Длина оператора превышает 32 символа' if len(word) > 32 else
                'ОШИБКА Ошибочный символ' if word in disable_symbol_list else
                'Римское число' if all([i in symbols_roman_number for i in word]) else
                'Индетефикатор' if word not in all_language else
                'арифметический знак' + word if word in symbols_arifmetic else
                'оператор ветвления ' + words_of_choise[word] if word in words_of_choise.keys() else
                'комментарий' if word == symbol_comment else
                'оператор присваивания' if word == symbol_equal else
                'ОШИБКА неопознанный объект'
            ]

            if word == symbol_comment:
                break
    return result


def print_result(lexical_result, result):
    for e, i in enumerate(lexical_result):
        print(f'___________________________\n==== строка № {e}:')
        for word in zip(lexical_result[e], result[e]):
            print('{0:33}  {1}'.format(word[0], word[1]))


def get_operations(lexical_result):
    operations = []
    is_case_block = False
    for line in lexical_result:
        if line == tuple([]):

            pass
        elif 'end' in line:
            is_case_block = False
        elif is_case_block:
            operations[-1] += line
        elif 'case' in line:
            is_case_block = True
            operations += [line]
        else:
            operations += [line]
    return operations


def print_operations(operations):
    for i in operations:
        print()
        for j in i:
            print(j, end=' ')


if __name__ == '__main__':

    # подгружаем текст кода в переменную
    source_code = load_file(file_name='code.txt')

    # парсим исходный код построчно, и пословно, формируя список и кортежей из лексем
    lexical_result = [tuple(j) for j in [re.findall(r"[A-Za-z0-9_]+|[:=]+|[~+-:;]", i) for i in source_code]]

    # Лексический анализ
    result = lexical_analyzer(lexical_result)

    # Вывод результата работы лексического анализатора
    print_result(lexical_result, result)

    # Цикл для формирования операций (обособить блок case of end) из исходного кода
    operations = get_operations(lexical_result)

    # Вывод последовательности операций из исходного кода в консоль
    print_operations(operations)
