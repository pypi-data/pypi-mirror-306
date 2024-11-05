
from Xclient import MetaLMEmbeddings
from Xclient import ModelClient

import numpy as np

sample = np.array(
    ['你从哪里来，要到哪里去'.encode("utf-8")], dtype=np.object_
)

with ModelClient("http://10.88.36.58:8200","bge_large_zh") as client:
    print(client.model_config)
    res = client.infer_sample(sample)
    a = res['OUTPUT__0'].tolist()

xlembed = MetaLMEmbeddings(model="bge-large-zh-v1_5",base_url="http://10.88.36.110:8300")

# text = ['asdasda','asdwrfa']
print('----------------------------------')
res= xlembed.embed_query('你从哪里来，要到哪里去')
print(res)
print(np.array(a)@np.array(res))
# res= xlembed.embed_documents(text)
# print(res)

# res= xlembed.embed_documents_sparse(text)
# print(res)


# res= xlembed.embed_query_sparse('asdasda')
# print(res)