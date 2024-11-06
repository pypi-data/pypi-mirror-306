import requests
import jwt
from datetime import datetime, timedelta
import time
#import subprocess
import json
#from modules.pdf import gerar_pdf_extrato
#import csv
#import io
#import sys
#import logging
from pydantic import BaseModel, StrictStr, StrictInt, ValidationError, field_validator, FieldValidationInfo
from typing import Literal

# Validações dos inputs
class InitParamsValidator(BaseModel):
    client_id: str
    user_agent: str
    private_key: str
    ambiente: Literal["prd", "sdx"]  # Aceita apenas "prd" ou "sdx"

    # Validação para garantir que cada parâmetro é uma string não vazia
    @field_validator('client_id', 'user_agent', 'private_key')
    def check_non_empty_string(cls, value, info):
        if not isinstance(value, str) or not value.strip():
            
            raise ValueError(f"O parâmetro '{info.field_name}' deve ser uma string não vazia.")
        
        return value
    
class DocumentoValidator(BaseModel):

    documento: StrictStr | StrictInt  # Aceita apenas str ou int

    # Valida se 'documento' não é vazio
    @field_validator('documento')
    def documento_nao_vazio(cls, value: StrictStr | StrictInt, info: FieldValidationInfo):
        
        if isinstance(value, str) and not value.strip():
        
            raise ValueError("O parâmetro 'documento' não pode ser uma string vazia.")
        
        return value

class AccountIDValidator(BaseModel):
    
    account_id: StrictStr # Aceita apenas str

    # Valida se 'client_id' não é vazio
    @field_validator('account_id')
    def account_id_nao_vazio(cls, value: StrictStr, info: FieldValidationInfo):
        
        if isinstance(value, str) and not value.strip():
        
            raise ValueError("O parâmetro 'account_id' não pode ser uma string vazia.")
        
        return value
    
class ExtratoParamsValidator(BaseModel):
    
    account_id: str
    data_inicio: datetime
    data_fim: datetime
    async_mode: bool

    # Valida se 'client_id' não é vazio
    @field_validator('account_id')
    def account_id_nao_vazio(cls, value: StrictStr, info: FieldValidationInfo):
        
        if isinstance(value, str) and not value.strip():
        
            raise ValueError("O parâmetro 'account_id' não pode ser uma string vazia.")
        
        return value

    # Valida se 'data_inicio' está no formato datetime
    @field_validator('data_inicio', 'data_fim')
    def check_datetime_format(cls, value, info: FieldValidationInfo):
        
        if not isinstance(value, datetime):
        
            raise ValueError(f"O parâmetro '{info.field_name}' deve estar no formato datetime.")
        
        return value

    # Valida se 'data_fim' é posterior a 'data_inicio'
    @field_validator('data_fim')
    def check_data_fim_posterior(cls, data_fim, values):
        data_inicio = values.get('data_inicio')
        
        if data_inicio and data_fim and data_fim <= data_inicio:
        
            raise ValueError("O parâmetro 'data_fim' deve ser posterior a data_inicio.")
        
        return data_fim

    # Valida se 'async_mode' é um valor booleano
    @field_validator('async_mode')
    def check_async_mode(cls, async_mode):
        
        if not isinstance(async_mode, bool):
        
            raise ValueError("O parâmetro 'async_mode' deve ser um valor booleano.")
        
        return async_mode

class ReceiptIDValidator(BaseModel):
    
    receipt_id: StrictStr # Aceita apenas str

    # Valida se 'receipt_id' não é vazio
    @field_validator('receipt_id')
    def receipt_id_nao_vazio(cls, value: StrictStr, info: FieldValidationInfo):
        
        if isinstance(value, str) and not value.strip():
        
            raise ValueError("O parâmetro 'receipt_id' não pode ser uma string vazia.")
        
        return value

class StoneAdmin:
    
    def __init__(self, client_id:str, user_agent:str, private_key:str, ambiente:str):
    
        try:
            
            InitParamsValidator(client_id=client_id, user_agent=user_agent, private_key=private_key, ambiente=ambiente)
        
        except ValidationError as e:
        
            raise ValueError("Erro na validação dos dados de input da inicialização da instância:", e.errors())
        
        # Produção
        if ambiente == 'prd':
        
            self.base_url = 'https://api.openbank.stone.com.br/resources/v1'
            self.base_auth_url = 'https://accounts.openbank.stone.com.br'
        
        # Sandbox
        else:
        
            self.base_url = 'https://sandbox-api.openbank.stone.com.br/resources/v1'
            self.base_auth_url = 'https://sandbox-accounts.openbank.stone.com.br'
        
        self.client_id = client_id
        self.user_agent = user_agent
        self.private_key = private_key
        self.token = self.__get_token()
        self.authenticated_header = {
            'Authorization' : f"Bearer {self.token}",
            'User-Agent': self.user_agent,
            #'Client-ID': self.client_id
        }

    def __get_token(self):
        base_url = f'{self.base_auth_url}/auth/realms/stone_bank'
        auth_url = f'{base_url}/protocol/openid-connect/token'
        payload = {
            'exp': int(time.time()) + 3600,
            'nbf': int(time.time()),
            'aud': base_url,
            'realm': 'stone_bank',
            'sub': self.client_id,
            'clientId': self.client_id,
            'jti': str(time.time()),
            'iat': int(time.time()),
            'iss': self.client_id
        }

        token = jwt.encode(payload, self.private_key, algorithm='RS256')

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': self.user_agent
        }

        token_payload = {
            'client_id': self.client_id,
            'grant_type': 'client_credentials',
            'client_assertion': token,
            'client_assertion_type': 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer'
        }

        response = requests.post(auth_url, data=token_payload, headers=headers, timeout=60)
        #print(response.json())
        return response.json()['access_token']

    def renew_authorization(self):
        self.token = self.__get_token()
        self.authenticated_header = {
            'Authorization' : f"Bearer {self.token}",
            'User-Agent': self.user_agent,
            #'Client-ID': self.client_id
        }

    def verificar_cliente(self,documento:str)->dict:
        
        try:
        
            DocumentoValidator(documento=documento)
        
        except ValidationError as e:
        
            raise ValueError("Erro na validação dos dados de input do método:", e.errors())
        
        params_conta_ativa = {'owner_document': documento}
        params_conta_inativa = {'owner_document': documento,'status':'closed'}

        try:

            # Verificando se existe cliente com esse documento, com a conta ativa
            response = requests.get(f"{self.base_url}/accounts", params=params_conta_ativa, headers=self.authenticated_header, timeout=60)
            
            # Retorno esperado pela API Stone Admin - consulta cliente ativo
            if response.status_code == 200:
                
                # Não existe cliente com esse documento e com a conta ativa
                if len(response.json()) == 0:
                    
                    # Verificando se existe cliente com esse documento, com a conta inativa
                    encontrado = False
                    response = requests.get(f"{self.base_url}/accounts", params=params_conta_inativa, headers=self.authenticated_header, timeout=60)
                    
                    # Retorno esperado pela API Stone Admin - consulta cliente inativo
                    if response.status_code == 200:
                        
                        resposta = response.json()
                    
                        # Existe cliente com esse documento, mas com a conta inativa
                        if len(resposta) != 0:
                        
                            encontrado = True
                    
                    # Algum erro na API Stone Admin - retorna erro
                    else:
                        
                        return False, ValueError(response.json())
                
                # Cliente econtrado e com a conta ativa
                else:

                    encontrado = True
                    resposta = response.json()
                
                retorno = []
                
                # Monta JSON , pode ter mais de uma conta
                for registro in resposta:

                    retorno_item = {}
                    account_code = registro["account_code"]
                    account_id = registro["id"]
                    owner_id = registro["owner_id"]
                    closed_at = registro["closed_at"]
                    created_at = registro["created_at"]

                    # Status atual da conta
                    if closed_at is None:

                        registro["conta_ativa"] = True
                    
                    else:
                    
                        registro["conta_ativa"] = False
                        
                    retorno.append(registro)

                retorno_json = {
                    "success":True,
                    "status_code": response.status_code,
                    "error": None,
                    "encontrado": encontrado,
                    "detalhes": retorno
                    }
                return retorno_json
            
            # Retorno inesperado pela API Stone Admin - consulta cliente ativo, retorna erro
            else:

                retorno_json = {
                    "success":False,
                    "status_code": response.status_code,
                    "error": ValueError(response.json())
                    }
                return retorno_json
        
        # Erro inesperado como a requisição à API Stone Admin - consulta cliente ativo, retorna erro
        except Exception as e:

            retorno_json = {
                "success":False,
                "status_code": response.status_code,
                "error": e
                }        
            return retorno_json
    
    def balance_da_conta(self,account_id:str):
        try:
        
            AccountIDValidator(account_id=account_id)
        
        except ValidationError as e:
        
            raise ValueError("Erro na validação dos dados de input do método:", e.errors())
        
        # Captura o balance da conta
        response = requests.get(f"{self.base_url}/accounts/{account_id}", headers=self.authenticated_header)
        return response

    def detalhar_titular_cpf(self,documento:str):

        try:
        
            DocumentoValidator(documento=documento)
        
        except ValidationError as e:
        
            raise ValueError("Erro na validação dos dados de input do método:", e.errors())

        # Detalha o titular
        
        # Verificar na rota /users (CPF)
        filtro = {'document': documento}
        param = {
            'filter': json.dumps(filtro)  # Transforma o dicionário em uma string JSON
        }
        response = requests.get(f"{self.base_url}/users", params=param, headers=self.authenticated_header)
        return response

    def detalhar_titular_cnpj(self,documento:str):

        try:
        
            DocumentoValidator(documento=documento)
        
        except ValidationError as e:
        
            raise ValueError("Erro na validação dos dados de input do método:", e.errors())

        # Verificar na rota /organizations (CNPJ)
        filtro = {'document': documento}
        param = {
            'filter': json.dumps(filtro)  # Transforma o dicionário em uma string JSON
        }
        response = requests.get(f"{self.base_url}/organizations", params=param, headers=self.authenticated_header)
        return response

    def extrair_extrato(self,account_id:str,data_inicio:datetime,data_fim:datetime,async_mode:bool=False):
        
        try:
        
            ExtratoParamsValidator(account_id=account_id, data_inicio=data_inicio, data_fim=data_fim, async_mode=async_mode)
        
        except ValidationError as e:
        
            raise ValueError("Erro na validação dos dados de input do método:", e.errors())
        
        # Validação do async_mode
        if not isinstance(async_mode, bool):
        
            raise ValueError("async_mode deve ser um valor booleano.")


        data_inicio = data_inicio.strftime('%Y-%m-%d')
        data_fim = data_fim + timedelta(days=1)
        data_fim = data_fim.strftime('%Y-%m-%d')

        try:
            
            if async_mode:
            
                response = requests.get(f"{self.base_url}/exports/accounts/{account_id}/statement?start_date={data_inicio}&end_date={data_fim}&format=pdf&async=true", headers=self.authenticated_header, timeout=60)
            
            else:
            
                response = requests.get(f"{self.base_url}/exports/accounts/{account_id}/statement?start_date={data_inicio}&end_date={data_fim}&format=pdf&async=false", headers=self.authenticated_header, timeout=120)

            if response.status_code == 200 and not async_mode:
            
                return {"success":True, "status_code": response.status_code, "error": None, "pdf_content": response.content}
        
            elif response.status_code == 202 and async_mode:

                return {"success":True, "status_code": response.status_code, "error": None, "receipt_id":response.json()["id"]}
            
            else:
            
                return {"success":False, "status_code": response.status_code, "error": str(response.text), "pdf_content": None}
    
        except Exception as e:

            return {"success": False, "status_code": response.status_code, "error": e, "pdf_content": None}

    def download_receipt(self,receipt_id:str):
        
        try:
        
            ReceiptIDValidator(receipt_id=receipt_id)
        
        except ValidationError as e:
        
            raise ValueError("Erro na validação dos dados de input do método:", e.errors())

        try:
        
            response = requests.get(f"https://api.openbank.stone.com.br/resources/v1/exports/receipt_requests/download/{receipt_id}", headers=self.authenticated_header, timeout=120)
        
            if response.status_code == 200:
        
                # Decodificando o conteúdo usando UTF-8
                #decoded_content = response.content.decode('utf-8')
                print("header:",response.headers['Content-Type'])
                print(f"type do content: {type(response.content)}")
                return {'result':True, 'status_code': response.status_code, 'error': None, 'pdf_content':response.content}
                #return {'result':True, 'status_code': response.status_code, 'error': None, 'pdf_content':decoded_content}
        
            else:
        
                return {'result': False, 'status_code': response.status_code, 'error': response.json(), 'pdf_content': None}
        
        except Exception as e:
            
            return {'result': False, 'status_code': None, 'error': e, 'pdf_content': None}