from umbral.curve import SECP256K1
from umbral import (
    keys,
    signing,
    config,
    pre
)
from cryptography.exceptions import InvalidTag
import random


config.set_default_curve(SECP256K1)

alices_private_key = keys.UmbralPrivateKey.gen_key()
alices_public_key = alices_private_key.get_pubkey()

alices_signing_key = keys.UmbralPrivateKey.gen_key()
alices_verifying_key = alices_signing_key.get_pubkey()
alices_signer = signing.Signer(private_key=alices_signing_key)

bobs_private_key = keys.UmbralPrivateKey.gen_key()
bobs_public_key = bobs_private_key.get_pubkey()

plaintext = b'Proxy Re-encryption is cool!'
ciphertext, capsule = pre.encrypt(alices_public_key, plaintext)

cleartext = pre.decrypt(
    ciphertext=ciphertext,
    capsule=capsule,
    decrypting_key=alices_private_key
)

kfrags = pre.generate_kfrags(
    delegating_privkey=alices_private_key,
    signer=alices_signer,
    receiving_pubkey=bobs_public_key,
    threshold=10,
    N=20
)

#<fetch the capsule through a side-channel>
bobs_capsule = capsule

try:
    fail = pre.decrypt(
        ciphertext=ciphertext,
        capsule=capsule,
        decrypting_key=bobs_private_key
    )
except InvalidTag:
    print("Bob can`t decpryt message as expected")

#<fetch keyfrags through a side-channel>
kfrags = random.sample(kfrags, 10)

assert (True, True, True) == capsule.set_correctness_keys(
    delegating=alices_public_key,
    receiving=bobs_public_key,
    verifying=alices_verifying_key
)

# Bob's cfrag collection

assert (False, False, False) == capsule.set_correctness_keys(
    delegating=alices_public_key,
    receiving=bobs_public_key,
    verifying=alices_verifying_key
)

for cfrag in cfrags:
    capsule.attach_cfrag(cfrag)

cleartext = pre.decrypt(
    ciphertext=ciphertext,
    capsule=capsule,
    decrypting_key=bobs_private_key
)

assert plaintext == cleartext
