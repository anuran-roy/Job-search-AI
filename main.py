from rss import loader
from db import insert_jobs
from vector_store import vector_store as vs
from uuid import uuid4
from embedding import query_embeddings, doc_embeddings
#docs=loader.load()
from pdf_utils import pdf_loader
import asyncio
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI
import json
llm = GoogleGenerativeAI(model="gemini-2.0-flash")
async def load_jobs():
    docs = loader.load()
    uuids = [str(uuid4()) for _ in range(len(docs))]
    vs.add_documents(documents=docs, ids=uuids)
    await insert_jobs([doc.model_dump() for doc in docs])
    
async def main():
    await load_jobs()
    resume=pdf_loader.load()
    resume_embedding=doc_embeddings.embed_query(resume[0].page_content)
    query=input("What type of job are you looking for?")
    # my_query_embeddings=query_embeddings.embed_query(query)
    relevant_jobs=vs.similarity_search(resume[0].page_content, score_threshold=0)
    print(f"\n\n===================\n\nRelevant jobs=\n\n===================\n\n{relevant_jobs}\n\n===================\n\n")
    final_query= '''You are an AI job search assistant. Given the following information, help the user find the job best suited for them.

The user query is:
```
{query}
```

The relevant jobs to their resume are:
```
{relevant_jobs}
```

'''
    print(f"\n\n===================\n\nFinal Query=\n\n===================\n\n{final_query}\n\n===================\n\n")
    template = PromptTemplate(template=final_query, input_variables=["relevant_jobs","query"])
    
    chain = template | llm
    result=chain.invoke(input={"query": query, "relevant_jobs": json.dumps([job.model_dump() for job in relevant_jobs])})
    print(result)
asyncio.run(main())