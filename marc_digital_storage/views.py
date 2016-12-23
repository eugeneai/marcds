from pyramid.view import view_config


@view_config(route_name='home', renderer='templates/page-fullwidth.pt')
def my_view(request):
    if request.method == "POST":
        # Найти книгу
        result="not found"
    else:
        result = None
    request.POST
    return {'project': 'Цифровой архив ИДСТУ СО РАН', "result":result}
