from pyramid.view import view_config

import marcds.searcher as searcher

M={
    "650":"Вид документа",
    "082":"Шифр издания",
    "100":"Автор(ы)",
    "245":"Заглавие",
    "260":"Выходные данные",
    "300":"Колич.характеристики",
    "246":"Предметные рубрики",
}


def to_html(marc):
    l=[]
    for field in marc:
        sf = ";".join([v for k,v in field])
        name=M.get(field.tag, field.tag)
        row = "<b>{}</b>: {}".format(name,sf)
        l.append(row)
    html="<br/>".join(l)
    return html


@view_config(route_name='home', renderer='templates/page-fullwidth.pt')
def my_view(request):
    value=''
    if request.method == "POST":
        q=request.POST.get("q", None)
        if q is None or q.strip()=="":
            result = "!!!wrong query"
            value = ''
        else:
            q=q.strip()
            value = q
            records = searcher.search(q, limit=10)
            # Найти книгу
            if records:
                text_parts=[]
                for rec in records:
                    #srec=str(rec)
                    srec=to_html(rec)
                    text_parts.append(srec)
                # Преобразование формата marc21
                text="<br/><br/>".join(text_parts)
                result=text
                pass
            else:
                result="!!!not found"
    else:
        result = None
    print(result)
    request.POST
    return {'project':
            'Цифровой архив ИДСТУ СО РАН',
            "result":result,
            "value":value
    }
