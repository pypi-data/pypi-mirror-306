from typing import List
from core.errors import SubmitError
from core.types import (
    AlignedVerificationData, Network,
    VerificationData, VerificationDataCommitment
)
from communication.protocol import check_protocol_version
from communication.messaging import send_messages, receive
from communication.batch import await_batch_verification
from eth_account import Account
import websockets
from sdk import get_payment_service_address

RETRIES = 10
TIME_BETWEEN_RETRIES = 10  # in seconds

async def submit_multiple_and_wait_verification(
    batcher_url: str,
    eth_rpc_url: str,
    network: Network,
    verification_data: List[VerificationData],
    max_fees: List[int],
    wallet: Account,
    nonce: int
) -> List[AlignedVerificationData]:
    aligned_verification_data = await submit_multiple(
        batcher_url, network, verification_data, max_fees, wallet, nonce
    )

    for data in aligned_verification_data:
        await await_batch_verification(data, eth_rpc_url, network)

    return aligned_verification_data


async def submit_multiple(
    batcher_url: str,
    network: Network,
    verification_data: List[VerificationData],
    max_fees: List[int],
    wallet: Account,
    nonce: int
) -> List[AlignedVerificationData]:
    return await _submit_multiple(
        batcher_url, network, verification_data, max_fees, wallet, nonce
    )


async def _submit_multiple(
    batcher_url, network: Network,
    verification_data: List[VerificationData],
    max_fees: List[int], wallet: Account, nonce: int
) -> List[AlignedVerificationData]:
    await check_protocol_version(batcher_url)

    async with websockets.connect(batcher_url) as socket:
        if not verification_data:
            raise SubmitError.missing_required_parameter("verification_data")

        payment_service_addr = get_payment_service_address(network)
        sent_verification_data = await send_messages(
            socket, payment_service_addr,
            verification_data, max_fees, wallet, nonce
        )

        num_responses = 0
        verification_data_commitments_rev: List[VerificationDataCommitment] = list(
            reversed([VerificationDataCommitment.from_data(vd.verification_data) for vd in sent_verification_data])
        )

        return await receive(
            socket, len(verification_data),
            num_responses, verification_data_commitments_rev
        )


async def submit_and_wait_verification(
    batcher_url: str,
    eth_rpc_url: str,
    network: Network,
    verification_data: VerificationData,
    max_fee: int,
    wallet: Account,
    nonce: int
) -> AlignedVerificationData:
    aligned_verification_data = await submit_multiple_and_wait_verification(
        batcher_url, eth_rpc_url, network, [verification_data], [max_fee], wallet, nonce
    )
    return aligned_verification_data[0]


async def submit(
    batcher_url: str,
    network: Network,
    verification_data: VerificationData,
    max_fee: int,
    wallet: Account,
    nonce: int
) -> AlignedVerificationData:
    aligned_verification_data = await submit_multiple(
        batcher_url, network, [verification_data], [max_fee], wallet, nonce
    )
    return aligned_verification_data[0]
