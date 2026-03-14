from fastapi import APIRouter


router = APIRouter(prefix='/interviews', tags=['interviews'])


@router.get('/health')
def health() -> dict[str, str]:
    return {'module': 'interviews', 'status': 'ok'}
