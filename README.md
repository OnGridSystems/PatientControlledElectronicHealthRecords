# Patient-controlled electronic health records platform (EHR)

A client-server prototype illustrating prospective DApp operation principles for
self-sovereign medical data. Private/Public key cryptography and encryption-decapsulation
 technologies offer a promising solution to the problems of medical record-keeping 
 systems which are currently centralizsed and insecure.
It's possible to push ownership of health records from centralized service providers to individuals.

Decentralised Patient-Controlled electronic health records (PCEDR) can be buil using
* blockchain with arbitrary code execution capabilities (smart-contracts) like Ethereum
* decentralised global content-addressable storage like swarm/ipfs or/and channels/queues/messengers like plasma/whisper/libp2p transports
* decentralised cryptography-based access-control and key management layer with incentivised reencryption engines.

We use Django web framework for modeling the components mentioned above.

## System description
It's a Django webserver with pythonic API and RESTful HTTP interface illustrating abstract call flow for record-keeping, 
access-control and reencryption. [Tests](blob/master/re_encryption/tests/test_data_sending.py) cover the following case:
* Patient and Recepient register their entities (public keys) in the framework
* Patient populates its medical records encrypted with its public key
* Upon receiving disclosure request Patient approves it giving the permission to read
* Recepient gets the data recapsulated for its private key
* Recipient now able to extract plaintext from the capsule

Some screenshots of REST client you can find [here](img/)

## HowTo

### Buidl

```
docker -t pcehr build .
```

### Test

```
docker run -it pcehr test -v 3
```

### Run REST API webserver

```
docker run -p 8000:8000/tcp -it pcehr
```
API endpoints (opens with browser, thanks Django Rest Framework tool)
* [http://127.0.0.1:8000/patients/signup/](http://127.0.0.1:8000/patients/signup/)
* [http://127.0.0.1:8000/patients/kfrags/](http://127.0.0.1:8000/patients/kfrags/)
* [http://127.0.0.1:8000/patients/delegations/make/](http://127.0.0.1:8000/patients/delegations/make/)
* [http://127.0.0.1:8000/recepients/signup/](http://127.0.0.1:8000/recepients/signup/)
* [http://127.0.0.1:8000/records/add/](http://127.0.0.1:8000/records/add/)
* [http://127.0.0.1:8000/re_encryptions/](http://127.0.0.1:8000/re_encryptions/)
* [http://127.0.0.1:8000/me/records/](http://127.0.0.1:8000/me/records/)

## Authors

* [Demyan Havdun](https://github.com/Utyuzhok), [OnGrid Systems](https://github.com/OnGridSystems)
* [Kirill Varlamov](https://github.com/ongrid), [OnGrid Systems](https://github.com/OnGridSystems)