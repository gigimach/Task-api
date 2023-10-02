from fastapi import APIRouter, status, HTTPException, Depends
from presentation.models.viewmodels import UserCreate, UserRead
from application.auth_service import AuthRepository
import infrastructure.cryptograph.hash_provider as hash_provider
from infrastructure.cryptograph.jwt_token_provider import JWTTokenProvider
from presentation.models.viewmodels import LoginData
from presentation.utils.auth_utils import obter_usuario_logado


router = APIRouter()
prefix = '/auth'

auth_repo = AuthRepository()
jwt_provider = JWTTokenProvider()


@router.post('/signup', status_code=status.HTTP_201_CREATED)
def signup(user: UserCreate):

    user_found = auth_repo.get_user_by_login(user.login)

    if user_found:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Login já utilizado!')

    user.password = hash_provider.hash(user.password)
    user_created = auth_repo.save(user)
    return {'id': user_created.id}


@router.post('/signin', status_code=status.HTTP_200_OK)
def signin(input: LoginData):
    # verificar se usuário existe
    user_found = auth_repo.get_user_by_login(input.login)
    print(user_found)

    if not user_found:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Usuário e/ou senha incorretos!')

    # verificar a senha
    valid = hash_provider.verify(input.password, user_found.password)

    if not valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Usuário e/ou senha incorretos!')
    
    # gerar token
    token = jwt_provider.signin({"login": input.login})

    return {'access_token': token}


@router.get('/me', response_model=UserRead)
async def auth_me(user: LoginData = Depends(obter_usuario_logado)):
     return user