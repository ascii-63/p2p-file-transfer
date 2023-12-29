# def fnv1a_hash(key):
#     prime = 16777619
#     hash_value = 2166136261
#     for char in key.encode('utf-8'):
#         hash_value ^= char
#         hash_value *= prime
#     return hash_value

# # Example usage:
# key = "example_key"
# hashed_value_fnv1a = fnv1a_hash(key)
# print(f"Key: {key}\nFNV-1a Hashed Value: {hashed_value_fnv1a}")

import hashlib


def hash_key_sha1(key):
    sha1_hash = hashlib.sha1(key.encode('utf-8')).hexdigest()
    return sha1_hash


# Example usage:
key = "example_key"
hashed_value_sha1 = hash_key_sha1(key)
print(f"Key: {key}\nSHA-1 Hashed Value: {hashed_value_sha1}")
