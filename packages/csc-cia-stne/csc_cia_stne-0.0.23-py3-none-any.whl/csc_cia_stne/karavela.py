import os

class Karavela():

    def __init__(self)->None:
        """Inicia a instância da classe Karavela

        """
        self.healthy_check_file = None
    
    def create_health_check_file(self,health_check_filename:str = None)->bool:
        """Cria o arquivo de health check

        Args:
            health_check_file (str): nome do arquivo de health check a ser criado
        Returns:
            bool: True
        """
        
        if health_check_filename is None or health_check_filename == "":
            
            raise ValueError("O método 'create_health_check_file' precisa do parâmetro health_check_filename especificado")
        
        self.health_check_filename = health_check_filename

        try:

            if not os.path.exists(self.health_check_filename):

                directory = os.path.dirname(self.health_check_filename)

                if not os.path.exists(directory) and str(directory).strip() != "":
             
                    os.makedirs(directory)
                
            with open(f'{self.health_check_filename}', 'w') as f:
                           
                f.write('OK!')
                return True
            
        except Exception as e:
        
            raise e
    
    def destroy_health_check_file(self)->bool:
        """Deleta o arquivo de health check

        Returns:
            bool: True
        """
        
        if self.health_check_filename is None:
        
            raise ValueError("O método 'create_health_check_file' precisa ser executado antes")
        
        try:

            if os.path.exists(self.health_check_filename):

                os.remove(self.health_check_filename)
                return True
                
            else:
            
                return True
                    
        except Exception as e:
        
            raise e
    
    def get_secret(self,name:str)->str:
        """Extrai a secret do ambiente

        Args:
            name (str): nome da variavel ou arquivo da secret

        Returns:
            str: string da secret armazenada na variável de ambiente ou no arquivo de secret
        """
        
        # Tentando extrair da variavel de ambiente
        secret = os.getenv(name)
        
        # secret não encontrada em variavel de ambiente, tentando extrair do arquivo em /secret
        if secret is None:

            # verifica na pasta ./secrets
            if os.path.exists(f"./secrets/{name}"):

                with open(f"./secrets/{name}",'r') as secret_file:
            
                    secret = secret_file.read()

            # verifica na pasta ./.secrets
            elif os.path.exists(f"./.secrets/{name}"):

                with open(f"./.secrets/{name}",'r') as secret_file:
            
                    secret = secret_file.read()

            # verifica na pasta ./private
            elif os.path.exists(f"./private/{name}"):

                with open(f"./private/{name}",'r') as secret_file:
            
                    secret = secret_file.read()

            # verifica na pasta ./.private
            elif os.path.exists(f"./.private/{name}"):

                with open(f"./.private/{name}",'r') as secret_file:
            
                    secret = secret_file.read()

            # verifica na pasta /secrets
            elif os.path.exists(f"/secrets/{name}"):

                with open(f"/secrets/{name}",'r') as secret_file:
            
                    secret = secret_file.read()

        return secret
    
