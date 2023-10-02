from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt

from infrastructure.cryptograph.jwt_token_provider import JWTTokenProvider
from application.auth_service import AuthRepository

oauth2_schema = OAuth2PasswordBearer(tokenUrl='signin')


async def obter_usuario_logado(
        token: str = Depends(oauth2_schema),
        jwt_provider = Depends(JWTTokenProvider),
        auth_repository = Depends(AuthRepository)
):

    try:
        payload = jwt_provider.decode(token)
        login = payload.get('login')  
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token expirado'
        )
    except jwt.DecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Erro ao decodificar o token'
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'Erro desconhecido ao processar o token: {str(e)}'
        )
    
    if not login:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token inválido: não foi possível encontrar o campo "login" no payload'
        )
    
    usuario = auth_repository.get_user_by_login(login)

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Usuário não encontrado'
        )

    return usuario






