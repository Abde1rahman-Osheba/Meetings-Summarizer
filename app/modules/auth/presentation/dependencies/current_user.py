from fastapi import Depends


def get_current_user() -> dict[str, str]:
    return {'id': 'user-1', 'role': 'recruiter'}


CurrentUser = Depends(get_current_user)
