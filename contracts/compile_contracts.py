#!/usr/bin/env python
import json
import os
from solc import compile_standard


CONTRACTS_DIR = os.path.dirname(os.path.abspath(__file__))
SOLIDITY_DIR = os.path.dirname(CONTRACTS_DIR)


def compile_contract(contract_name):
    contract_source = os.path.join(CONTRACTS_DIR, f'{contract_name}.sol')
    if not os.path.isfile(contract_source):
        raise FileNotFoundError(f'Expected {contract_source} to exist.')

    compiled = compile_standard({
        'language': 'Solidity',
        'sources': {
            contract_name: {
                'urls': [contract_source]
            }
        },
        'settings': {
            'remappings': ["openzeppelin-solidity=%s" % os.path.join(SOLIDITY_DIR, 'openzeppelin-solidity')],
            'outputSelection': {
                contract_name: {
                    contract_name: ['abi', 'evm.bytecode.object']
                }
            }
        }
    }, allow_paths=SOLIDITY_DIR)

    abi = compiled['contracts'][contract_name][contract_name]['abi']
    bytecode = compiled['contracts'][contract_name][contract_name]['evm']['bytecode']['object']

    output_filename = os.path.join(CONTRACTS_DIR, f'{contract_name}.json')

    with open(output_filename, 'w') as f:
        json.dump({'abi': abi, 'bin': bytecode}, f)


def main():
    compile_contract('PCEHR')


if __name__ == '__main__':
    main()
