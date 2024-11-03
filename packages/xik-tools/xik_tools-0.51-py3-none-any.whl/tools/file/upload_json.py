import requests
import base64

def upload_json_to_github(json_content,  git_token, git_repo, file_name = 'data.json'):

    encoded_content = base64.b64encode(json_content.encode('utf-8')).decode('utf-8')


      
    url = f'https://api.github.com/repos/{git_repo}/contents/{file_name}'
    

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

