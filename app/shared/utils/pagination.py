def pagination_meta(total: int, page: int, size: int) -> dict[str, int]:
    return {"total": total, "page": page, "size": size}
