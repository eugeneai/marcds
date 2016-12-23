from pyramid.view import view_config

import marcds.searcher as searcher

@view_config(route_name='home', renderer='templates/page-fullwidth.pt')
def my_view(request):
    if request.method == "POST":
        q=request.POST.get("q", None)
        print(repr(q))
        if q is None or q.strip()=="":
            result = "!!!wrong query"
        else:
            records = searcher.search(q, limit=10)
            # Найти книгу
            if records:
                # Преобразование формата marc21
                pass
            else:
                result="!!!not found"
    else:
        result = None
    request.POST
    return {'project': 'Цифровой архив ИДСТУ СО РАН', "result":result}
