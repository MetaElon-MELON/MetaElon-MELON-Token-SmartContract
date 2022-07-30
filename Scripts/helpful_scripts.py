from brownie import accounts, network, config


def getAccount():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.load("MEfirefox")
