from fastapi import APIRouter


router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/register')
def register() -> dict[str, str]:
    return {'status': 'registered'}


@router.post('/login')
def login() -> dict[str, str]:
    return {'status': 'logged_in'}


@router.post('/refresh')
def refresh() -> dict[str, str]:
    return {'status': 'refreshed'}


@router.get('/me')
def me() -> dict[str, str]:
    return {'user': 'current'}
