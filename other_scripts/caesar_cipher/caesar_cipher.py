import sys

class CaesarCipher:
    def __init__(self, **kwargs):
        if kwargs is not None:
            try:
                self.shift = kwargs['shift']
                self.message = kwargs['message']
            except:
                sys.exit("Must provide 'shift' amount, and 'message'")

        print ('---------------------------------')
        print('abcdefghijklmnopqrstuvwxyz')
        print(self.encrypt('abcdefghijklmnopqrstuvwxyz'))
        print ('---------------------------------')
        print('Encrypted Message: {}'.format(self.encrypt(self.message)))

    def get_ascii_value(self, char):
        ascii_min = 97
        ascii_max = 122
        if (ord(char) >= ascii_min and ord(char) <= ascii_max):
            shifted_char_ascii = ord(char) + int(self.shift)

            if shifted_char_ascii < ascii_min:
                return ascii_max - (ascii_min - shifted_char_ascii - 1)
            elif shifted_char_ascii > ascii_max:
                return ascii_min + (shifted_char_ascii - ascii_max - 1)
            else:
                return shifted_char_ascii
        else:
            return ord(char)

    def encrypt(self, msg):
        encrypted_msg = ""
        for char in msg.lower():

            shifted_char = self.get_ascii_value(char)
            encrypted_msg += chr(shifted_char)

        return encrypted_msg



print('Caesar Cipher')
print('------------------------------')
shift_amt = input('Shift Amount (-25 to 25): ')
msg = input('Message: ')

CaesarCipher(shift=shift_amt, message=msg)
