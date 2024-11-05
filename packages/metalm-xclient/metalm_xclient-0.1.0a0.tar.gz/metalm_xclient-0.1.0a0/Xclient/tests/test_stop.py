import sys
sys.path.append("/data/jueyuan/project/MetaLM-Xclient/Xclient")

from llms import ChatMetaLM

   
llm = ChatMetaLM(server_url="10.88.36.58:8201", model_name="Qwen2-0.5B-Instruct")
llm.stop_stream("Qwen2-0.5B-Instruct",'4')