import sys

class CaesarCipher:
    def __init__(self, **kwargs):
        if kwargs is not None:
            try:
                self.shift = kwargs['shift']
                self.message = kwargs['message']
            except:
                sys.exit("Must provide 'shift' amount, and 'message'")

        self.encrypt()

    def encrypt(self):
        print('Original Message: {}'.format(self.message))
        print('Encrypted Message: ')

print('Caesar Cipher')
print('------------------------------')
shiftAmt = input('Shift Amount: ')
msg = input('Message: ')

CaesarCipher(shift=shiftAmt, message=msg)
