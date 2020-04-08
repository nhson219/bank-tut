class ResponseService:
    def response(self, status, http_status_response, data):
        print(data)
        return {
            'status' : status,
            'http_status_response': http_status_response,
            'data' : data
        }     
