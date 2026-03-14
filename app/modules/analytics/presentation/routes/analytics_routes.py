from fastapi import APIRouter


router = APIRouter(prefix='/analytics', tags=['analytics'])


@router.get('/health')
def health() -> dict[str, str]:
    return {'module': 'analytics', 'status': 'ok'}
