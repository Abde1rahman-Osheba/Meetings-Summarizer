from fastapi import APIRouter


router = APIRouter(prefix='/users', tags=['users'])


@router.get('/health')
def health() -> dict[str, str]:
    return {'module': 'users', 'status': 'ok'}
