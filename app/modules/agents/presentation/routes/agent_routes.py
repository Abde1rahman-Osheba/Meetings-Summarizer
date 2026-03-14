from fastapi import APIRouter


router = APIRouter(prefix='/agents', tags=['agents'])


@router.get('/health')
def health() -> dict[str, str]:
    return {'module': 'agents', 'status': 'ok'}
