import requests
from utils import DOMAIN, PROJECT, TOKEN_SECRET, TOKEN_PUBLIC


class GerenciadorApi:

    def __init__(self) -> None:
        pass

    def __get_headers(self) -> dict:
        try:

            response = requests.get(f"https://{PROJECT}.supabase.co/rest/v1/rpc/get_last_token", headers={
                'apikey': TOKEN_PUBLIC,
                'Authorization': f'Bearer {TOKEN_SECRET}'
            })

            if response.status_code == 200 and len(response.json()) > 0:

                token = response.json()[0].get('token', None)

                if token is not None:
                    return {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}

        except Exception as e:
            return {}

    def __response(self, url: str, method: str, data: str | None = None) -> dict:
        try:
            if data is None:
                data = {}

            if method == 'GET':
                response = requests.get(url, headers=self.__get_headers())

            elif method == 'POST':
                response = requests.post(url, headers=self.__get_headers(), data=data)

            elif method == 'PUT':
                response = requests.put(url, headers=self.__get_headers(), data=data)

            else:
                return {}

            if response.status_code == 200 or response.status_code == 201:
                return response.json()['data']
            else:
                return {}

        except requests.exceptions.RequestException as e:
            return {}
        except Exception as e:
            return {}

    # Busca todas as filas vinculadas ao server rodando, para ativar.
    def find_filas_by_application(self, application: str, server_process: str) -> dict:
        __url = f'{DOMAIN}/fila?application={application}&server_process={server_process}'
        return self.__response(__url, 'GET')

    # Atualizar a fila, informando o status de processamento.
    def update_fila(self, payload: str) -> dict:
        __url = f'{DOMAIN}/fila'
        return self.__response(__url, 'PUT', payload)

    # Busca todos os dados do site para processar algum dado.
    def find_all_applications_by_application_name(self, name: str) -> dict:
        __url = f'{DOMAIN}/site?name={name}'
        return self.__response(__url, 'GET')

    # Atualiza a senha do site.
    def update_password_site(self, id: int, password: str) -> dict:
        __url = f'{DOMAIN}/site?id={id}&password={password}'
        return self.__response(__url, 'PUT')

    # Busca a ultima sessão gerado no site.
    def find_last_session_site(self, siteName: str) -> dict:
        __url = f'{DOMAIN}/sessao?siteName={siteName}'
        return self.__response(__url, 'GET')

    # Permite cadastrar a sessão.
    def create_session_by_user(self, payload: str) -> dict:
        __url = f'{DOMAIN}/sessao'
        return self.__response(__url, 'POST', payload)

    # Busca todas as filas vinculadas ao server rodando.
    def find_all_fila_playlist_by_application(self, application: str) -> dict:
        __url = f'{DOMAIN}/fila/playlist?application={application}'
        return self.__response(__url, 'GET')

    # Atualiza a fila, informando o status de processamento.
    def update_fila_playlist(self, payload: str) -> dict:
        __url = f'{DOMAIN}/fila/playlist'
        return self.__response(__url, 'PUT', payload)

    # Atualiza o site e tipo do container.
    def update_container(self, container_identifier: str, configuration_type: str, site_name: str) -> dict:
        __url = f'{DOMAIN}/container/sync-website?container_identifier={container_identifier}&configuration_type={configuration_type}&site_name={site_name}'
        return self.__response(__url, 'POST')
