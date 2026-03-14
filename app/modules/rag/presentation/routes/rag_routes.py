from fastapi import APIRouter


router = APIRouter(prefix='/rag', tags=['rag'])


@router.get('/health')
def health() -> dict[str, str]:
    return {'module': 'rag', 'status': 'ok'}
