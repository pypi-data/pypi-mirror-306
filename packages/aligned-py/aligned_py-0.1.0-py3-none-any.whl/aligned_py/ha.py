from core.errors import SubmitError
from core.types import ValidityResponseMessage, VerificationData, ResponseMessage, BatchInclusionData
from communication.protocol import check_protocol_version
import asyncio

async def main():
    await check_protocol_version("wss://batcher.alignedlayer.com")
asyncio.run(main())


# print(ValidityResponseMessage.InvalidNonce.value)
# ha = {'BatchInclusionData': {'batch_merkle_root': [71, 86, 97, 27, 80, 181, 186, 198, 90, 53, 26, 192, 187, 132, 28, 181, 149, 158, 242, 104, 148, 198, 110, 230, 179, 128, 205, 75, 67, 195, 204, 207], 'batch_inclusion_proof': {'merkle_path': [[148, 64, 45, 77, 2, 8, 114, 23, 178, 192, 188, 149, 141, 176, 80, 134, 140, 201, 226, 89, 178, 7, 200, 239, 253, 188, 232, 114, 145, 57, 23, 16], [28, 115, 188, 199, 56, 18, 34, 253, 215, 166, 29, 76, 90, 218, 30, 29, 189, 115, 3, 81, 223, 116, 29, 184, 103, 197, 46, 244, 193, 202, 223, 27], [94, 252, 33, 141, 220, 59, 117, 182, 245, 153, 38, 13, 79, 15, 111, 27, 228, 54, 226, 179, 175, 26, 34, 79, 58, 80, 192, 58, 163, 235, 103, 73], [53, 89, 21, 90, 159, 254, 221, 89, 78, 108, 35, 96, 90, 156, 120, 172, 179, 145, 5, 194, 213, 230, 29, 193, 210, 165, 101, 37, 243, 14, 10, 82], [144, 61, 116, 249, 139, 212, 222, 13, 239, 251, 61, 195, 154, 146, 51, 179, 250, 101, 242, 181, 203, 174, 174, 186, 87, 217, 203, 100, 5, 143, 54, 69]]}, 'index_in_batch': 0}}

# print(next(iter(ha.keys())))
# batch = BatchInclusionData(
#     batch_merkle_root=ha.get("BatchInclusionData").get("batch_merkle_root"),
#     batch_inclusion_proof=ha.get("BatchInclusionData").get("batch_inclusion_proof"),
#     index_in_batch=ha.get("BatchInclusionData").get("index_in_batch")
# )

# fuck: BatchInclusionData = ResponseMessage.BatchInclusionDataMessage("BatchInclusionData", ha.get("BatchInclusionData"))
# print(batch.batch_inclusion_proof["merkle_path"])

# # print(ha.get("BatchInclusionData").get("batch_merkle_root"))