def uuid_encode(self, uuid):
    """
    Encodes a UUID into a string (LSB first) according to the alphabet
    If leftmost (MSB) bits 0, string might be shorter

    """
    alphabet = list('23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz')
    unique_id = uuid.int
    output = ''
    while unique_id:
        unique_id, digit = divmod(unique_id, self._alpha_len)
        output += self.alphabet[digit]
    return output
