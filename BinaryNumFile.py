NUM_BITS = 16
BIN_ONE = '1'
BIN_ONE = BIN_ONE.rjust(NUM_BITS, '0')
BIN_ZERO = '0'
BIN_ZERO = BIN_ZERO.rjust(NUM_BITS, '0')


def binary_add_helper(number_1, number_2):
    result = ''
    carry = 0
    for i in range(NUM_BITS - 1, -1, -1):
        bit_sum = carry
        bit_sum += 1 if number_1[i] == '1' else 0
        bit_sum += 1 if number_2[i] == '1' else 0
        result = ('1' if bit_sum % 2 == 1 else '0') + result
        carry = 0 if bit_sum < 2 else 1
    return result


def binary_sub_helper(number_1, number_2):
    result = ''
    carry = 0
    for i in range(NUM_BITS - 1, - 1, - 1):
        num = int(number_1[i]) - int(number_2[i]) - carry
        if num % 2 == 1:
            result = '1' + result
        else:
            result = '0' + result
        if num < 0:
            carry = 1
        else:
            carry = 0
    if int(result) == 0:
        result = 0
    return result


class BinaryNum:
    def __init__(self, decimal_num=0, bin_additional=''):
        if bin_additional == '':
            self.dec = decimal_num
            self.bin_right = self.to_binary_right()
            self.bin_reverse = self.to_binary_reverse()
            self.bin_additional = self.to_binary_additional()
        else:
            self.bin_additional = bin_additional
            self.bin_reverse = self.from_additional_to_reverse()
            self.bin_right = self.from_reverse_to_right()
            self.dec = self.binary_to_decimal()

    def to_binary_right(self):
        answer = ""
        sign = 0
        number = self.dec
        if number == 0:
            answer = BIN_ZERO
            return answer
        if number < 0:
            sign = 1
            number *= -1
        while number:
            answer += str(number % 2)
            number = int(number / 2)
        answer = answer[::-1]
        answer = answer.rjust(NUM_BITS, '0')
        answer = str(sign) + answer[1:]
        return answer

    def binary_to_decimal(self):
        right_code = self.bin_right
        sign = int(right_code[0])
        if sign:
            right_code = '0' + right_code[1:]
        binary = int(right_code)
        decimal, i = 0, 0
        while binary != 0:
            dec = binary % 10
            decimal = decimal + dec * pow(2, i)
            binary = binary // 10
            i += 1
        if sign:
            decimal *= -1
        return decimal

    def invert_number(self, number):
        sign = number[0]
        number = number.replace('1', '2')
        number = number.replace('0', '1')
        number = number.replace('2', '0')
        number = sign + number[1:]
        return number

    def to_binary_reverse(self):
        answer = self.bin_right
        if self.dec < 0:
            return self.invert_number(answer)
        else:
            return answer

    def to_binary_additional(self):
        if self.dec >= 0:
            return self.bin_right
        answer = self.bin_reverse
        answer = binary_add_helper(answer, BIN_ONE)
        return answer

    def from_additional_to_reverse(self):
        if int(self.bin_additional[0]):
            answer = binary_sub_helper(self.bin_additional, BIN_ONE)
            return answer
        else:
            return self.bin_additional

    def from_reverse_to_right(self):
        if int(self.bin_additional[0]):
            answer = self.invert_number(self.bin_reverse)
            return answer
        else:
            return self.bin_reverse

    def print_num(self):
        print("Decimal: {0}\nBinary right: {1}\nBinary reverse: {2}\nBinary additional: {3}".format(self.dec,
                                                                                                    self.bin_right,
                                                                                                    self.bin_reverse,
                                                                                                    self.bin_additional))


def binary_add(number_1, number_2):
    if number_1.dec >= 0 and number_2.dec >= 0:
        return BinaryNum(0, binary_add_helper(number_1.bin_right, number_2.bin_right))
    elif number_1.dec > 0 > number_2.dec:
        return BinaryNum(0, binary_add_helper(number_1.bin_right, number_2.bin_additional))
    elif number_1.dec < 0 < number_2.dec:
        return BinaryNum(0, binary_add_helper(number_1.bin_additional, number_2.bin_right))
    elif number_1.dec < 0 and number_2.dec < 0:
        return BinaryNum(0, binary_add_helper(number_1.bin_additional, number_2.bin_additional))


def binary_sub(number_1, number_2):
    if number_1.dec >= 0 and number_2.dec >= 0:
        return BinaryNum(0, binary_sub_helper(number_1.bin_right, number_2.bin_right))
    elif number_1.dec > 0 > number_2.dec:
        return BinaryNum(0, binary_sub_helper(number_1.bin_right, number_2.bin_additional))
    elif number_1.dec < 0 < number_2.dec:
        return BinaryNum(0, binary_sub_helper(number_1.bin_additional, number_2.bin_right))
    elif number_1.dec < 0 and number_2.dec < 0:
        return BinaryNum(0, binary_sub_helper(number_1.bin_additional, number_2.bin_additional))


def binary_div_helper(number_1, number_2):
    result = ''
    temp_decreased = '0'
    difference = 0
    for i in range(len(number_1)):
        if int(number_2) > int(temp_decreased):
            result += '0'
            temp_decreased += number_1[i]
        else:
            temp_decreased = temp_decreased.rjust(NUM_BITS, '0')
            difference = binary_sub_helper(temp_decreased, number_2)
            if difference == 0:
                temp_decreased = number_1[i]
                result += '1'
            else:
                difference = str(difference).lstrip('0')
                result += '1'
                temp_decreased = difference + number_1[i]
    if int(temp_decreased) != 0:
        result = result + '1'
    else:
        result = result + '0'
    return result[1:]


def binary_mult_helper(number_1, count):
    result = number_1.bin_additional
    for num in range(count - 1):
        result = binary_add_helper(result, number_1.bin_additional)
    return result


def binary_mult(number_1, number_2):
    if number_1.dec == 0 or number_2.dec == 0:
        return BinaryNum(0)
    elif number_1.dec > 0 and number_2.dec > 0:
        return BinaryNum(0, binary_mult_helper(number_1, number_2.dec))
    elif number_1.dec < 0 and number_2.dec < 0:
        return BinaryNum(0, binary_mult_helper(BinaryNum(number_1.dec * -1), number_2.dec * -1))
    elif number_1.dec > 0 > number_2.dec:
        return BinaryNum(0, binary_mult_helper(number_2, number_1.dec))
    elif number_2.dec > 0 > number_1.dec:
        return BinaryNum(0, binary_mult_helper(number_1, number_2.dec))


def binary_div(number_1, number_2):
    try:
        if number_2.dec == 0:
            raise ZeroDivisionError
    except ZeroDivisionError:
        print("ZeroDivisionError")
        return BinaryNum(0)
    if number_1.dec == 0:
        return BinaryNum(0)
    elif number_1.dec > 0 and number_2.dec > 0:
        return BinaryNum(0, binary_div_helper(number_1.bin_right, number_2.bin_right))
    elif number_1.dec < 0 and number_2.dec < 0:
        return BinaryNum(0, binary_div_helper(BinaryNum(number_1.dec * -1).bin_right,
                                              BinaryNum(number_2.dec * -1).bin_right))
    elif number_1.dec > 0 > number_2.dec:
        quotient = BinaryNum(0, binary_div_helper(number_1.bin_right, BinaryNum(number_2.dec * -1).bin_right))
        return binary_mult(quotient, BinaryNum(-1))
    elif number_2.dec > 0 > number_1.dec:
        quotient = BinaryNum(0, binary_div_helper(BinaryNum(number_1.dec * -1).bin_right, number_2.bin_right))
        return binary_mult(quotient, BinaryNum(-1))
