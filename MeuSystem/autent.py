import requests as requestss

class Bd:
    API_KEY = 'AIzaSyCehwb75WGgdGYS2QAuY0jC2EzxXMvYpGo'
    localId = None
    idToken = None

    def login(self, email, senha):

        lk = f'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.API_KEY}'

        info = f'{{"email": "{email}", "password": "{senha}", "returnSecureToken": true}}'
        log = requestss.post(lk, data=info)
        

        if log.ok:
            log = log.json()
            localId = log['localId']
            idToken = log['idToken']
            refreshToken = log['refreshToken']

            with open('refreshT.txt', 'w') as arq:
                arq.write(refreshToken)

            self.localId = localId
            self.idToken = idToken
            

        else:
            self.localId = None
            self.idToken = None
            
            log = log.json()
            rep = log['error']['message']
            if rep in ('INVALID_EMAIL', 'EMAIL_NOT_FOUND'):
            	rep = 'e-mail invalido!'
            
            if rep == 'INVALID_PASSWORD':
            	rep = 'senha invalida!'
            	
            if rep == 'MISSING_PASSWORD':
            	rep = 'digite sua senha!'
            	

    def manter_log(self, token):

        lk = f'https://securetoken.googleapis.com/v1/token?key={self.API_KEY}'

        info = {"grant_type": "refresh_token", "refresh_token": token}
        log = requestss.post(lk, data=info)

        if log.ok:
            log = log.json()
            localId = log['user_id']
            idToken = log['id_token']
            refreshToken = log['refresh_token']

            with open('refreshT.txt', 'w') as arq:
                arq.write(refreshToken)

            self.localId = localId
            self.idToken = idToken
        
        else:
            self.localId = None
            self.idToken = None
