# BUILDING QUERIES #####
from neuromorphopy import QueryFields

# Get available fields
fields = QueryFields.get_fields()

# Get valid values for a field
values = QueryFields.get_values("brain_region")

# Get complete reference
reference = QueryFields.describe()

print(fields)
print(values)

# SEARCHING AND DOWNLOADING #####
from neuromorphopy import Query, search_and_download

query = Query.from_file("test_query.yaml")
search_and_download(query, "./neurons")
