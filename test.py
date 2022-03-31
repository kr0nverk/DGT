#!/usr/bin/python
"""Simple script generator

This script generates a transaction on a specific node
with the following restrictions:

 - cluster, Cluster number,
 - node, Node number,
 - function, set/inc/dec/trans,
 - number, Transaction number,
 - wallet, Wallet id,
 - count, Wallet count,
 - wallet2, Wallet2 id.

"""
import sys
import argparse
import paramiko
import time

username = "user"
password = "1qaz@WSX"
topology_nodes = ["11", "12", "31", "21"]
topology_hosts = ["172.27.216.170", "172.27.216.170", "172.27.216.170", "172.27.216.170"]


class CustomFormatter(argparse.RawDescriptionHelpFormatter, argparse.ArgumentDefaultsHelpFormatter):
    pass

def ParseArgs(args=sys.argv[1:]):
    """Parse arguments"""

    parser = argparse.ArgumentParser(description=sys.modules[__name__].__doc__, formatter_class=CustomFormatter)

    parser.add_argument('cluster', type=int, help='Cluster number')
    parser.add_argument('node', type=int, help='Node number')

    g = parser.add_argument_group("transaction settings")
    g.add_argument('-f', '--function', metavar="N", default="set", help='set/inc/dec/trans')
    g.add_argument('-n', '--number', metavar="N", default=1, type=int, help='Transactions number')
    g.add_argument('-w', '--wallet', metavar="N", default="BGT_1", help='Wallet id')
    g.add_argument('-c', '--count', metavar="N", default=100, type=int, help='Wallet count')
    g.add_argument('-w2', '--wallet2', metavar="N", default="BGT_2", help='Wallet2 id')

    return parser.parse_args()

def SetWallet(cluster, node, wallet, count):
    """Sets the bgt value"""

    console = ("docker exec -it shell-dgt-c{cluster}-{node} ").format(cluster=cluster, node=node)
    set_wallets = ("bgt set {wallet} {count}").format(wallet=wallet, count=count)
    command = console + set_wallets

    return(command)

def IncWallet(cluster, node, wallet, count):
    """increases bgt value"""

    console = ("docker exec -it shell-dgt-c{cluster}-{node} ").format(cluster=cluster, node=node)
    inc_wallets = ("bgt inc {wallet} {count}").format(wallet=wallet, count=count)
    command = console + inc_wallets

    return(command)

def DecWallet(cluster, node, wallet, count):
    """reduces dgt value"""

    console = ("docker exec -it shell-dgt-c{cluster}-{node} ").format(cluster=cluster, node=node)
    dec_wallets = ("bgt dec {wallet} {count}").format(wallet=wallet, count=count)
    command = console + dec_wallets

    return(command)

def TransWallet(cluster, node, from_wallet, count, to_wallet):
    """ transfers tokens from wallet to wallet"""

    console = ("docker exec -it shell-dgt-c{cluster}-{node} ").format(cluster=cluster, node=node)
    trans_wallets = ("bgt trans {from_wallet} {count} {to_wallet}").format(from_wallet=from_wallet, count=count, to_wallet=to_wallet)
    command = console + trans_wallets

    return (command)

def RemoteClient(hostname, commands):
    """Connect to SSH Server"""

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname, username=username, password=password)
    except:
        print("[!] Cannot connect to SSH Server")
        exit()

    for i, command in enumerate(commands):
        print("Executing the Command {n}:".format(n=i+1))
        stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
        #time.sleep(1)
        print(stdout.read().decode())
        err = stderr.read().decode()
        if err:
            print(err)

    ssh.close()

def CreateCommands(cluster, node, function, n, wallet, count, to_wallet):
    """Create Commands"""

    commands = []

    if function == "set":
        for i in range(n):
            commands.append(SetWallet(cluster, node, wallet, count))
    elif function == "inc":
        for i in range(n):
            commands.append(IncWallet(cluster, node, wallet, count))
    elif function == "dec":
        for i in range(n):
            commands.append(DecWallet(cluster, node, wallet, count))
    elif function == "trans":
        for i in range(n):
            commands.append(TransWallet(cluster, node, wallet, count, to_wallet))
    else:
        print("[!] Wrong Create Command")
        exit()

    return commands

def Main():
    """Main"""

    option = ParseArgs()

    cluster_node = str(option.cluster) + str(option.node)
    hostname = topology_hosts[topology_nodes.index(cluster_node)]
    #print(hostname)

    commands = CreateCommands(option.cluster, option.node, option.function, option.number, option.wallet, option.count, option.wallet2)
    #print(commands)

    RemoteClient(hostname, commands)

if __name__ == '__main__':
    Main()
