from fastapi import APIRouter


router = APIRouter(prefix='/outreach', tags=['outreach'])


@router.get('/health')
def health() -> dict[str, str]:
    return {'module': 'outreach', 'status': 'ok'}
