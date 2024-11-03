class HttpToRequestsConverter:
    def __init__(self, raw_http):
        self.raw_http = raw_http.strip()
        self.__method = None
        self.__url = None
        self.__headers = {}
        self.__cookies = {}
        self.__body = None
        self._parse_http()

    def _parse_http(self):
        # Split headers and body
        request_parts = self.raw_http.split('\n\n', 1)
        header_lines = request_parts[0].splitlines()

        # Parse the request line (GET / HTTP/1.1)
        request_line = header_lines[0]
        self.__method, self.__path, _ = request_line.split()

        self.__url = self._get_full_url()

        # Parse headers
        for line in header_lines[1:]:
            if line.strip():  # Ignore empty lines
                key, value = line.split(":", 1)
                key, value = key.strip(), value.strip()

                # Separate cookies if found
                if key.lower() == "cookie":
                    self._parse_cookies(value)
                else:
                    self.headers[key] = value

        # Parse body if it exists
        if len(request_parts) > 1:
            self.__body = request_parts[1].strip()

    def _get_full_url(self):
        # Check if the URL is relative
        if self.__path.startswith("http"):
            return self.__path
        else:
            # Add the protocol (http) and host if it's missing
            host = self.headers.get("Host", "")
            return f"http://{host}{self.__path}" if host else self.__path

    def _parse_cookies(self, cookie_header):
        # Parse cookies from Cookie header
        cookies = cookie_header.split(";")
        for cookie in cookies:
            key, value = cookie.strip().split("=", 1)
            self.__cookies[key.strip()] = value.strip()

    @property
    def url(self):
        return self._get_full_url()

    @property
    def cookies(self):
        return self.__cookies

    @property
    def headers(self):
        return self.__headers

    @property
    def method(self):
        return self.__method

    @property
    def body(self):
        return self.__body

