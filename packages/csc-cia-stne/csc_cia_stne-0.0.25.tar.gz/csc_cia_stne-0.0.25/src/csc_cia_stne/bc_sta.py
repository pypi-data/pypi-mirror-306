from requests.auth import HTTPBasicAuth
import requests
import xml.etree.ElementTree as ET
import hashlib
from pydantic import BaseModel, ValidationError, field_validator
from typing import Literal, Dict, Union, Optional

# Validações dos inputs
class InitParamsValidator(BaseModel):
    usuario: str
    senha: str
    ambiente: Literal["prd", "hml"]  # Aceita apenas "prd" ou "sdx"

    # Validação para garantir que cada parâmetro é uma string não vazia
    @field_validator('usuario', 'senha')
    def check_non_empty_string(cls, value, info):
        if not isinstance(value, str) or not value.strip():
            
            raise ValueError(f"O parâmetro '{info.field_name}' deve ser uma string não vazia.")
        
        return value

class EnviarArquivoValidator(BaseModel):
    tipo_arquivo:str
    file_content:bytes
    nome_arquivo:str
    observacao:str
    destinatarios:Optional[Union[Dict[str, str], str]] = None  # Aceita um dicionário
    
    @field_validator("tipo_arquivo")
    def check_tipo_arquivo(cls, value):
        if not isinstance(value, str) or not value.strip():
    
            raise ValueError("O parâmetro 'tipo_arquivo' deve ser uma string não vazia, com o código do tipo de envio a ser utilizado para o STA, verificar codigos disponíveis na documentação STA")
    
        return value
    
    # Validador para file_content: deve ter conteúdo em bytes
    @field_validator("file_content")
    def check_file_content(cls, value):
        if not isinstance(value, bytes) or len(value) == 0:
            raise ValueError("O parâmetro 'file_content' deve ser um byte array não vazio.")
        return value
    
    # Validador para nome_arquivo: deve ser uma string não vazia e terminar com uma extensão de arquivo comum
    @field_validator("nome_arquivo")
    def check_nome_arquivo(cls, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("O nome do arquivo deve ser uma string não vazia.")
        if not value.lower().endswith(('.zip', '.xpto')):
            raise ValueError("O nome do arquivo deve ter uma extensão válida.")
        return value
    
    @field_validator("observacao")
    def check_observacao(cls, value):
        if not isinstance(value, str) or not value.strip():
    
            raise ValueError("O parâmetro 'observacao' deve ser uma string não vazia")
    
        return value

    # Validador para destinatarios: aceita um dicionário ou uma string XML opcional
    @field_validator("destinatarios")
    def check_destinatarios(cls, value):
        if value is not None:
            
            if not isinstance(value, list):
            
                raise ValueError("O parâmetro 'destinatarios' deve ser uma lista de dicionários.")
            
            for item in value:
            
                if not isinstance(item, dict):
            
                    raise ValueError("Cada destinatário deve ser um dicionário.")
            
                required_keys = {"unidade", "dependencia", "operador"}
            
                if not required_keys.issubset(item.keys()):
            
                    raise ValueError("Cada destinatário deve conter as chaves 'unidade', 'dependencia' e 'operador'. Verifique a documentação da API BC STA para entender o que colocar cada campo")
        
        return value
    
class BC_STA:
    
    def __init__(self, usuario:str, senha:str, ambiente:str):

        try:
            
            InitParamsValidator(usuario=usuario, senha=senha, ambiente=ambiente)
        
        except ValidationError as e:
        
            raise ValueError("Erro na validação dos dados de input da inicialização da instância 'BC_STA':", e.errors())
        
        if ambiente == 'prd':
            
            self.base_url = "https://sta.bcb.gov.br/staws"
        
        else:
            
            self.base_url = "https://sta-h.bcb.gov.br/staws"
        
        try:

            self.auth = HTTPBasicAuth(usuario,senha)
            self.error = None
            self.headers = {'Content-Type': 'application/xml'}
            self.is_connected = self.verifica_conexao()

        except Exception as e:

            self.is_connected = False
            self.error = e
    
    def verifica_conexao(self):
        try:

            response = requests.get("https://sta.bcb.gov.br/staws/arquivos?tipoConsulta=AVANC&nivelDetalhe=RES", auth=self.auth)
            
            # Verificando o status e retornando a resposta
            if response.status_code == 200:

                return True

            else:

                return False


        except Exception as e:

            raise e

    def enviar_arquivo(self, tipo_arquivo:str, file_content:bytes, nome_arquivo:str, observacao:str, destinatarios:dict=None):

        try:
            
            EnviarArquivoValidator(tipo_arquivo=tipo_arquivo, file_content=file_content, nome_arquivo=nome_arquivo, observacao=observacao, destinatarios=destinatarios)
        
        except ValidationError as e:
        
            raise ValueError("Erro na validação dos dados de input do método 'enviar_arquivo':", e.errors())

        def generate_sha256_hash(file_content):
            
            # Gera o hash SHA-256 do arquivo
            sha256_hash = hashlib.sha256()
            sha256_hash.update(file_content)
            return sha256_hash.hexdigest()

        def process_response(xml_content):

            try:

                root = ET.fromstring(xml_content)

                # Verifica se há um elemento <Erro> no XML
                erro = None
                erro_elem = root.find('Erro')
                
                if erro_elem is not None:
                
                    codigo_erro = erro_elem.find('Codigo').text
                    descricao_erro = erro_elem.find('Descricao').text
                    erro = f"Erro {codigo_erro}: {descricao_erro}"
                    resposta = {
                        'enviado':False,
                        'protocolo': None,
                        'link': None,
                        'erro': erro
                        }                                    

                else:

                    protocolo = root.find('Protocolo').text
                    link = root.find('.//atom:link', namespaces={'atom': 'http://www.w3.org/2005/Atom'}).attrib['href']
                    resposta = {
                        'enviado':True,
                        'protocolo': protocolo,
                        'link': link,
                        'erro': None
                        }

                return resposta

            except ET.ParseError as e:

                resposta = {
                    'enviado': False,
                    'protocolo': None,
                    'link': None,
                    'erro': f"Error processing XML: {str(e)}"
                }
                return resposta
        
        url = self.base_url + '/arquivos'

        # Calcula o hash SHA-256 do conteúdo do arquivo
        hash_sha256 = generate_sha256_hash(file_content)
        tamanho_arquivo = len(file_content)  # Tamanho do arquivo em bytes

        # Constrói o XML de requisição
        parametros = ET.Element('Parametros')
        ET.SubElement(parametros, 'IdentificadorDocumento').text = tipo_arquivo
        ET.SubElement(parametros, 'Hash').text = hash_sha256
        ET.SubElement(parametros, 'Tamanho').text = str(tamanho_arquivo)
        ET.SubElement(parametros, 'NomeArquivo').text = nome_arquivo
        
        # Campo observação é opcional
        if observacao:
            ET.SubElement(parametros, 'Observacao').text = observacao

        # Campo destinatários é opcional
        if destinatarios:

            destinatarios_elem = ET.SubElement(parametros, 'Destinatarios')

            for dest in destinatarios:

                destinatario_elem = ET.SubElement(destinatarios_elem, 'Destinatario')
                ET.SubElement(destinatario_elem, 'Unidade').text = dest['unidade']

                if 'dependencia' in dest:

                    ET.SubElement(destinatario_elem, 'Dependencia').text = dest['dependencia']

                if 'operador' in dest:

                    ET.SubElement(destinatario_elem, 'Operador').text = dest['operador']

        # Converte o XML para string
        xml_data = ET.tostring(parametros, encoding='utf-8', method='xml')

        # Envia a requisição POST
        response = requests.post(url, headers=self.headers, data=xml_data, auth=self.auth, timeout=60)

        if response.status_code == 201:  # Verifica se o protocolo foi criado com sucesso
            
            resultado_protocolo = process_response(response.text)
            
            # Protocolo gerado, prosseguir com envio do arquivo
            if resultado_protocolo["enviado"]:
                
                try:
                    
                    # Solicita o envio
                    protocolo = resultado_protocolo["protocolo"]
                    # URL do endpoint, incluindo o protocolo
                    url = url + f"/{protocolo}/conteudo"

                    # Envia a requisição PUT com o conteúdo binário do arquivo
                    response = requests.put(url, data=file_content, auth=self.auth, timeout=60)
                    
                    if response.status_code == 200:
                    
                        return resultado_protocolo
                    
                    else:
                    
                        resposta = {
                            'enviado':False,
                            'protocolo': None,
                            'link': None,
                            'erro': f"Falha ao enviar arquivo. Status code: {response.status_code}, Text: {response.text}, Reason: {response.reason}"
                            }
                        return resposta

                except Exception as e:
                    
                    erro = str(e)
                    resposta = {
                        'enviado':False,
                        'protocolo': None,
                        'link': None,
                        'erro': erro
                        }
                    return resposta



            # Protocolo não foi gerado, retornar erro
            else:
            
                return resultado_protocolo

        else:

            print(response.text)
            resposta = {
                'enviado': False,
                'protocolo': None,
                'link': None,
                'erro': f"Failed to create protocol. Status code: {response.status_code}, Reason: {response.reason}"
            }
            #return f"Failed to create protocol. Status code: {response.status_code}, Reason: {response.reason}"
            return resposta

