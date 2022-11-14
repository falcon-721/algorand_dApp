import json
import base64
from algosdk import account, mnemonic, constants
from algosdk.v2client import algod
from algosdk.future import transaction
from scripts.defaults import algorand_local_ip_address, algorand_token
from scripts.defaults import algorand_test_ip_address, algorand_main_ip_address


def generate_algorand_key_pair():
    """
    A method to generate an algorand key pair
    """
    global private_key, my_address
    private_key, my_address = account.generate_account()
    print("My address: {}".format(my_address))
    print("My private key: {}".format(private_key))
    print("My passphrase: {}".format(mnemonic.from_private_key(private_key)))
    print("Private key type: {}".format(type(private_key)))


def get_mnemonic(private_key: str) -> str:
    """
    A method to get mnemonic given a private key

    Parameters
    =--------=
    private_key: string
        The private key from which we are going to generate th mnemonic

    Returns
    =-----=
    the_mnemonic: string
        The generated mnemonic
    """
    print('Private key: *******')
    print(f"Mnemonic key: {mnemonic.from_private_key(private_key)}")
    the_mnemonic = mnemonic.from_private_key(private_key)
    return the_mnemonic


def make_transaction(private_key, sender_address, receiver_address,
                     amount_to_send):
    """
    A method to make a transaction between two accounts

    Parameters
    =--------=
    private_key: string
        The senders private key to sign the transaction
    sender_address: string
        The senders address from which to make the transaction
    receiver_address: string
        The receivers address which receives the transaction
    """
    # connect with a client given the token and address of the network
    algod_client = algod.AlgodClient(algorand_token, algorand_test_ip_address)

    # print basic sender info
    print("\nSender address: {}".format(sender_address))
    account_info = algod_client.account_info(sender_address)
    print("Account balance: {} microAlgos".format(account_info.get('amount')))

    # build transaction
    params = algod_client.suggested_params()
    # comment out the next two (2) lines to use suggested fees
    params.flat_fee = constants.MIN_TXN_FEE
    params.fee = 1000
    # amount = 100000
    amount = amount_to_send
    note = "Initial transaction example".encode()

    # print basic receiver info
    print("\nReceiver address: {}".format(receiver_address))
    account_info = algod_client.account_info(receiver_address)
    print("Account balance: {} microAlgos".format(account_info.get('amount')))

    unsigned_txn = transaction.PaymentTxn(sender_address, params,
                                          receiver_address, amount, None, note)

    # sign transaction
    signed_txn = unsigned_txn.sign(private_key)

    # submit transaction
    tx_id = algod_client.send_transaction(signed_txn)
    print("Signed transaction with tx_id: {}".format(tx_id))

    # wait for confirmation
    try:
        confirmed_txn = transaction.wait_for_confirmation(algod_client, tx_id,
                                                          4)
    except Exception as err:
        print("A damn error occurred: {}".format(err))
        return

    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
    print("Decoded note: {}".format(base64.b64decode(
        confirmed_txn["txn"]["txn"]["note"]).decode()))

    print("Starting Account balance: {} microAlgos".format(
        account_info.get('amount')))
    print("Amount transferred: {} microAlgos".format(amount))
    print("Fee: {} microAlgos".format(params.fee))

    account_info = algod_client.account_info(sender_address)
    print("Final Account balance: {} microAlgos".format(
        account_info.get('amount')) + "\n")
    return True


def get_balance(account_address: str) -> int:
    """
    A method that tells the accounts balance given an account address

    Parameters
    =--------=
    account_address: string
        The account address

    Returns
    =-----=
    account_balance : integer
        The accounts balance
    """
    # create a client to interact with
    client = algod.AlgodClient(algorand_token, algorand_test_ip_address)
    # client = algod.AlgodClient(algorand_token, algorand_main_ip_address)
    account_info = client.account_info(account_address)
    print(json.dumps(account_info, indent=4))

    account_balance = account_info.get('amount')
    print('Account balance: {} microAlgos'.format(account_balance))
    return account_balance


def get_records():
    """
    A method to get all account related records
    TODO: get the records of the given network in here
    """
    return 'one'


print('--- transaction helpers over and out ---')
