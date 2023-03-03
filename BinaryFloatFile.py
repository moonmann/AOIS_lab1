import BinaryNumFile


def compare_length(number_1, number_2):
    max_length = max(len(number_1), len(number_2))
    if number_1[0] and number_2[0] == "0":
        number_1 = number_1.rjust(max_length, "0")
        number_2 = number_2.rjust(max_length, "0")
    if number_1[0] == "1":
        number_1 = number_1.rjust(max_length, "1")
    if number_2[0] == "1":
        number_2 = number_2.rjust(max_length, "1")
    return number_1, number_2


def from_decimal_to_binary_fix(number):
    if number == 0:
        return '0.0'
    int_number = int(number)
    i = 0
    mantissa_size = 23
    float_part = number - float(int_number)
    int_result = BinaryNumFile.BinaryNum(int_number).bin_additional
    if int_result.find("1") == -1:
        result = "0" + "."
    else:
        result = int_result[int_result.find("1"):] + "."
    while i <= (mantissa_size - len(result)):
        float_part *= 2
        if int(float_part) == 0:
            result += "0"
        elif int(float_part) == 1:
            float_part -= 1
            result += "1"
            if float_part == 0:
                result = result.ljust(23, "0")
    return result


def binary_add_float_helper(number_1, number_2):
    answer = ""
    carry = 0
    number_1, number_2 = (compare_length(number_1, number_2))
    for i in reversed(range(0, len(number_1))):
        if (int(number_1[i]) + int(number_2[i]) == 1) and (carry == 0):
            answer = "1" + answer
        elif (int(number_1[i]) + int(number_2[i]) == 1) and (carry > 0):
            answer = "0" + answer
        elif (int(number_1[i]) + int(number_2[i]) == 2) and (carry > 0):
            answer = "1" + answer
        elif (int(number_1[i]) + int(number_2[i]) == 0) and (carry > 0):
            answer = "1" + answer
            carry -= 1
        elif (int(number_1[i]) + int(number_2[i]) == 0) and (carry == 0):
            answer = "0" + answer
        elif (int(number_1[i]) + int(number_2[i]) == 2) and (carry == 0):
            answer = "0" + answer
            carry += 1
    if carry > 0:
        answer = "1" + answer
    return answer


def translate_float_part_of_number(float_part):
    result = 0
    for i in range(1, len(float_part) + 1):
        result += 2 ** (-i) * int(float_part[i - 1])
    return result


def binary_add_float(number_1, number_2):
    number_1 = from_decimal_to_binary_fix(number_1)
    number_2 = from_decimal_to_binary_fix(number_2)
    unitnum1 = number_1.find("1", 0, number_1.find("."))
    unitnum2 = number_2.find("1", 0, number_2.find("."))
    exp1 = number_1.find(".") - unitnum1 - 1
    exp2 = number_2.find(".") - unitnum2 - 1
    if number_1.find("1", 0, number_1.find(".")) == -1:
        exp1 = 0
    if number_2.find("1", 0, number_2.find(".")) == -1:
        exp2 = 0
    if exp1 >= exp2:
        diff_exp = exp1 - exp2
        numsum2 = "0" * diff_exp + number_2[:(number_2.find("."))] + number_2[(number_2.find(".") + 1):(
                len(number_2) - diff_exp)]
        numsum1 = number_1[:(number_1.find("."))] + number_1[(number_1.find(".") + 1):]
    else:
        diff_exp = exp2 - exp1
        numsum1 = "0" * diff_exp + number_1[:(number_1.find("."))] + number_1[(number_1.find(".") + 1):(
                len(number_1) - diff_exp)]
        numsum2 = number_2[:(number_2.find("."))] + number_2[(number_2.find(".") + 1):]
    temp_floating_summ = binary_add_float_helper(numsum1, numsum2)
    add_numbers = len(temp_floating_summ) - len(numsum2)
    temp_result = (temp_floating_summ[:(max(number_1.find("."), number_2.find("."))) + add_numbers]
                   + "." + temp_floating_summ[(max(exp1, exp2) + add_numbers + 1):])
    print('Binary result: ' + temp_result)
    int_part = BinaryNumFile.BinaryNum(0, temp_result[:(temp_result.find("."))].rjust(16, '0')).dec
    float_part = translate_float_part_of_number(temp_result[(temp_result.find(".") + 1):])
    result = int_part + float_part
    print('Float result: ' + str(result))
    return result



