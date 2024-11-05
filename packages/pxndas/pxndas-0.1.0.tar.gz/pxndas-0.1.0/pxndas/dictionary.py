hex_bin_dict = {
    '0': '0000', '1': '0001', '2': '0010', '3': '0011',
    '4': '0100', '5': '0101', '6': '0110', '7': '0111',
    '8': '1000', '9': '1001', 'A': '1010', 'B': '1011',
    'C': '1100', 'D': '1101', 'E': '1110', 'F': '1111'
}

def hex_to_bin(hex_num):
    
    bin_num=''
    for i in hex_num.upper():
        bin_num+=hex_bin_dict[i]

    return bin_num
    

hex_num = input("Enter a hexadecimal number: ")

print("The binary equivalent of hexadecimal number:",hex_to_bin(hex_num))
