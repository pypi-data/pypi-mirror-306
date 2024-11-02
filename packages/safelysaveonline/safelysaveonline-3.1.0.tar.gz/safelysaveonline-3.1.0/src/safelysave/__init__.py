import os
import shutil
import json
import uuid
from pathlib import Path

from httpx import Timeout
from cryptography.fernet import Fernet
import git
from webdav4.client import Client

def create_sso_file(location: str, server_type: str, server_address: str) -> bytes:
    content: dict = {
        'data': [],
        'additions': [],
        'removals': [],
        'server_type': server_type,
        'server_address': server_address,
        'file_uuid': str(uuid.uuid4())
    }

    key: bytes = Fernet.generate_key()
    enc = Fernet(key)

    content_json: str = json.dumps(content)
    content_enc: bytes = enc.encrypt(content_json.encode())

    with open(location, 'wb') as file:
        file.write(content_enc)
    return key

class sso:
    def __init__(self, location: str, key: bytes) -> None:
        self.location = location
        self.key = key

        try:
            enc = Fernet(key)
        except:
            raise Exception("Invalid key / Something went wrong")

        try:
            with open(location, 'rb') as file:
                content_enc: bytes = file.read()

            content_json: str = enc.decrypt(content_enc).decode()
            content: dict = json.loads(content_json)
        except:
            raise Exception("Failed loading file")

    def get_data(self) -> list:
        if os.path.isfile(self.location) == True:
            with open(self.location, 'rb') as file:
                content_enc: bytes = file.read()

            enc = Fernet(self.key)
            content_json: str = enc.decrypt(content_enc).decode()
            content: dict = json.loads(content_json)

            data: list = content['data']
            additions: list = content['additions']
            removals: list = content['removals']

            for i in range(len(additions)):
                data.append(additions[i])

            for i in range(len(removals)):
                for j in range(len(data)):
                    if data[j]['uuid'] == removals[i]:
                        del data[j]
                        break

            return data
        else:
            data = []
            return data

    def add_data(self, data: dict) -> None:
        if os.path.isfile(self.location) == True:
            data['uuid'] = str(uuid.uuid4())

            with open(self.location, 'rb') as file:
                content_enc: bytes = file.read()

            enc = Fernet(self.key)
            content_json: str = enc.decrypt(content_enc).decode()
            content: dict = json.loads(content_json)

            content['additions'].append(data)

            content_json: str = json.dumps(content)
            content_enc: bytes = enc.encrypt(content_json.encode())

            with open(self.location, 'wb') as file:
                file.write(content_enc)

    def remove_data(self, data_uuid: str) -> None:
        if os.path.isfile(self.location) == True:
            with open(self.location, 'rb') as file:
                content_enc: bytes = file.read()

            enc = Fernet(self.key)
            content_json: str = enc.decrypt(content_enc).decode()
            content: dict = json.loads(content_json)

            content['removals'].append(data_uuid)

            content_json: str = json.dumps(content)
            content_enc: bytes = enc.encrypt(content_json.encode())

            with open(self.location, 'wb') as file:
                file.write(content_enc)

    def sync(self) -> None:
        with open(self.location, 'rb') as file:
            content_enc: bytes = file.read()

        enc = Fernet(self.key)
        content_json: str = enc.decrypt(content_enc).decode()
        content: dict = json.loads(content_json)

        if content['server_type'] != 'webdav' and content['server_type'] != 'git':
            raise Exception(f'Invalid server type: {content['server_type']}')

        # pathlib
        repo_path: str = os.path.join(os.path.join(Path(__file__).resolve().parent, '.sso-temp-repo'))
        if os.path.exists(repo_path) == True:
            shutil.rmtree(repo_path)
        os.mkdir(repo_path)

        file_path = content['file_uuid'] + '.sso'

        if content['server_type'] == 'webdav':
            os.chdir(repo_path)
            client = Client(content['server_address'], timeout=Timeout(60))

            if client.exists(file_path):
                client.download_file(file_path, os.path.join(repo_path, file_path))
                with open(os.path.join(repo_path, file_path), 'rb') as file:
                    content_enc = file.read()
                content_json: str = enc.decrypt(content_enc).decode()
                content_of_file_in_repo: dict = json.loads(content_json)
                content['data'] = content_of_file_in_repo['data']

        if content['server_type'] == 'git':
            repo = git.Repo.clone_from(content['server_address'], repo_path)
            repo = git.Repo(repo_path)
            os.chdir(repo_path)

            if os.path.isfile(file_path) == True:
                with open(file_path, 'rb') as file:
                    content_enc = file.read()
                content_json: str = enc.decrypt(content_enc).decode()
                content_of_file_in_repo: dict = json.loads(content_json)
                content['data'] = content_of_file_in_repo['data']

        data = content['data']
        adds = content['additions']
        rms = content['removals']

        for i in range(len(adds)):
            data.append(adds[i])

        for i in range(len(rms)):
            for j in range(len(data)):
                if data[j]['uuid'] == rms[i]:
                    del data[j]
                    break
        content['data'] = data
        content['additions'] = []
        content['removals'] = []

        # Until here everything should work

        content_json: str = json.dumps(content)
        content_enc: bytes = enc.encrypt(content_json.encode())

        with open(self.location, 'wb') as file:
            file.write(content_enc)

        # File does exist

        if content['server_type'] == 'webdav':
            client = Client(content['server_address'], timeout=Timeout(60))
            client.upload_file(self.location, file_path, overwrite=True)

        if content['server_type'] == 'git':
            repo =  git.Repo(repo_path)
            repo.index.add([file_path])
            commit_message = '[SSO] Synced data of profile ' + content['file_uuid'] + ' with client.'
            repo.index.commit(commit_message)

            origin = repo.remote(name='origin')
            origin.push()

    def overrite_file(self, name: str, value) -> None:
        if os.path.isfile(self.location) == True:
            with open(self.location, 'rb') as file:
                content_enc: bytes = file.read()

            enc = Fernet(self.key)
            content_json: str = enc.decrypt(content_enc).decode()
            content: dict = json.loads(content_json)

            content[name] = value

            content_json: str = json.dumps(content)
            content_enc: bytes = enc.encrypt(content_json.encode())

            with open(self.location, 'wb') as file:
                file.write(content_enc)
