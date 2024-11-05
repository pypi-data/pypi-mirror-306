import requests
import base64, json
import os
import logging

class ServiceNow:
    
    def __init__(self, username: str = None, password: str = None, env: str = None) -> None:
        # Verifica se todos os parâmetros foram fornecidos e não estão vazios
        if not all([username and username.strip(), password and password.strip(), env and env.strip()]):
            raise ValueError("Todos os parâmetros precisam ser fornecidos para a criação da instância ServiceNow, ou algum dos valores esta nulo ou vazio (username, password, env)")

        # Normaliza o valor de 'env' para maiúsculas
        env = env.strip().upper()

        # Dicionário de ambientes válidos e URLs correspondentes
        valid_envs = {
            'DEV': 'https://stonedev.service-now.com/api',
            'QA': 'https://stoneqas.service-now.com/api',
            'QAS': 'https://stoneqas.service-now.com/api',
            'PROD': 'https://stone.service-now.com/api'
        }

        # Verifica se 'env' é válido
        if env not in valid_envs:
            raise ValueError("O valor de 'env' precisa ser 'dev', 'qa', 'qas' ou 'prod'.")

        # Atribui as variáveis de instância
        self.username = username.strip()
        self.password = password.strip()
        self.env = env
        self.api_url = valid_envs[env]
        self.api_header = {"Content-Type":"application/json","Accept":"application/json"}
        
    # Criação de funções básicas para reutilizar nas funções especificas

    def __auth(self):
        """
            Retorna o e-mail e senha para realizar a autenticação.
        """
        return (self.username, self.password)
    
    def request (self, url, params = ""):
        try:
            response = requests.get(
                url, 
                params=params,
                auth=self.__auth(),
                headers=self.api_header,
                timeout=15,
                verify=True
            )

            # VALIDA SE HOUVE SUCESSO NA REQUISIÇÃO
            response.raise_for_status()

             # Analisa o conteúdo da resposta JSON
            result = response.json()
            if "result" in result:
                return result["result"]
            else:
                logging.warning("A resposta não contém o campo 'result'.")
                return {}

        except requests.exceptions.HTTPError as http_err:
            logging.error(f"Erro HTTP ao buscar os detalhes do ticket: {http_err}")
            raise
        except requests.exceptions.RequestException as req_err:
            logging.error(f"Erro ao buscar os detalhes do ticket: {req_err}")
            raise
        except Exception as e:
            logging.error(f"Erro inesperado: {e}")
            raise

    def put(self, url, payload):
        
        payload = json.dumps(payload)

        try: 
            response = requests.put(
                f"{url}",
                auth=self.__auth(),
                headers=self.api_header,
                data=f"{payload}",
                timeout=15,
                verify=True
            )

            # VALIDA SE HOUVE SUCESSO NA REQUISIÇÃO
            response.raise_for_status()

            # POSSUINDO 'RESULT', TEREMOS O RETORNO DO TICKET ABERTO.
            result = response.json()
            if "result" in result:
                update = result["result"]
                logging.info(f"Atualização concluída com sucesso. Registro atualizado: {update["sys_id"]} | Alterações: {payload}")
            else:
                logging.warning(f"A Resposta da sua requisição não contém o campo 'Result'. Segue o retorno: \n {result} | Alterações: {payload}")
        
        #TRATAMENTOS DE ERRO 
        except requests.exceptions.HTTPError as http_err:

            logging.error(f"Erro HTTP ao tentar atualizar o ticket: {http_err} \n Reposta da solicitação: {response.json().get("error").get("message")}")
            raise
        except requests.exceptions.RequestException as req_err:
            
            logging.error(f"Erro ao tentar atualizar o ticket: \n {req_err}")
            raise
        except Exception as e:
            logging.error(f"Erro inesperado: \n {e}")
            raise
    
    def post(self, url, variables, header_content_type = ""):
        """
            Função para criar um novo ticket no servicenow usando o API REST.

                Parametros:
                    - Payload (Dict): Dicionário contendo os dados que serão utilizados para criar o ticket
                Retorno: 
                    - Dict: Um dicionário contendo os detalhes do ticket criado
                Raises:
                    - Exception: Se ocorrer um erro ao criar o ticket.

        """
        if header_content_type:
            header = header_content_type
        else:
            header = self.api_header

        # Ajustar o Payload para a abertura do ticket
        payload = {
            "sysparm_quantity" : "1",
            "variables" : json.dumps(variables)
        }
        try: 
            response = requests.post(
                f"{url}",
                auth=self.__auth(),
                headers=header,
                data=f"{payload}"
            )

            # VALIDA SE HOUVE SUCESSO NA REQUISIÇÃO
            response.raise_for_status()

            # POSSUINDO 'RESULT', TEREMOS O RETORNO DO TICKET ABERTO.
            result = response.json()
            if "result" in result:
                ticket_number = result["result"].get("number")
                ticket_sys_id = result["result"].get("sys_id")
                logging.info(f"Ticket registrado com sucesso. Número: {ticket_number} | SYS_ID: {ticket_sys_id}")
                return result["result"]
            else:
                logging.warning(f"A Resposta da sua requisição não contém o campo 'Result'. Segue o retorno: \n {result}")
        
        #TRATAMENTOS DE ERRO 
        except requests.exceptions.HTTPError as http_err:

            logging.error(f"Erro HTTP ao tentar registrar o ticket: {http_err} \n Reposta da solicitação: {response.json().get("error").get("message")}")
            raise
        except requests.exceptions.RequestException as req_err:
            
            logging.error(f"Erro ao tentar registrar o ticket: \n {req_err}")
            raise
        except Exception as e:
            logging.error(f"Erro inesperado: \n {e}")
            raise
    
    def listar_tickets(self, tabela: str = None, campos: list = None, query: str = None, limite: int = 50, timeout:int=15)->dict:
        """lista tickets do ServiceNow

        Args:
            tabela (str): tabela do ServiceNow de onde a query será feita
            campos (list): lista de campos com valores a trazer
            query (str): query do ServiceNow
            limite (int, optional): quantidade máxima de tickets para trazer. Default=50
            timeout (int, optional): segundos para a requisicao dar timeout. Default=15

        Returns:
            dict: dicionário com o resultado da query
        """
        # Validação de 'tabela'
        if not tabela or not tabela.strip():
            raise ValueError("O parâmetro 'tabela' precisa ser especificado com o nome da tabela de onde os tickets serão listados.")

        # Validação de 'campos'
        if not isinstance(campos, list) or not campos or not all(isinstance(campo, str) and campo.strip() for campo in campos):
            raise ValueError("O parâmetro 'campos' precisa ser uma lista não vazia de strings válidas com os nomes dos campos do formulário.")

        # Validação de 'query'
        if not query or not query.strip():
            raise ValueError("O parâmetro 'query' precisa ser uma string não vazia.")

        # Validação de 'timeout'
        if not isinstance(timeout, int):
            raise ValueError("O parâmetro 'timeout' precisa ser um valor (int) em segundos.")

        # Validação de 'limite'
        if not isinstance(limite, int):
            raise ValueError("O parâmetro 'limite' precisa ser um número inteiro.")

        params = {}
        params["sysparm_query"] = query
        params["sysparm_fields"] = ','.join(campos)
        params["sysparm_display_value"] = "all"
        params["sysparm_limit"] = limite

        url = f"{self.api_url}/now/table/{tabela}"
        
        try:
            response = self.request(url, params)
            # response = requests.get(url, params=params, auth=(self.username, self.password), headers=self.api_header, verify=True, timeout=timeout)
            return {"result":True, "content": response.json()}
        
        except Exception as e:
            return {}

    def update_ticket(self, tabela: str = None, sys_id: str = None, campos: dict = None, timeout:int=15)->dict:
        """Atualiza as informações de um ticket

        Args:
            tabela (str): Tabela do ServiceNow de onde o ticket pertence
            sys_id (str): sys_id do ticket a ser atualizado
            campos (dict): Dicionário com os dados a serem atualizados no ticket
            timeout (int, optional): segundos para a requisicao dar timeout. Default=15

        Returns:
            dict: resposta do ServiceNow
        """

        # Validação de 'tabela'
        if not tabela or not tabela.strip():
            raise ValueError("O parâmetro 'tabela' precisa ser especificado com o nome da tabela de onde o ticket será atualizado.")

        # Validação de 'sys_id'
        if not sys_id or not sys_id.strip():
            raise ValueError("O parâmetro 'sys_id' precisa ser especificado com o sys_id do ticket.")

        # Validação de 'campos'
        if not isinstance(campos, dict):
            raise ValueError("O parâmetro 'campos' precisa ser um dicionário contendo os campos do ticket a serem atualizados.")

        if "assigned_to" not in campos:
            
            campos["assigned_to"] = self.username

        try:

            url = f"{self.api_url}/now/table/{tabela}/{sys_id}"
            response = self.put(url, payload=campos)
            # response = requests.patch(url, auth=(self.username, self.password), headers=self.api_header, data=str(campos).encode('utf-8'), verify=True, timeout=timeout)

            return response.json()

        except Exception as e:
            
            raise e

    def anexar_arquivo_no_ticket(self,header_content_type:dict=None, anexo_path:str=None, tabela:str=None, sys_id:str=None, timeout:int=15):
        """Anexa arquivo em um ticket do ServiceNow

        Args:
            header_content_type (dict): Dicionário contendo a chave 'Content-Type' com a especificação do tipo do arquivo
            anexo_path (str): Path do arquivo a ser anexado
            tabela (str): Tabela do ServiceNow de onde o ticket pertence
            sys_id (str): sys_id do ticket o qual o arquivo será anexado
            timeout (int, optional): segundos para a requisicao dar timeout. Default=15

        Returns:
            dict: resposta do ServiceNow
        """

        # Validação de 'tabela'
        if not tabela or not tabela.strip():
            raise ValueError("O parâmetro 'tabela' precisa ser especificado com o nome da tabela do ticket pra onde o arquivo será anexado.")

        # Validação de 'sys_id'
        if not sys_id or not sys_id.strip():
            raise ValueError("O parâmetro 'sys_id' precisa ser especificado com o sys_id do ticket que o arquivo será anexado.")

        # Validação de 'anexo_path'
        if not anexo_path or not anexo_path.strip():
            raise ValueError("O parâmetro 'anexo_path' precisa ser especificado com o path para o arquivo a ser anexado.")
        
        if not os.path.exists(anexo_path):
            raise FileExistsError(f"O arquivo não foi encontrado ({anexo_path})")

        header_content_type = self.valida_header_content_type(anexo_path)

        # Converte as chaves do dicionário para minúsculas
        header_content_type_lower = {k.lower(): v for k, v in header_content_type.items()}

        
        
        if "content-type" not in header_content_type_lower:
            
            raise ValueError("O parâmetro 'header_content_type' não possui a chave 'Content-Type' com o tipo do anexo")

        nome_arquivo = os.path.basename(anexo_path)

        with open(anexo_path, 'rb') as f:

            file_data = f

        try:
            url = f"{self.api_url}/now/attachment/file?table_name={tabela}&table_sys_id={sys_id}&file_name={nome_arquivo}"
            response = self.post(url, file_data, header_content_type )
            # response = requests.post(f"{self.api_url}/now/attachment/file?table_name={tabela}&table_sys_id={sys_id}&file_name={nome_arquivo}", headers=header_content_type, auth=(self.username, self.password), data=file_data, timeout=timeout)
            return response.json()
        
        except Exception as e:
            
            raise e
        
    def valida_header_content_type(self, anexo_path ):

        # Pré validando 'header_content_type'
        if os.path.splitext(anexo_path)[1].lower() == ".zip" and header_content_type is None:
            
            header_content_type = {"Content-Type": "application/zip"}
        
        elif os.path.splitext(anexo_path)[1].lower() == ".xlsx" and header_content_type is None:
        
            header_content_type = {"Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"}
        
        elif os.path.splitext(anexo_path)[1].lower() == ".pdf" and header_content_type is None:
        
            header_content_type = {"Content-Type": "application/pdf"}
        
        elif os.path.splitext(anexo_path)[1].lower() == ".txt" and header_content_type is None:
        
            header_content_type = {"Content-Type": "text/plain"}

        # Validação de 'header_content_type'
        if not isinstance(header_content_type, dict):
            raise ValueError("O parâmetro 'header_content_type' precisa ser um dicionário contendo o 'Content-Type' do arquivo a ser anexado. (Ex: {\"Content-Type\": \"application/zip\"})")
        
        # Validação de 'header_content_type'
        if not isinstance(header_content_type, dict):
            raise ValueError("O parâmetro 'header_content_type' precisa ser um dicionário contendo o 'Content-Type' do arquivo a ser anexado. (Ex: {\"Content-Type\": \"application/zip\"})")
        
        return header_content_type

    def get_anexo(self, sys_id: str = None, tabela: str = None, campo: str = 'default', download_dir:str=None, timeout:int=15)->dict:
        """Traz os anexos de um campo do ticket especificado

        Args:
            sys_id (str): sys_id do ticket
            tabela (str): tabela do ticket
            campo (str, optional): campo do anexo
            timeout (int, optional): segundos para a requisicao dar timeout. Default=15

        Returns:
            dict: dicionário com os anexos do ticket
        """

        # Validação de 'sys_id'
        if not isinstance(sys_id, str) or not sys_id.strip():
            raise ValueError("O parâmetro 'sys_id' precisa ser uma string não vazia com o sys_id do ticket.")
        
        # Validação de 'tabela'
        if not isinstance(tabela, str) or not tabela.strip():
            raise ValueError("O parâmetro 'tabela' precisa ser uma string não vazia com o nome da tabela do ticket.")

        # Validação de 'timeout'
        if not isinstance(timeout, int):
            raise ValueError("O parâmetro 'timeout' precisa ser um valor (int) em segundos.")

        # Validação de 'download_dir'
        if download_dir is not None:
            if not isinstance(download_dir, str) or not download_dir.strip():
            
                raise ValueError("O parâmetro 'download_dir' precisa ser a pasta pra onde o anexo será feito o download.")
            
            if not os.path.exists(download_dir):
            
                raise NotADirectoryError(f"A pasta informada '{download_dir}' não existe")
        
        # Validação de 'campo'
        if not isinstance(campo, str) or not campo.strip():
            raise ValueError("O parâmetro 'campo' precisa ser uma string não vazia com o nome do campo do anexo.")

        campo = str(campo).strip().lower()

        # Convert bytes to base64
        def __bytes_to_base64(image_bytes):
            base64_encoded = base64.b64encode(image_bytes)

            # Decode the bytes to a string (UTF-8 encoding)
            base64_string = base64_encoded.decode('utf-8')

            return base64_string 
        
        def __formatar_tamanho(tamanho_bytes):
            # Converte o valor de string para inteiro
            tamanho_bytes = int(tamanho_bytes)
            
            # Define os múltiplos de bytes
            unidades = ['B', 'KB', 'MB', 'GB', 'TB']

            # Itera sobre as unidades até encontrar a maior possível
            for unidade in unidades:
                if tamanho_bytes < 1024:
                    return f"{tamanho_bytes:.2f} {unidade}"
                tamanho_bytes /= 1024
            
            # Caso o valor seja maior que o esperado (Exabyte ou superior)
            return f"{tamanho_bytes:.2f} PB"  # Petabyte

        anexo_dict = {"var_servicenow": campo, "anexos":[]}

        # Fazendo download do anexo do campo padrao do ticket
        if campo == 'default':
            
            print(f"verificando o campo '{campo}' de anexo")

            try:
                #url = f"{SERVICENOW_API_URL}/now/attachment?sysparm_query=table_name=sc_req_item^table_sys_id={sys_id}"
                url = f"{self.api_url}/now/attachment?sysparm_query=table_name={tabela}^table_sys_id={sys_id}"
                response = self.request(url)
                # response = requests.get(url, auth=(self.username, self.password), verify=True, timeout=timeout)
                if response.status_code == 200 and len(response.json()["result"]) >= 1:

                    for attachment in response.json()["result"]:

                        print("attachment")
                        print(attachment)
                        arquivo = {}
                        arquivo["file_name"] = attachment["file_name"]
                        arquivo["size"] = __formatar_tamanho(attachment["size_bytes"]["display_value"])
                        arquivo["content_type"] = attachment["content_type"]
                        #arquivo["table_sys_id"] = attachment["table_sys_id"]

                        try:
                            byte_response = self.request(attachment["download_link"])
                            # byte_response = requests.get(attachment["download_link"], auth=(self.username, self.password), verify=True, timeout=timeout)
                            
                            if byte_response.status_code == 200:

                                arquivo["base64"] = __bytes_to_base64(byte_response.content)
                                
                                if download_dir is not None:
                                    with open(arquivo["file_name"],'wb') as download_file:
                                        download_file.write(byte_response.content)

                                #del arquivo["sys_id"]
                                #del arquivo["download_link"]
                                #del arquivo["table_sys_id"]
                                anexo_dict["anexos"].append(arquivo)
                                #return JSONResponse(content=arquivo, status_code=byte_response.status_code, media_type="application/json")
                                # Requisicao não OK (!= 200)
                        
                        except Exception as e:
                        
                            raise e
                        
                elif response.status_code != 200:
                
                    return response.json()
            
            except Exception as e:
        
                raise e
        
        # Fazendo download do anexo do campo especificado do ticket
        else:
        
            print(f"verificando o campo '{campo}' de anexo")

            url = f"{self.api_url}/now/table/{tabela}?sysparm_query=sys_id={sys_id}&sysparm_fields={campo}&sysparm_display_value=all&sysparam_limit=1"
            try:
                response = requests.get(url, auth=(self.username, self.password), verify=True)

                # Requisicao OK e com anexo
                if response.status_code == 200 and len(response.json()["result"]) >= 1:

                    for ticket_data in response.json()["result"]:

                        if len(ticket_data) >= 1:
                            
                            try:

                                #temp_file_name = ticket_data[campo]["display_value"]
                                temp_sys_id = ticket_data[campo]["value"]

                            except Exception as e:
                                
                                raise e

                            url = f"{self.api_url}/now/table/sys_attachment?sysparm_query=sys_id={temp_sys_id}&sysparm_display_value=all&sysparam_limit=1"

                            response = requests.get(url, auth=(self.username, self.password), verify=True)
                            
                            if response.status_code == 200:

                                attachment = response.json()["result"][0]
                                arquivo = {}
                                arquivo["file_name"] = attachment["file_name"]["display_value"]
                                arquivo["size"] = __formatar_tamanho(attachment["size_bytes"]["display_value"])
                                #arquivo["sys_id"] = attachment["sys_id"]
                                arquivo["content_type"] = attachment["content_type"]["value"]
                                #attach_sys_id = attachment["sys_id"]["display_value"]
                                #attach_sys_id_table = attachment["table_sys_id"]["value"]
                                #url = f"{self.api_url}/now/attachment/{sys_id}/file"
                                try:

                                    url = f"{self.api_url}/now/attachment/{temp_sys_id}/file"
                                    byte_response = requests.get(url, auth=(self.username, self.password), verify=True)
                                    arquivo["base64"] = __bytes_to_base64(byte_response.content)
                                    anexo_dict["anexos"].append(arquivo)
                                    if download_dir is not None:
        
                                        with open(arquivo["file_name"],'wb') as download_file:
                                            download_file.write(byte_response.content)

                                except Exception as e:

                                    raise e
                
                # Requisicao não OK (!= 200)
                elif response.status_code != 200:
                
                    return response.json()
                
            except Exception as e:
                
                raise e
        
        return anexo_dict