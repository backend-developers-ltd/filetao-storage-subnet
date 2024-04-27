# The MIT License (MIT)
# Copyright © 2023 Yuma Rao
# Copyright © 2023 philanthrope

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import typing
import pydantic
import bittensor as bt


_UNSET = object()


class ShortReprMixin:
    SHORT_REPR_FIELDS: typing.ClassVar[typing.Set[str]] = set()

    def __repr_args__(self, short: bool = False):
        repr_args = []
        for key, value in super().__repr_args__():
            if short and value == self._get_field_default(key):
                continue
            if key in self.SHORT_REPR_FIELDS:
                value_repr = str(value)
                if len(value_repr) > 12:
                    value = value_repr[:12] + "…"
            repr_args.append((key, value))
        return repr_args

    def _get_field_default(self, field_name: str):
        return getattr(self.__class__.__fields__.get(field_name), "default", _UNSET)

    def __repr_str__(self, sep=", ", short: bool = False):
        return sep.join(
            f"{key}={value!r}" for key, value in self.__repr_args__(short=short)
        )

    def __str__(self):
        return f'{self.__repr_name__()}({self.__repr_str__(", ", short=True)})'


class FileTaoSynapseMixin(ShortReprMixin):
    def __repr_args__(self, short: bool = False):
        repr_args = super().__repr_args__(short=short)
        for field in ("dendrite", "axon"):
            value = getattr(self, field)
            if value != self._get_field_default(field):
                repr_args.insert(0, (field, value.dict()))
        return repr_args


# Basically setup for a given piece of data
class Store(FileTaoSynapseMixin, bt.Synapse):
    # Data to store
    encrypted_data: str  # base64 encoded string of encrypted data (bytes)

    # Setup parameters
    curve: str  # e.g. P-256
    g: str  # base point   (hex string representation)
    h: str  # random point (hex string representation)

    seed: typing.Union[
        str, int, bytes
    ]  # random seed (bytes stored as hex) for the commitment

    # Return signature of received data
    randomness: typing.Optional[int] = None
    commitment: typing.Optional[str] = None
    signature: typing.Optional[bytes] = None
    commitment_hash: typing.Optional[str] = None  # includes seed
    ttl: typing.Optional[int] = None  # time to live (in seconds)

    required_hash_fields: typing.List[str] = pydantic.Field(
        [
            "curve",
            "g",
            "h",
            "seed",
            "randomness",
            "commitment",
            "signature",
            "commitment_hash",
        ],
        title="Required Hash Fields",
        description="A list of required fields for the hash.",
        allow_mutation=False,
    )

    SHORT_REPR_FIELDS: typing.ClassVar[typing.Set[str]] = {
        "encrypted_data",
        "curve",
        "g",
        "h",
        "seed",
        "randomness",
        "commitment",
        "commitment_hash",
    }


class StoreUser(FileTaoSynapseMixin, bt.Synapse):
    # Data to store
    encrypted_data: str  # base64 encoded string of encrypted data (bytes)
    encryption_payload: str  # encrypted json serialized bytestring of encryption params

    data_hash: typing.Optional[str] = None  # Miner storage lookup key
    ttl: typing.Optional[int] = None  # time to live (in seconds)

    required_hash_fields: typing.List[str] = pydantic.Field(
        ["encrypted_data", "encryption_payload"],
        title="Required Hash Fields",
        description="A list of required fields for the hash.",
        allow_mutation=False,
    )

    SHORT_REPR_FIELDS: typing.ClassVar[typing.Set[str]] = {
        "data_hash",
        "encrypted_data",
        "encryption_payload",
    }


class Challenge(FileTaoSynapseMixin, bt.Synapse):
    # Query parameters
    challenge_hash: str  # hash of the data to challenge
    challenge_index: int  # block indices to challenge
    chunk_size: int  # bytes (e.g. 1024) for how big the chunks should be

    # Setup parameters
    g: str  # base point   (hex string representation)
    h: str  # random point (hex string representation)
    curve: str
    seed: typing.Union[str, int]  # random seed for the commitment

    # Returns
    # - commitment hash (hex string) hash( hash( data + prev_seed ) + seed )
    # - commitment (point represented as hex string)
    # - data chunk (base64 encoded string of bytes)
    # - random value (int)
    # - merkle proof (List[Dict[<left|right>, hex strings])
    # - merkle root (hex string)
    commitment_hash: typing.Optional[str] = None
    commitment_proof: typing.Optional[str] = None
    commitment: typing.Optional[str] = None
    data_chunk: typing.Optional[bytes] = None
    randomness: typing.Optional[int] = None
    merkle_proof: typing.Optional[
        typing.Union[typing.List[typing.Dict[str, str]], str]
    ] = None
    merkle_root: typing.Optional[str] = None

    required_hash_fields: typing.List[str] = pydantic.Field(
        [  # TODO: can this be done? I want to verify that these values haven't changed, but
            # they are None intially...
            "commitment_hash",
            "commitment_proof",
            "commitment",
            "data_chunk",
            "randomness",
            "merkle_proof",
            "merkle_root",
        ],
        title="Required Hash Fields",
        description="A list of required fields for the hash.",
        allow_mutation=False,
    )

    SHORT_REPR_FIELDS: typing.ClassVar[typing.Set[str]] = {
        "challenge_hash",
        "challenge_index",
        "chunk_size",
        "g",
        "h",
        "curve",
        "seed",
        "commitment_hash",
        "commitment_proof",
        "commitment",
        "data_chunk",
        "randomness",
        "merkle_proof",
        "merkle_root",
    }


class Retrieve(FileTaoSynapseMixin, bt.Synapse):
    # Where to find the data
    data_hash: str  # Miner storage lookup key
    seed: str  # New random seed to hash the data with

    # Fetched data and proof
    data: typing.Optional[str] = None
    commitment_hash: typing.Optional[str] = None
    commitment_proof: typing.Optional[str] = None

    required_hash_fields: typing.List[str] = pydantic.Field(
        ["data", "data_hash", "seed", "commtiment_proof", "commitment_hash"],
        title="Required Hash Fields",
        description="A list of required fields for the hash.",
        allow_mutation=False,
    )

    SHORT_REPR_FIELDS: typing.ClassVar[typing.Set[str]] = {
        "data_hash",
        "seed",
        "data",
        "commitment_hash",
        "commitment_proof",
    }


class RetrieveUser(FileTaoSynapseMixin, bt.Synapse):
    # Where to find the data
    data_hash: str  # Miner storage lookup key

    # Fetched data to return along with AES payload in base64 encoding
    encrypted_data: typing.Optional[str] = None
    encryption_payload: typing.Optional[str] = None

    required_hash_fields: typing.List[str] = pydantic.Field(
        ["data_hash"],
        title="Required Hash Fields",
        description="A list of required fields for the hash.",
        allow_mutation=False,
    )

    SHORT_REPR_FIELDS: typing.ClassVar[typing.Set[str]] = {
        "data_hash",
        "encrypted_data",
        "encryption_payload",
    }


class DeleteUser(bt.Synapse):
    # Where to find the data
    data_hash: str  # Miner storage lookup key
    encryption_payload: str # encrypted json serialized bytestring of encryption params

    deleted: bool = False

    required_hash_fields: typing.List[str] = pydantic.Field(
        ["data_hash"],
        title="Required Hash Fields",
        description="A list of required fields for the hash.",
        allow_mutation=False,
    )
