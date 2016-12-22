from pyramid.view import view_config


@view_config(route_name='home', renderer='templates/page-fullwidth.pt')
def my_view(request):
    return {'project': 'marc-digital-storage-11166', 'name':'V.I.Lenin'}
