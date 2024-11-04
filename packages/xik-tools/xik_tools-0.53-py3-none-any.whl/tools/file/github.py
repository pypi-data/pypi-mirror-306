import requests
import base64
import pandas as pd
import json

class GitMgt:
    
    def __init__(self):
        pass
    
    @staticmethod    
    def upload_json_to_github(content, git_token, git_repo, file_name='data'):
        
        if isinstance(content, pd.DataFrame):
            json_content = content.to_json(orient='records', lines=True)
        elif isinstance(content, dict):
            json_content = json.dumps(content)
        else:
            raise ValueError("content는 DataFrame, dict 이어야 합니다.")
        
        encoded_content = base64.b64encode(json_content.encode('utf-8')).decode('utf-8')
        
        url = f'https://api.github.com/repos/{git_repo}/contents/{file_name}.json'
        
        headers = {
            'Authorization': f'token {git_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        data = {
            'message': 'Upload JSON file',
            'content': encoded_content, 
        }

        response = requests.put(url, headers=headers, json=data)

        if response.status_code == 201:
            print('파일이 성공적으로 업로드되었습니다!')
        else:
            print('업로드 실패:', response.json())