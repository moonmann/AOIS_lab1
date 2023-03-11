import BinaryNumFile

MANTISSA_SIZE = 23
BIN_ZERO = '0.0000000000000000000000'


def translate_float_part_to_bin(float_part, result):
    result.append('')
    while MANTISSA_SIZE >= len(result[0]) + len(result[1]):
        float_part *= 2
        if int(float_part) == 0:
            result[1] += '0'
        elif int(float_part) == 1:
            float_part -= 1
            result[1] += '1'
            if float_part == 0:
                result[1] = result[1].ljust(MANTISSA_SIZE-len(result[0]), '0')
    return result


def from_decimal_to_binary_fix(number):
    if number == 0.0:
        return BIN_ZERO
    result = []
    int_number = int(number)
    float_part = number - float(int_number)
    int_part = BinaryNumFile.BinaryNum(int_number).bin_right
    if int_part == BinaryNumFile.BIN_ZERO:
        result.append('0')
    else:
        result.append(int_part[int_part.find('1'):])
    translate_float_part_to_bin(float_part, result)
    return result


def convert_to_normal_view(number):
    zero_index = number.find('0')
    one_index = number.find('1')
    if zero_index < one_index:
        return number[zero_index + 1:]
    return number


def binary_add_float_helper(number_1, number_2):
    result = ''
    carry = 0
    for i in range(MANTISSA_SIZE - 1, -2, -1):
        bit_sum = carry
        bit_sum += 1 if number_1[i] == '1' else 0
        bit_sum += 1 if number_2[i] == '1' else 0
        result = ('1' if bit_sum % 2 == 1 else '0') + result
        carry = 0 if bit_sum < 2 else 1
    return convert_to_normal_view(result)


def translate_float_part_to_decimal(float_part):
    result = 0
    for i in range(1, len(float_part) + 1):
        result += 2 ** (-i) * int(float_part[i - 1])
    return result


def binary_add_float(number_1, number_2):
    str_num_1 = from_decimal_to_binary_fix(number_1)
    str_num_2 = from_decimal_to_binary_fix(number_2)
    point_index_1 = len(str_num_1[0])
    point_index_2 = len(str_num_2[0])
    point_index = point_index_1 - point_index_2
    if point_index > 0:
        str_num_1 = (str_num_1[0] + str_num_1[1])[:MANTISSA_SIZE]
        str_num_2 = ('0' * point_index + str_num_2[0] + str_num_2[1])[:MANTISSA_SIZE]
    else:
        str_num_1 = ('0' * (point_index * -1) + str_num_1[0] + str_num_1[1])[:MANTISSA_SIZE]
        str_num_2 = (str_num_2[0] + str_num_2[1])[:MANTISSA_SIZE]
    float_sum = binary_add_float_helper(str_num_1, str_num_2)
    print(float_sum)
    int_part_str = float_sum[:max(point_index_1, point_index_2) + len(float_sum) - MANTISSA_SIZE]
    float_part_str = float_sum[max(point_index_1, point_index_2) + len(float_sum) - MANTISSA_SIZE:]
    bin_result = int_part_str + '.' + float_part_str
    print('Binary result: ' + bin_result)
    int_part = BinaryNumFile.BinaryNum(0, int_part_str.rjust(BinaryNumFile.NUM_BITS, '0')).dec
    float_part = translate_float_part_to_decimal(float_part_str)
    result = int_part + float_part
    print('Float result: ' + str(result))
    return result
