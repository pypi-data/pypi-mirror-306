from sdk import get_balance_in_aligned, get_next_nonce, estimate_fee, submit_and_wait_verification
from core.types import Network, PriceEstimate, VerificationData, ProvingSystemId
from web3 import Web3
import asyncio
import requests

async def main():
    rpc_api = "https://eth-holesky.g.alchemy.com/v2/rdrUy9h_eUsh0V1_r31PYbpoW2Fn4ab9"
    private_key = '0x8d76fc4c878c8a99ab611e94621c840f5ae41dbe2f3613b73c7330b604d081da'
    web3 = Web3(Web3.HTTPProvider(rpc_api))
    account = web3.eth.account.from_key(private_key)
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
    result = await submit_and_wait_verification(
        "wss://batcher.alignedlayer.com",
        rpc_api,
        Network.Holesky,
        ver_data,
        data["max_fee"],
        account,
        int(data["nonce"], 16)
    )
    print(result)


asyncio.run(main())