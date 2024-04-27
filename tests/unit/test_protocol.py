import bittensor
from storage import protocol


class TestStore:
    def test_str__empty(self):
        synapse = protocol.Store(
            encrypted_data="data",
            curve="curve",
            g="g",
            h="h",
            seed="seed",
        )
        assert str(synapse) == (
            "Store(encrypted_data='data', " "curve='curve', g='g', h='h', seed='seed')"
        )

    def test_str__lengthy(self):
        synapse = protocol.Store(
            encrypted_data="data",
            curve="curve",
            g="g",
            h="h",
            seed="seed",
            ttl=10,
            commitment="commitment",
            commitment_hash="commitment_hash" * 10,
            axon=bittensor.TerminalInfo(ip="127.0.0.1"),
            dendrite=bittensor.TerminalInfo(ip="127.0.0.1"),
        )
        assert str(synapse) == (
            "Store(axon={'status_code': None, 'status_message': None, 'process_time': "
            "None, 'ip': '127.0.0.1', 'port': None, 'version': None, 'nonce': None, "
            "'uuid': None, 'hotkey': None, 'signature': None}, dendrite={'status_code': "
            "None, 'status_message': None, 'process_time': None, 'ip': '127.0.0.1', "
            "'port': None, 'version': None, 'nonce': None, 'uuid': None, 'hotkey': None, "
            "'signature': None}, encrypted_data='data', curve='curve', g='g', h='h', "
            "seed='seed', commitment='commitment', commitment_hash='commitment_h…', "
            "ttl=10)"
        )


class TestRetrieve:
    def test_str__empty(self):
        synapse = protocol.Retrieve(data_hash="data_hash", seed="seed")
        assert str(synapse) == "Retrieve(data_hash='data_hash', seed='seed')"

    def test_str__lengthy(self):
        synapse = protocol.Retrieve(
            data_hash="data_hash",
            seed="seed",
            data="data",
            commitment_hash="commitment_hash" * 10,
            commitment_proof="commitment_proof" * 10,
        )
        assert str(synapse) == (
            "Retrieve(data_hash='data_hash', seed='seed', data='data', "
            "commitment_hash='commitment_h…', commitment_proof='commitment_p…')"
        )


class TestStoreUser:
    def test_str__empty(self):
        synapse = protocol.StoreUser(
            encrypted_data="data", encryption_payload="payload"
        )
        assert str(synapse) == (
            "StoreUser(encrypted_data='data', encryption_payload='payload')"
        )

    def test_str__lengthy(self):
        synapse = protocol.StoreUser(
            encrypted_data="data" * 10,
            encryption_payload="payload" * 10,
            data_hash="data_hash" * 10,
            ttl=3600,
        )
        assert str(synapse) == (
            "StoreUser(encrypted_data='datadatadata…', "
            "encryption_payload='payloadpaylo…', data_hash='data_hashdat…', ttl=3600)"
        )


# Adding tests for the Challenge class
class TestChallenge:
    def test_str__empty(self):
        synapse = protocol.Challenge(
            challenge_hash="hash",
            challenge_index=1,
            chunk_size=1024,
            g="g",
            h="h",
            curve="curve",
            seed="seed",
        )
        expected_str = (
            "Challenge(challenge_hash='hash', challenge_index=1, chunk_size=1024, "
            "g='g', h='h', curve='curve', seed='seed')"
        )
        assert str(synapse) == expected_str

    def test_str__lengthy(self):
        synapse = protocol.Challenge(
            challenge_hash="hash",
            challenge_index=1,
            chunk_size=1024,
            g="g",
            h="h",
            curve="curve",
            seed="seed",
            commitment_hash="commitment_hash",
            commitment_proof="commitment_proof",
            commitment="commitment",
            data_chunk=b"data_chunk" * 10,
            randomness=1234,
            merkle_proof=[{"left": "abc", "right": "def"}],
            merkle_root="merkle_root",
        )
        assert str(synapse) == (
            "Challenge(challenge_hash='hash', challenge_index=1, chunk_size=1024, g='g', "
            "h='h', curve='curve', seed='seed', commitment_hash='commitment_h…', "
            "commitment_proof='commitment_p…', commitment='commitment', "
            "data_chunk=\"b'data_chunk…\", randomness=1234, merkle_proof=\"[{'left': "
            "'a…\", merkle_root='merkle_root')"
        )


class TestRetrieveUser:
    def test_str__empty(self):
        synapse = protocol.RetrieveUser(data_hash="data_hash")
        assert str(synapse) == "RetrieveUser(data_hash='data_hash')"

    def test_str__lengthy(self):
        synapse = protocol.RetrieveUser(
            data_hash="data_hash",
            encrypted_data="encrypted_data",
            encryption_payload="encryption_payload",
        )
        assert str(synapse) == (
            "RetrieveUser(data_hash='data_hash', encrypted_data='encrypted_da…', "
            "encryption_payload='encryption_p…')"
        )
