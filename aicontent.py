import os 
import openai


def productgenerator(query):
    openai.api_key = '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'
    response = openai.Completion.create(
    engine="text-davinci-001",
    prompt=query,
    temperature=0.7,
    max_tokens=200,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0)
    content = response.choices[0].text
    return content


def emailgenerator(query):
    openai.api_key = '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'
    response = openai.Completion.create(
    engine="text-davinci-001",
    prompt=query,
    temperature=0.7,
    max_tokens=200,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0)
    emailcontent = response.choices[0].text
    return emailcontent

def blogideagenerator(query):
    openai.api_key = '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'
    response = openai.Completion.create(
    engine="text-davinci-001",
    prompt=query,
    temperature=0.7,
    max_tokens=200,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0)
    blogcontent = response.choices[0].text
    return blogcontent

def twitterpostgenerator(query):
    openai.api_key = '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'
    response = openai.Completion.create(
    engine="text-davinci-001",
    prompt=query,
    temperature=0.7,
    max_tokens=200,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0)
    twittercontent = response.choices[0].text
    return twittercontent

def summarizationgenerator(query):
    openai.api_key = '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'
    response = openai.Completion.create(
    engine="text-davinci-001",
    prompt=query,
    temperature=0.7,
    max_tokens=200,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0)
    sumcontent = response.choices[0].text
    return sumcontent

