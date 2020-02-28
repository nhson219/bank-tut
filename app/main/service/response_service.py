class ResponseService:
    def response(status = '', http_status_response = '', data = ''):
        return {
            'status' : status,
            'http_status_response': http_status_response,
            'data' : data
        }
