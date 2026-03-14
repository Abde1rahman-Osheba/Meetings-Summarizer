from fastapi import APIRouter


router = APIRouter(prefix='/jobs', tags=['jobs'])


@router.get('/health')
def health() -> dict[str, str]:
    return {'module': 'jobs', 'status': 'ok'}
