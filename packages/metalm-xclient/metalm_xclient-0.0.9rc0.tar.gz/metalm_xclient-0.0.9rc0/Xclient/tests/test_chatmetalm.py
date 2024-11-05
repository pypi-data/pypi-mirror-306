import numpy as np
import sys
sys.path.append("/data/jueyuan/project/MetaLM-Xclient/Xclient")
from client import ModelClient
from llms import ChatMetaLM


# async def main():
#     client = AsyncioDecoupledModelClient("grpc://10.88.36.58:8201", "Qwen2-0.5B-Instruct")
#     async for answer in client.infer_sample(np.array(["介绍一下你自己".encode('utf-8')])):
#         print(answer)
#     await client.close()

# # Run the code as a coroutine using asyncio.run()
# import asyncio
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())

with ModelClient("grpc://10.88.36.58:8201", "Qwen2-0.5B-Instruct") as client:
    print(client.model_config)
    
llm = ChatMetaLM(server_url="10.88.36.58:8201", model_name="Qwen2-0.5B-Instruct",stop=[])
#result = llm.invoke("I'm Pickle Rick")
#print(result)
n=0
for token in llm.stream("你好",max_tokens=4000,request_id='1'):
    print(token)
    if n==100:
        llm.stop_stream("Qwen2-0.5B-Instruct",request_id='2')
    n = n + 1


