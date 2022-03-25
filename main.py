#!/usr/bin/env python3

"""Simple script generator
This script generates a transaction on a specific node
with the following restrictions:
 - cluster, Cluster number,
 - node, Node number,
 - number, Transaction number,
 - wallet, Wallet id,
 - count, Wallet count.
"""

import argparse
import sys
import os
import time

class CustomFormatter(argparse.RawDescriptionHelpFormatter,
                      argparse.ArgumentDefaultsHelpFormatter):
    pass

def parse_args(args=sys.argv[1:]):
    """Parse arguments"""

    parser = argparse.ArgumentParser(description=sys.modules[__name__].__doc__, formatter_class=CustomFormatter)

    parser.add_argument('cluster', type=int, help='Cluster number')
    parser.add_argument('node', type=int, help='Node number')

    g = parser.add_argument_group("transaction settings")
    g.add_argument('-n', '--number', metavar="N", default=0, type=int, help='Transactions number')
    g.add_argument('-w', '--wallet', metavar="N", type=int, help='Wallet id')
    g.add_argument('-c', '--count', metavar="N", default=100, type=int, help='Wallet count')

    return parser.parse_args()


def set_wallet(cluster, node, wallet, count):
    """Sets the bgt value"""

    console = f"docker exec -it shell-dgt-c{cluster}-{node} "
    creat_wallets = f"bgt set wallet_{wallet} {count}"
    cluster_long = f"{80 + cluster:02}"
    node_long = f"{7 + node:02}"
    rest_ip_http = f" http://api-dgt-c{cluster}-{node}:{cluster_long}{node_long}"

    command = console + creat_wallets

    #print(command)
    print(os.system(command))

def inc_wallet():
    """increases bgt value"""
    print()
def dec_wallet():
    """reduces dgt value"""
    print()
def trans_wallet():
    """ transfers tokens from wallet to wallet"""
    print()

if __name__ == '__main__':
    """main"""
    option = parse_args()
    if option.wallet is None:
        option.wallet = option.node

    i = 0
    count = option.count
    while True:
        set_wallet(option.cluster, option.node, option.wallet, count)
        count += 1

        i += 1
        if i == option.number:
            break
        time.sleep(1)
