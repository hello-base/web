def uuid_encode(uuid):
    """
    Encodes a UUID into a string (LSB first) according to the alphabet
    If leftmost (MSB) bits 0, string might be shorter

    """
    alphabet = list('23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz')
    alpha_len = len(alphabet)

    unique_id = uuid.int
    output = ''
    while unique_id:
        unique_id, digit = divmod(unique_id, alpha_len)
        output += alphabet[digit]
    return output
