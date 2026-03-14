from fastapi import APIRouter


router = APIRouter(prefix='/matching', tags=['matching'])


@router.get('/health')
def health() -> dict[str, str]:
    return {'module': 'matching', 'status': 'ok'}
