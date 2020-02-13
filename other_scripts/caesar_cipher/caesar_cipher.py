import sys

class CaesarCipher:
    def __init__(self, **kwargs):
        if kwargs is not None:
            if self.is_shift_valid(kwargs['shift']):
                self.shift = kwargs['shift']
            else:
                sys.exit("Must provide a valid 'shift' amount")

            if len(kwargs['message']) > 0:
                self.message = kwargs['message']
            else:
                sys.exit("Must provide a 'message'")

        print('---------------------------------')
        print('abcdefghijklmnopqrstuvwxyz')
        print(self.encrypt('abcdefghijklmnopqrstuvwxyz'))
        print('---------------------------------')
        print('Encrypted Message: {}'.format(self.encrypt(self.message)))

    def is_shift_valid(self, shift_amt):
        """Returns true if the shift value is valid"""
        try:
            if (int(shift_amt)
                and int(shift_amt) <= 25
                and int(shift_amt) >= -25):
                return True;
        except ValueError:
            return False;

    def get_ascii_value(self, char):
        """Get the shifted ascii character"""
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

    def encrypt(self, orig_msg):
        """Encrypt the message using the specified shift amount"""
        encrypted_msg = ""
        for char in orig_msg.lower():

            shifted_char = self.get_ascii_value(char)
            encrypted_msg += chr(shifted_char)

        return encrypted_msg



print('Caesar Cipher')
print('------------------------------')
SHIFT_AMT = input('Shift Amount (-25 to 25): ')
MSG = input('Message: ')

CaesarCipher(shift=SHIFT_AMT, message=MSG)
