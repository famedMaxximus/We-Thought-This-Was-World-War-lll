"""
mokorotlo -- the 16-bit block cipher used by the festival ticketing app.
Six rounds of (key mix, substitution, bit permutation), the last without the
permutation, followed by a final key mix.  Seven independent 16-bit round keys;
the keys are not in this file.
"""

SBOX = [2, 10, 0, 14, 6, 5, 3, 8, 7, 11, 15, 1, 12, 13, 9, 4]
PERM = [9, 15, 3, 6, 8, 0, 4, 12, 2, 14, 7, 10, 5, 1, 13, 11]    # bit i moves to bit PERM[i]
ROUNDS = 6


def substitute(x):
    return sum(SBOX[(x >> (4 * n)) & 15] << (4 * n) for n in range(4))


def permute(x):
    return sum(((x >> i) & 1) << PERM[i] for i in range(16))


def encrypt_block(x, keys):
    assert len(keys) == ROUNDS + 1
    for r in range(ROUNDS):
        x = substitute(x ^ keys[r])
        if r < ROUNDS - 1:
            x = permute(x)
    return x ^ keys[ROUNDS]
