plaintext=input("Enter a one-word,lowercase message: ")
distance=int(input("Enter the distance value: "))
code=""
for ch in plaintext:
  ordvalue=ord(ch)
  ciphervalue=ordvalue+distance
  if ciphervalue>ord('z'):
    ciphervalue = ord('a') + (ciphervalue - ord('z') - 1) # Corrected calculation for wrap-around
  code+=chr(ciphervalue)

code1 = ""
for ch in code:
    ordvalue = ord(ch)
    ciphervalue = ordvalue - distance


    if ciphervalue < ord('a'):
        ciphervalue = ord('z') - (ord('a') - ciphervalue - 1)

    code1 += chr(ciphervalue)

print("\n\t ENCRYPTION \n")
print("The given text is : " ,plaintext)
print("Encrypted text is : " ,code)
print("\n\t DECRYPTION \n")
print("The given text is : " ,code)
print("Decrypted text is : " ,code1)
