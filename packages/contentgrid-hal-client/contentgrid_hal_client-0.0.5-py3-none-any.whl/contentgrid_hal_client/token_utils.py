'''
Utilities for requesting and handling access tokens.
'''
import requests as re

class TokenData():
    '''
    Token data for requesting an access token.

    - scope: The scope of the token.
    - grant_type: The grant type of the token.
    - client_id: The client ID of the application.
    - client_secret: The client secret of the application.
    '''
    def __init__(self, scope: str, grant_type: str, client_id: str, client_secret: str) -> None:
        '''
        Initialize a TokenData with the following parameters:

        - scope: The scope of the token.
        - grant_type: The grant type of the token.
        - client_id: The client ID of the application.
        - client_secret: The client secret of the application.
        '''
        self.scope = scope
        self.grant_type = grant_type
        self.client_id = client_id
        self.client_secret = client_secret

    def to_dict(self) -> dict:
        '''
        Get the token data as a dictionary.

        Returns the token data as a dictionary.
        '''
        return {
            "scope": self.scope,
            "grant_type": self.grant_type,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }


def request_token(uri: str, data: TokenData) -> str:
    '''
    Given a URI and token data, request an access token.

    - uri: The URI to request the access token from.
    - data: The token data to use for the request.

    Returns the access token.
    '''
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = data.to_dict()
    res = re.post(uri, headers=headers, data=data)
    
    if res.status_code != 200:
        raise Exception(f'Failed to request token. Status code: {res.status_code}. Reason: {res.reason}')
    else:
        return res.json()['access_token']


def get_application_token(auth_uri: str, client_id: str, client_secret: str) -> str:
    '''
    Get an application token for the given client ID and client secret.

    - auth_uri: The authorization URI of the application.
    - client_id: The client ID of the application.
    - client_secret: The client secret of the application.

    Returns the application token.
    '''
    token_data = TokenData(
        scope='email',
        grant_type='client_credentials',
        client_id=client_id,
        client_secret=client_secret
    )
    acces_token = request_token(auth_uri, token_data)
    return acces_token