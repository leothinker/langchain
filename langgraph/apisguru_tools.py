from typing import Optional
import requests
import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig


class APIs_guruApi:

    BaseUrl = 'https://api.apis.guru/v2'

    HttpHeader = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer YOUR_ACCESS_TOKEN'
        }

    prompt = ChatPromptTemplate.from_messages(
    [
        (
            'system',
            '''You are a specialized manager movie records. You can,

            + use the `getProviders` tool to list all providers
            + use the `getProvider` tool to list all apis for a particular provider
            + use the `getServices` tool to list all servicenames for a particular provider
            + use the `getAPI` tool to retrieve one version of a particular api
            + use the `getServiceAPI` tool to retrieve one version of a particular api with a servicename.
            + use the `listAPIs` tool to list all apis
            + use the `getMetrics` tool to get basic metrics

            Now answer your question'''
        ),
        ('placeholder', '{messages}'),
    ])

    @tool
    def getProviders() -> dict:
        '''List all providers'''
        
        response = requests.get(APIs_guruApi.BaseUrl + f'/providers.json', headers=APIs_guruApi.HttpHeader)
        if response.status_code == 200:
            return 'OK' + '\n\n' + json.dumps(response.json(), indent = 2)
        return f'Request failed with status code: {response.status_code}'
            
    @tool
    def getProvider(provider: str) -> dict:
        '''List all APIs for a particular provider'''
        
        response = requests.get(APIs_guruApi.BaseUrl + f'/{provider}.json', headers=APIs_guruApi.HttpHeader)
        if response.status_code == 200:
            return 'OK' + '\n\n' + json.dumps(response.json(), indent = 2)
        return f'Request failed with status code: {response.status_code}'
            
    @tool
    def getServices(provider: str) -> dict:
        '''List all serviceNames for a particular provider'''
        
        response = requests.get(APIs_guruApi.BaseUrl + f'/{provider}/services.json', headers=APIs_guruApi.HttpHeader)
        if response.status_code == 200:
            return 'OK' + '\n\n' + json.dumps(response.json(), indent = 2)
        return f'Request failed with status code: {response.status_code}'
            
    @tool
    def getAPI(provider: str, api: str) -> dict:
        '''Retrieve one version of a particular API'''
        
        response = requests.get(APIs_guruApi.BaseUrl + f'/specs/{provider}/{api}.json', headers=APIs_guruApi.HttpHeader)
        if response.status_code == 200:
            return 'OK' + '\n\n' + json.dumps(response.json(), indent = 2)
        return f'Request failed with status code: {response.status_code}'
            
    @tool
    def getServiceAPI(provider: str, service: str, api: str) -> dict:
        '''Retrieve one version of a particular API with a serviceName.'''
        
        response = requests.get(APIs_guruApi.BaseUrl + f'/specs/{provider}/{service}/{api}.json', headers=APIs_guruApi.HttpHeader)
        if response.status_code == 200:
            return 'OK' + '\n\n' + json.dumps(response.json(), indent = 2)
        return f'Request failed with status code: {response.status_code}'
            
    @tool
    def listAPIs() -> dict:
        '''List all APIs'''
        
        response = requests.get(APIs_guruApi.BaseUrl + f'/list.json', headers=APIs_guruApi.HttpHeader)
        if response.status_code == 200:
            return 'OK' + '\n\n' + json.dumps(response.json(), indent = 2)
        return f'Request failed with status code: {response.status_code}'
            
    @tool
    def getMetrics() -> dict:
        '''Get basic metrics'''
        
        response = requests.get(APIs_guruApi.BaseUrl + f'/metrics.json', headers=APIs_guruApi.HttpHeader)
        if response.status_code == 200:
            return 'OK' + '\n\n' + json.dumps(response.json(), indent = 2)
        return f'Request failed with status code: {response.status_code}'
            

    tools = [
        getProviders,
        getProvider,
        getServices,
        getAPI,
        getServiceAPI,
        listAPIs,
        getMetrics,
    ]

    def __init__(self, llm):
        self.runnable = APIs_guruApi.prompt | llm.bind_tools(APIs_guruApi.tools)

    def __call__(self, state, config: RunnableConfig):
        configuration = config.get("configurable")
        APIs_guruApi.BaseUrl = configuration.get('url', None)
        APIs_guruApi.HttpHeader['Authorization'] = configuration.get('token', None)
        result = self.runnable.invoke(state)
        return {'messages': result}
    