import time, json, sys, base64, io
from llama_cpp import Llama
from llama_cpp.llama_chat_format import MTMDChatHandler
from PIL import Image, ImageDraw
model, mmproj = sys.argv[1], sys.argv[2]
t=time.time()
h = MTMDChatHandler(clip_model_path=mmproj, verbose=False)
llm = Llama(model_path=model, chat_handler=h, n_ctx=4096, n_threads=2, n_batch=512, verbose=False, seed=7)
print("load s", round(time.time()-t,1))
schema={"type":"object","properties":{"evidence":{"type":"string","maxLength":200},"score":{"type":"integer","minimum":1,"maximum":5}},"required":["evidence","score"]}
msgs=[{"role":"system","content":"You are a careful linguistic evaluator. Reply only with JSON."},
      {"role":"user","content":"Context: an email to a company's board of directors. Task: explain a revenue shortfall.\nResponse: 'Hey guys, so yeah, revenue tanked lol. We'll sort it.'\nRate register appropriateness from 1 (very inappropriate) to 5 (fully appropriate). Give one sentence of evidence, then the score."}]
t=time.time()
r=llm.create_chat_completion(messages=msgs,temperature=0,max_tokens=120,response_format={"type":"json_object","schema":schema})
dt=time.time()-t; u=r["usage"]
print("text:", r["choices"][0]["message"]["content"], u, "s=",round(dt,1), "tok/s overall", round((u["total_tokens"])/dt,1))
# image test
img=Image.new("RGB",(448,448),"white"); d=ImageDraw.Draw(img)
d.rectangle([60,60,200,200],fill="red"); d.ellipse([250,250,400,400],fill="blue"); d.text((70,220),"WET FLOOR",fill="black")
b=io.BytesIO(); img.save(b,format="PNG"); url="data:image/png;base64,"+base64.b64encode(b.getvalue()).decode()
msgs=[{"role":"user","content":[{"type":"image_url","image_url":{"url":url}},{"type":"text","text":"Describe the shapes, their colours and any text in this image in one sentence."}]}]
t=time.time()
r=llm.create_chat_completion(messages=msgs,temperature=0,max_tokens=80)
dt=time.time()-t; u=r["usage"]
print("image:", r["choices"][0]["message"]["content"], u, "s=",round(dt,1))
