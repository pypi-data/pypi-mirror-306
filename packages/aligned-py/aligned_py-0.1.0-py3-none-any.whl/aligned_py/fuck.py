from core.types import *
from sdk import *
from communication.serialization import *
import asyncio
from web3 import Web3
import requests
from eth_account import Account
import eth_account
import json
import websockets

async def main():
    rpc_api = "https://eth-holesky.g.alchemy.com/v2/rdrUy9h_eUsh0V1_r31PYbpoW2Fn4ab9"
    private_key = '0x8d76fc4c878c8a99ab611e94621c840f5ae41dbe2f3613b73c7330b604d081da'
    web3 = Web3(Web3.HTTPProvider(rpc_api))
    account = web3.eth.account.from_key(private_key)
    acc = Account.from_key(private_key)
    print(account.address)

    balance = get_balance_in_aligned(account.address, rpc_api, Network.Holesky)
    nonce = get_next_nonce(rpc_api, account.address, Network.Holesky)
    max_fee = estimate_fee(rpc_api, PriceEstimate.Instant)
    print(balance)
    print(nonce)

    response = requests.get("http://localhost:3030/generate-verification-data")
    data = response.json()
    ver_data = VerificationData(
        proving_system=ProvingSystemId.SP1,
        proof=bytes(data["verification_data"]["proof"]),
        public_input=data["verification_data"]["pub_input"],
        verification_key=data["verification_data"]["verification_key"],
        vm_program_code=bytes(data["verification_data"]["vm_program_code"]),
        proof_generator_address=data["verification_data"]["proof_generator_addr"]
    )

    nonced_data = NoncedVerificationData(
        verification_data=ver_data,
        nonce=data["nonce"],
        max_fee=data["max_fee"],
        chain_id=data["chain_id"],
        payment_service_addr=data["payment_service_addr"]
    )

    nonced_data.get_struct_hash()
    client_message = ClientMessage.new(nonced_data, acc)
    message = json.loads(client_message.to_string())
    msg_bin = cbor_serialize(message)
    print("Key value:", len(msg_bin))

    uri = "wss://batcher.alignedlayer.com"
    async with websockets.connect(uri) as socket:
        # WebSocket "open" event equivalent
        print("WebSocket is open now.")
        
        # Sending a binary message (replace `msg_bin` with your actual binary data)
        await socket.send(msg_bin)
        print("Message sent")

        # WebSocket "message" event equivalent
        try:
            async for message in socket:
                decoded_message = cbor_deserialize(message)
                # pretty_message = json.dumps(decoded_message, indent=4)
                print("Message from server:", decoded_message)
        except websockets.ConnectionClosed:
            # WebSocket "close" event equivalent
            print("WebSocket connection closed.")


asyncio.run(main())
# main()