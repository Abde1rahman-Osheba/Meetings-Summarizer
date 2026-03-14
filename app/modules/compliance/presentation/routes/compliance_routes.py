from fastapi import APIRouter


router = APIRouter(prefix='/compliance', tags=['compliance'])


@router.get('/health')
def health() -> dict[str, str]:
    return {'module': 'compliance', 'status': 'ok'}
