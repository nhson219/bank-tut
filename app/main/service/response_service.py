class ResponseService:
    def response(self, status, http_status_response, data):
        # print(repr(data))
        return {
            'status' : status,
            'http_status_response': http_status_response,
            'data' : data
        }
    def test(self):
        print(123)        