import bip39
from solana.rpc.api import Keypair
from mnemonic import Mnemonic
from solana_account_sdk.core import decorator
import json


@decorator
def format_mnemonic(mnemonic_words, _debug=False, _dpath=''):
    seed = bip39.phrase_to_seed(mnemonic_words)

    if _dpath:
        keypair = Keypair.from_seed_and_derivation_path(seed, dpath=_dpath)
    else:
        keypair = Keypair.from_seed(seed[:32])
    format_data = {
        'mnemonic': mnemonic_words,
        'address': keypair.pubkey().__str__(),
        'bs58': keypair.__str__(),
        'uint8': keypair.to_bytes_array()
    }
    if _debug:
        format_json_data = json.dumps(format_data, indent=4)
        print(format_json_data)

    return format_data


def create_account(_mnemonic_words=12, _dpath='', _debug=False):
    _mnemonic = Mnemonic(language='english')
    if _mnemonic_words not in [12, 24]:
        print('仅支持<12>/<24>格式类型助记词')
        return
    mnemonic_words_length_mapping = {
        12: 128,
        24: 256,
    }
    mnemonic_words = _mnemonic.generate(strength=mnemonic_words_length_mapping.get(_mnemonic_words))
    account_info = format_mnemonic(mnemonic_words, _dpath=_dpath, _debug=_debug)
    return account_info

