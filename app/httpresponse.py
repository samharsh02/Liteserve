class HttpResponse:
    STATUS_MESSAGES = {
        200: "OK",
        400: "Bad Request",
        404: "Not Found",
        500: "Internal Server Error"
    }

    def __init__(self, status_code=200, content_type='text/plain', body=''):
        self.status_code = status_code
        self.content_type = content_type
        self.body = body

    def to_http_response(self):
        status_message = self.STATUS_MESSAGES.get(self.status_code, "OK")
        response_line = f"HTTP/1.1 {self.status_code} {status_message}\r\n"

        headers = (
            f"Content-Type: {self.content_type}\r\n"
            f"Content-Length: {len(self.body.encode('utf-8'))}\r\n"
        )

        blank_line = "\r\n"
        response = response_line + headers + blank_line + self.body
        return response.encode('utf-8')

    @classmethod
    def ok(cls, body='', content_type='text/plain'):
        return cls(200, content_type, body).to_http_response()

    @classmethod
    def not_found(cls, body='', content_type='text/plain'):
        return cls(404, content_type, body).to_http_response()

    @classmethod
    def bad_request(cls, body='', content_type='text/plain'):
        return cls(400, content_type, body).to_http_response()

    @classmethod
    def internal_error(cls, body='', content_type='text/plain'):
        return cls(500, content_type, body).to_http_response()
