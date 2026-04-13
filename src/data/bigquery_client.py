"""
BigQuery 客戶端封裝
"""

import json
from pathlib import Path
from typing import Optional

from google.cloud import bigquery
from google.oauth2 import credentials


class BigQueryClient:
    """BigQuery 客戶端管理類別"""
    
    _instance: Optional["BigQueryClient"] = None
    
    def __init__(self, project_id: str = "onlyme-920902"):
        self.project_id = project_id
        self._client: Optional[bigquery.Client] = None
        self._connect()
    
    def _connect(self):
        """建立 BigQuery 連接"""
        credential_path = Path.home() / '.config' / 'gcloud' / 'legacy_credentials' / 'a0985821880@gmail.com' / 'adc.json'
        
        if credential_path.exists():
            try:
                with open(credential_path, 'r') as f:
                    adc_data = json.load(f)
                creds = credentials.Credentials.from_authorized_user_info(adc_data)
                self._client = bigquery.Client(
                    project=self.project_id,
                    credentials=creds
                )
            except Exception as e:
                print(f"讀取憑證失敗: {e}")
                self._client = bigquery.Client(project=self.project_id)
        else:
            self._client = bigquery.Client(project=self.project_id)
    
    @property
    def client(self) -> bigquery.Client:
        """取得 BigQuery 客戶端"""
        if self._client is None:
            self._connect()
        return self._client
    
    def query(self, sql: str):
        """執行 SQL 查詢"""
        return self.client.query(sql).result().to_dataframe()
    
    def query_to_file(self, sql: str, output_path: str):
        """執行 SQL 查詢並儲存為 CSV"""
        df = self.query(sql)
        df.to_csv(output_path, index=False)
        return df


_client_instance: Optional[BigQueryClient] = None


def get_client(project_id: str = "onlyme-920902") -> BigQueryClient:
    """取得 BigQuery 客戶端單例"""
    global _client_instance
    if _client_instance is None:
        _client_instance = BigQueryClient(project_id)
    return _client_instance
