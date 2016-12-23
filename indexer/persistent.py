from elasticsearch_dsl import Mapping, Nested, field
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.query import MultiMatch, Match

connections.create_connection(hosts=['indexer'], timeout=20)

# name your type
m = Mapping('my-type')

# add fields
m.field('title', 'string')

# you can use multi-fields easily
m.field('category', 'string', fields={'raw': field.String(index='not_analyzed')})

# you can also create a field manually
comment = Nested()
comment.field('author', field.String())
comment.field('created_at', field.Date())

# and attach it to the mapping
m.field('comments', comment)

# you can also define mappings for the meta fields
m.meta('_all', enabled=False)

# save the mapping into index 'my-index'
m.save('my-index')

#rc=MultiMatch(query='python django', fields=['title', 'body'])

#print(rc)


from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

client = Elasticsearch('indexer')

s = Search().using(client).query("match", title="python")
response = s.execute()
for hit in s:
    print(hit.title)


