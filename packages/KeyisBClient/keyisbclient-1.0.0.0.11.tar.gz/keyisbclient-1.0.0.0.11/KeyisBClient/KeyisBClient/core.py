
import re
from typing import Optional, List, Literal
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
import asyncio


class Url:
    def __init__(self, url_str: Optional[str] = None):
        self.interpreter: Optional[str] = None
        self.scheme: str = None # type: ignore
        self.hostname: str = None # type: ignore
        self.path: str = None # type: ignore
        self.query: str = None # type: ignore
        self.fragment: str = None # type: ignore
        self.params: dict = None # type: ignore

        if url_str:
            self.setUrl(url_str)
        
        

    def __parse_url(self, url_str: str):
        pattern = r"^(?P<interpreter>[A-Za-z0-9_]+):(?P<rest>[A-Za-z0-9_]+://.+)$"
        match = re.match(pattern, url_str)
        
        if match:
            interpreter = match.group("interpreter")
            rest_url = match.group("rest")
        else:
            interpreter = None
            rest_url = url_str
    
        parsed_url = urllib.parse.urlparse(rest_url)


        self.interpreter = interpreter
        self.scheme = parsed_url.scheme if parsed_url.scheme != '' else None # type: ignore

        self.hostname = parsed_url.netloc if parsed_url.netloc != '' else None # type: ignore
        self.path = parsed_url.path
        self.query = parsed_url.query
        self.fragment = parsed_url.fragment
        self.params = self.__parse_params(parsed_url.query)

    def __parse_params(self, query_str: str) -> dict:

        parsed = urllib.parse.parse_qs(query_str)
        cleaned = {k: v[0] if len(v) == 1 else v for k, v in parsed.items()}
        return cleaned

    def __str__(self):
        return self.getUrl()
    def setUrl(self, url_str: str):
        if url_str == '':
            url_str = '/'
        
        self.__parse_url(url_str)
        

    def getUrl(self, parts: List[Literal['interpreter', 'scheme', 'hostname', 'path', 'params', 'fragment']] = ['scheme', 'hostname', 'path', 'params', 'fragment']) -> str:
        scheme = self.scheme if'scheme' in parts else ''
        hostname = self.hostname if 'hostname' in parts else ''
        params = urllib.parse.urlencode(self.params, doseq=True) if 'params' in parts else ''
        path = self.path if 'path' in parts else ''
        fragment = self.fragment if 'fragment' in parts else ''

        if scheme is None: scheme = ''
        if hostname is None: hostname = ''



        url = urllib.parse.urlunparse((
            scheme, hostname, path, '', params, fragment
        ))
        url = f'{self.interpreter}:{url}' if 'interpreter' in parts and self.interpreter is not None else url


        if 'path' not in parts:
            if url.endswith(':'):
                url = url[:-1]

        if 'scheme' not in parts:
            if url.startswith('//'):
                url = url[2:]

        
        return url
    def isSchemeSecure(self) -> bool:
        return self.scheme in ('https', 'mmbps')
    
    def getDafaultUrl(self) -> 'Url':
        _url = Url(self.getUrl())


        if _url.scheme in ('mmbp', 'mmbps'):
            with ThreadPoolExecutor() as executor:
                future = executor.submit(self.__run_asyncio_task_fetch_sync__, _url.hostname)
                result = future.result()
                _url.hostname = result
        if _url.scheme == 'mmbps': _url.scheme = 'https'

        return _url

        
            

    def __run_asyncio_task_fetch_sync__(self, hostname):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            import KeyisBClient
            result = loop.run_until_complete(KeyisBClient.Client.getDNS(hostname))
        finally:
            loop.close()
        return result

