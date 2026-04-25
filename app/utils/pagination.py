def paginate(queryset, page: int = 1, limit: int = 10):
    total = queryset.count()

    items = queryset.offset((page - 1) * limit).limit(limit).all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit,
        "data": items
    }