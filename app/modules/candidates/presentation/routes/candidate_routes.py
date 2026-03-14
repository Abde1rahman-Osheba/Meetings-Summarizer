from fastapi import APIRouter


router = APIRouter(prefix='/candidates', tags=['candidates'])


@router.get('/health')
def health() -> dict[str, str]:
    return {'module': 'candidates', 'status': 'ok'}
