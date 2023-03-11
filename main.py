import BinaryFloatFile
import BinaryNumFile


def main():
    while True:
        """num1 = BinaryNumFile.BinaryNum(int(input("Enter the first int number: ")))
        num1.print_num()
        num2 = BinaryNumFile.BinaryNum(int(input("Enter the second int number: ")))
        num2.print_num()"""

        """print('Binary sum: ')
        BinaryNumFile.binary_add(num1, num2).print_num()
        print('Binary sub: ')
        BinaryNumFile.binary_sub(num1, num2).print_num()
        print('Binary mult: ')
        BinaryNumFile.binary_mult(num1, num2).print_num()
        print('Binary div: ')
        BinaryNumFile.binary_div(num1, num2).print_num()"""

        num3 = float(input("Enter the first float number: "))
        num4 = float(input("Enter the second float number: "))

        print('Float binary sum: ')
        BinaryFloatFile.binary_add_float(num3, num4)

        if int(input("Do you want to continue? 1 — continue, 2 — stop: ")) == 1:
            continue
        else:
            break


if __name__ == '__main__':
    main()