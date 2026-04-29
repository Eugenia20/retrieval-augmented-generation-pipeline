def paginate(query, page: int = 1, limit: int = 10):
    # safety limits
    page = max(page, 1)
    limit = min(max(limit, 1), 100)

    total = query.count()

    items = query.offset((page - 1) * limit).limit(limit).all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit,
        "data": items
    }