from fastapi import APIRouter


router = APIRouter(prefix='/organizations', tags=['organizations'])


@router.get('/health')
def health() -> dict[str, str]:
    return {'module': 'organizations', 'status': 'ok'}
