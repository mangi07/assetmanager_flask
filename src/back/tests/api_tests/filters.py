class Filters:
    def __init__(self,
                 cost_greater_than=None,
                 cost_less_than=None,
                 location=None,
                 description=None):
        self.cost_greater_than = cost_greater_than # get all assets greater than cost
        self.cost_less_than = cost_less_than # get all assets less than cost
        self.location = location # get all assets at this location and all its child locations
        self.description = description # get all assets at this location and all its child locations

    def get_url_query_params(self):
        params = "?"
        if self.cost_greater_than:
            params = params + f"cost__gt={str(self.cost_greater_than)}&"
        if self.cost_less_than:
            params = params + f"cost__lt={str(self.cost_less_than)}&"
        if self.location:
            params = params + f"location_count.location__eq={str(self.location)}&"
        if self.description:
            params = params + f"desc__contains={str(self.description)}&"

        params = params[:-1]
        return params
