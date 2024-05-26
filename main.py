import ollama
import requests

def modelResponse(model, message):
    response = ollama.chat(model=model, messages=[
    {
        'role': 'user',
        'content': message,
    },
    ])
    return response['message']['content']

def streamingModelResponse(model, message):
    response = ""
    for chunk in ollama.chat(model=model, messages=[
    {
        'role': 'user',
        'content': message,
    },
    ], stream=True):
        print(chunk['message']['content'], end='', flush=True)
        response += chunk['message']['content']
    return response

def retrievePageInformation(link):
    baseURL="https://r.jina.ai/"
    # get response from baseURL+link
    res = requests.get(baseURL + link)
    return res.text

def BrowseWeb(query):
    EngineURL = "https://YOUR-SEARXNG-INSTANCE/search?q={query}&format=json".format(query=query)
    res = requests.get(EngineURL)
    results = res.json()['results']
    # top 8 results
    results = results[:8]
    return results

FindKeywordPrompt = '''
You are an intelligent and resourceful bot designed to provide curated, accurate information by browsing the web. Your goal is to assist users by generating precise search queries based on their questions. Respond only with the exact text for optimal web searching.
Examples:
Q: What is the capital of France?
A: What is the capital of France?
Q: How do I use the SearxNG API?
A: SearxNG API documentation

Keep your responses concise and relevant to ensure users can easily find the information they need.
Here is the user's input:
'''
question = input("What do you want to know today? :) \n")

Query = modelResponse("llama3", "{prompt} {question}".format(prompt=FindKeywordPrompt, question=question))
print("Searching for: ", Query)
results = BrowseWeb(Query)
SearchResultPrompt = '''
You are an expert search assistant with the ability to distill and present the most relevant information from the web. Based on the original question, generate a query, retrieve the top 8 results, and present them in a clear, user-friendly format.

Original Question: {question}
Generated Query: {query}

Here are the top 8 results according to the user's request:
------------
{results}
------------

Please choose the most relevant result and respond with the format containing the title on one line and the URL on the next line. Only format data with no extra response.
'''.format(question=question, query=Query, results=results)
WebsiteCandidate = streamingModelResponse("llama3", SearchResultPrompt)

lines = WebsiteCandidate.strip().split('\n')
title = lines[0]
url = lines[1]

print("\nTitle: ", title)
print("URL: ", url)

print("Retrieving information from: ", url)
WebPageResponse = retrievePageInformation(url)
print(WebPageResponse)

ResultPrompt = '''
Original Question: {question}
Generated Query: {query}
Chosen Result: {chosen_result}

Here is the information from the chosen result:
------------
{web_page_response}
------------

Give the user the information they need in a clear, concise manner. Make sure to include all relevant details and avoid unnecessary information.
'''.format(question=question, query=Query, chosen_result=title, web_page_response=WebPageResponse)

streamingModelResponse("llama3", ResultPrompt)
