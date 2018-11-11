

class NoMessagesFoundException(Exception):
    def __init__(self, **kwargs):
        Exception.__init__(self)
        self.query = {}

        for key in kwargs:
            self.query[key] = kwargs[key]

    def __str__(self):
        error = "No Messages found.\n"
        query = "Query: \n"

        for key in self.query:
            query += "{} -> {}\n".format(key,self.query[key])

        return error + query