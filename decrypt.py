
from encryptionProject.image_recognition.functions_and_constants import cipher, get_index, arr_to_int, get_key


def decrypt(Q):
    def decrypt_np(string):
        neg = False
        if string[0] == '-':
            neg = True
            string = string[1:]
        ciper_data = []
        decoded_array = []
        for c in string:
            ciper_data.append(get_key(cipher, c))
        # print((ciper_data))
        for i in range(3, len(ciper_data), 3):
            # print(ciper_data[i-6:i])
            code = arr_to_int(ciper_data[i - 3:i]) - (i - 3) // 3
            # print(code)
            decoded_array.append(get_index(Q, code))
        # print(decoded_array)
        decoded = arr_to_int(decoded_array)
        if neg:
            decoded *= -1
        return decoded / 1e5
    return decrypt_np
