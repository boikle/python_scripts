from caesar_cipher import CaesarCipher

print('Caesar Cipher')
print('------------------------------')
ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
SHIFT_AMT = input('Shift Amount (-25 to 25): ')
MSG = input('Message: ')
 
# Show Alphabet and Corresponding Cipher Text
print('------------------------------')
print('{}'.format(ALPHABET))
CaesarCipher(shift=SHIFT_AMT, message=ALPHABET)

# Convert the message
print('------------------------------')
CaesarCipher(shift=SHIFT_AMT, message=MSG)
