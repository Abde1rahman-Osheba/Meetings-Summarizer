from fastapi import APIRouter


router = APIRouter(prefix='/audit', tags=['audit'])


@router.get('/health')
def health() -> dict[str, str]:
    return {'module': 'audit', 'status': 'ok'}
