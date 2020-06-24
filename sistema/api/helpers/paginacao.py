from flask import request, url_for


def paginacao(model, schema):
    page = int(request.args.get("pagina", 5))
    per_page = 5
    obj_paginacao = model.query.paginate(page=page, per_page=per_page)

    next = url_for(
        request.endpoint,
        pagina=obj_paginacao.next_num if obj_paginacao.has_next else obj_paginacao.page,
    )

    prev = url_for(
        request.endpoint,
        pagina=obj_paginacao.prev_num if obj_paginacao.has_prev else obj_paginacao.page,
    )

    return {
        "total": obj_paginacao.total,
        "paginas": obj_paginacao.pages,
        "next": next,
        "prev": prev,
        "resultado": schema.dump(obj_paginacao.items),
    }
