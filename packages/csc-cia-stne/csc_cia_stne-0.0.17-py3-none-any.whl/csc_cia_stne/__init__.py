import os
from .settings import settings

if os.getenv('ambiente_de_execucao') is not None and os.getenv('ambiente_de_execucao') == "karavela":
    from .logger_json import logger
else:
    from .logger_rich import logger
from .karavela import Karavela
from .utilitarios import Util
from .servicenow import ServiceNow
from .stne_admin import StoneAdmin
from .bc_sta import BC_STA
from .bc_correios import BC_Correios
from .gcp_bigquery import BigQuery