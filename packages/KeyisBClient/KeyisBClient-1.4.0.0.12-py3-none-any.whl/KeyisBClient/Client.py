

import os
import httpx
import asyncio
from typing import Optional, Union,  AsyncIterable
import logging as logging2
logging2.basicConfig(level=logging2.INFO)
import tempfile
from concurrent.futures import ThreadPoolExecutor

from KeyisBLogging import logging

from .Exceptions import Exceptions
from .core import Url


class _Client:
    def __init__(self):
        self.__servers = {}

        self.__root_dns_server = 'http://51.250.85.38:50000'
        self.addServer(self.__root_dns_server)

        self.__ca_crt = """
-----BEGIN CERTIFICATE-----
MIIDozCCAougAwIBAgIUZPOwLkKJSodBsrye8uGyCDfS2WswDQYJKoZIhvcNAQEL
BQAwYTELMAkGA1UEBhMCVVMxDjAMBgNVBAgMBVN0YXRlMQ0wCwYDVQQHDARDaXR5
MRUwEwYDVQQKDAxPcmdhbml6YXRpb24xDTALBgNVBAsMBFVuaXQxDTALBgNVBAMM
BE15Q0EwHhcNMjQxMDEzMDA0MTM4WhcNMzQxMDExMDA0MTM4WjBhMQswCQYDVQQG
EwJVUzEOMAwGA1UECAwFU3RhdGUxDTALBgNVBAcMBENpdHkxFTATBgNVBAoMDE9y
Z2FuaXphdGlvbjENMAsGA1UECwwEVW5pdDENMAsGA1UEAwwETXlDQTCCASIwDQYJ
KoZIhvcNAQEBBQADggEPADCCAQoCggEBAK0UapAmQ/6tQ5FGcqmCzs9E+plXK8J3
I+93urrqUAwmU8GVmEJHfHWid16HYK8qrUrDslVWwOS9Oz+7TcXRRvY9VihKdm0D
JS8ba0ry4xIX0tIXQ2+lpOhBQ9dyTcte5Ob049DNZrKWDiAtXgC4IF7MGNTtBPLj
abdKeHowxLzwbJIje3tHhFB6Haz5+xHHZdqU13uhmOd+HzXOIYOKoB3QeFCH91Ll
U9WXrxtjT8gNnyWMbiEjnifoPQISv2r2K284PaJhe+EnzH2HEclSS8mjlvvUn5pd
AOX4YM6q1BTGZRmswTOUHECDsFPcqOA8KO1b8AfVDcFSJgiL6Wdh71sCAwEAAaNT
MFEwHQYDVR0OBBYEFPLj7vlEwwzgRNM61uRpU41K+kfjMB8GA1UdIwQYMBaAFPLj
7vlEwwzgRNM61uRpU41K+kfjMA8GA1UdEwEB/wQFMAMBAf8wDQYJKoZIhvcNAQEL
BQADggEBAAqJNsbtJzPTsN9jzfMW8wqkwCN13cdENdpoRfmm28rTRimOQIF4h6Cn
xG4PkLjVQ0bWeTwmLy1PBUX4zVwQ1d/7hrvrG96cCmcTmOuyxCPL8H6wWlWPOBu1
aOL4ufmQ7kNokW6JEyeV9eKxBrOH1cj0g+dEN3+/cmMfcchmkgzV+lZdwQi2MPTy
/0X8VFCwk+xj8ub24GUYQAfxdG4vVw6c1y5znSDA5v7J36l2Z6jMJTruzUnV0xFz
ZD67YhdblKrtvSXLoUbFfhaUbtNlzj2qqwhnL4PPZQQ1h8TpVt9LlEI0A01nZ1s6
3cnEYOLHpCNUYqELwlE9QTj+BaQAQak=
-----END CERTIFICATE-----
"""
        self.__protocols = {
            'mmbp':'http',
            'mmbps':'https'
        }
        self.ssl_certificate = self._create_ca_file()
        self.__httpxClient_mmbps = httpx.AsyncClient(verify = self.ssl_certificate)
        self.__httpxClient_https = httpx.AsyncClient()

    def _create_ca_file(self):
        temp_cert = tempfile.NamedTemporaryFile(delete=False, suffix=".crt")
        temp_cert.write(self.__ca_crt.encode())
        temp_cert.close()
        return temp_cert.name
    
    async def getDNS(self, domain: str) -> str:
        """
        Получение DNS-адреса из сети DNS GW

        :param domain: 
        """
        ip_address, port = await self._resolve_dns(domain)
        result = f"{ip_address}:{port}"
        return result
    
    async def get(self, url: Union[Url, str], data=None, json: Optional[dict] = None, headers=None, stream: bool = False) -> httpx.Response:
        return await self.fetch(url, "GET", data, json, headers, stream)
    async def post(self, url: Union[Url, str], data=None, json: Optional[dict] = None, headers=None, stream: bool = False) -> httpx.Response:
        return await self.fetch(url, "POST", data, json, headers, stream)
    async def put(self, url: Union[Url, str], data=None, json: Optional[dict] = None, headers=None, stream: bool = False) -> httpx.Response:
        return await self.fetch(url, "PUT", data, json, headers, stream)
    async def patch(self, url: Union[Url, str], data=None, json: Optional[dict] = None, headers=None, stream: bool = False) -> httpx.Response:
        return await self.fetch(url, "PATCH", data, json, headers, stream)
    
        
        

    async def fetch(self, url: Union[Url, str], method: str = 'GET', data=None, json: Optional[dict] = None, headers=None, stream: bool = False) -> httpx.Response:
        """
        Асинхронный метод для выполнения запросов к серверам MMBPS и HTTPS.
        """
        if isinstance(url, str):
            url = Url(url)



        if url.scheme in ('mmbps', 'mmbp'):
            response = await self._fetch_mmbps(url, method, data, json, headers, stream)
        elif url.scheme in ('https', 'http'):
            response = await self._fetch_any(url, method, data, json, headers, stream)
        else:
            raise ValueError("Unsupported URL scheme")
        
        return response # type: ignore

    def fetch_sync(self, url: str, method: str = 'GET', data=None, json=None, headers=None, stream: bool = False, verify = False):
        """Синхронный метод для выполнения запросов."""
        with ThreadPoolExecutor() as executor:
            future = executor.submit(self._run_asyncio_task_fetch_sync__, url, method, data, json, headers, stream)
            result = future.result()
        return result

    def _run_asyncio_task_fetch_sync__(self, url, method, data, json, headers, stream):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(self.fetch(url, method, data, json, headers, stream))
        finally:
            loop.close()
        return result

    async def _fetch_any(self, url: Url, method: str = 'GET', data=None, json=None, headers=None, stream=False, verify = False) -> Union[AsyncIterable[bytes], httpx.Response]:
        if stream:
            return self._fetch_https_stream(url, method, data, json, headers)
        else:
            if url.hostname not in self.__servers:
                return await self._fetch_https(url, method, data, json, headers, verify)
            else:
                return await self._fetch_https_keep_alive(url, method, data, json, headers)

    async def _fetch_https_stream(self, url: Url, method: str = 'GET', data=None, json=None, headers=None) -> AsyncIterable[bytes]:
        """Стриминг HTTPS запроса с использованием httpx."""
        async with httpx.AsyncClient() as client:
            try:
                async with client.stream(method, url.getUrl(), data=data, json = json, headers=headers) as response:
                    logging.debug(f"HTTPS stream response received: {response.status_code}")

                    async for chunk in response.aiter_bytes():
                        yield chunk

            except httpx.TimeoutException:
                logging.debug("HTTPS request timed out")
                raise Exceptions.ServerTimeoutError("Запрос к серверу завершился по тайм-ауту")

            except httpx.ConnectError:
                logging.debug("Failed to connect to server")
                raise Exceptions.ErrorConnection("Не удалось подключиться к серверу")

            except httpx.HTTPStatusError as e:
                logging.debug(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
                raise Exceptions.InvalidServerResponseError(f"Некорректный ответ от сервера: {e.response.status_code}")

            except httpx.RequestError as e:
                logging.debug(f"HTTPS request failed: {e}")
                raise Exceptions.UnexpectedError(f"Неожиданная ошибка запроса HTTPS: {str(e)}")

    async def _get_mmb_verify_crt(self, url: Url) -> Union[bool, str]:
        if url.scheme == 'mmbps':
            return self.ssl_certificate
        else:
            return False
    async def _fetch_https(self, url: Url, method: str = 'GET', data=None, json=None, headers=None, verify=False) -> httpx.Response:
        async with httpx.AsyncClient(verify=verify, follow_redirects=True) as client:
            try:
                response = await client.request(method, url.getUrl(), data=data, json=json, headers=headers)
                return response

            except httpx.TimeoutException:
                logging.debug("HTTPS request timed out")
                raise Exceptions.ServerTimeoutError("Запрос к серверу завершился по тайм-ауту")

            except httpx.ConnectError:
                logging.debug("Failed to connect to server")
                raise Exceptions.ErrorConnection("Не удалось подключиться к серверу")

            except httpx.HTTPStatusError as e:
                logging.debug(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
                raise Exceptions.InvalidServerResponseError(f"Некорректный ответ от сервера: {e.response.status_code}")

            except httpx.RequestError as e:
                logging.debug(f"HTTPS request failed: {e}")
                raise Exceptions.UnexpectedError(f"Неожиданная ошибка запроса HTTPS: {str(e)}")
    async def _fetch_https_keep_alive(self, url: Url, method: str = 'GET', data=None, json=None, headers=None) -> httpx.Response:
        try:
            response = await self.__httpxClient_mmbps.request(method, url.getUrl(), data=data, json=json, headers=headers)
            return response

        except httpx.TimeoutException:
            logging.debug("HTTPS request timed out")
            raise Exceptions.ServerTimeoutError("Запрос к серверу завершился по тайм-ауту")

        except httpx.ConnectError:
            logging.debug("Failed to connect to server")
            raise Exceptions.ErrorConnection("Не удалось подключиться к серверу")

        except httpx.HTTPStatusError as e:
            logging.debug(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            raise Exceptions.InvalidServerResponseError(f"Некорректный ответ от сервера: {e.response.status_code}")

        except httpx.RequestError as e:
            logging.debug(f"HTTPS request failed: {e}")
            raise Exceptions.UnexpectedError(f"Неожиданная ошибка запроса HTTPS: {str(e)}")

    async def _fetch_mmbps(self, url: Url, method: str = 'GET', data=None, json = None, headers=None, stream: bool = False):

        ip_address, port = await self._resolve_dns(url.hostname)
        verify = await self._get_mmb_verify_crt(url)
        url.hostname = f'{ip_address}:{port}'
        url.scheme = self.__protocols[url.scheme]
        return await self._fetch_any(url, method, data, json, headers, stream, verify = verify) # type: ignore

    async def _resolve_dns(self, hostname: str):
        
        dns_query_url = f"{self.__root_dns_server}/servers?d={hostname}"
        
        async with httpx.AsyncClient(verify=False) as client:
            try:
                response = await client.get(dns_query_url)
                if response.status_code == 404:
                    logging.error(f"DNS request failed: {response.status_code} - Server Not Found")
                    raise Exceptions.DNS.DNSServerNotFoundError("DNS server not found")
                elif response.status_code == 403:
                    logging.error(f"DNS request failed: {response.status_code} - Access Denied")
                    raise Exceptions.DNS.DNSAccessDeniedError("Access denied to DNS server")
                elif response.status_code == 500:
                    logging.error(f"DNS request failed: {response.status_code} - Server Failure")
                    raise Exceptions.DNS.DNSServerFailureError("DNS server failure")
                elif response.status_code != 200:
                    logging.error(f"DNS request failed: {response.status_code}")
                    raise Exceptions.DNS.UnexpectedError("Invalid DNS response status")

                result = response.json()
                ip_address = result.get('ip')
                if not ip_address:
                    raise Exceptions.DNS.DNSResponseError("Invalid DNS response format: 'ip' field is missing")

                port = result.get('port', 443)
                return ip_address, port

            except httpx.TimeoutException:
                logging.debug("Connection timeout during DNS resolution")
                raise Exceptions.DNS.DNSTimeoutError("Timeout during DNS resolution")
            except httpx.RequestError as e:
                logging.debug(f"Request error during DNS resolution: {e}")
                raise Exceptions.DNS.ErrorConnection("Connection error during DNS resolution")
            except Exception as e:
                logging.debug(f"Unexpected error during DNS resolution: {e}")
                raise Exceptions.DNS.UnexpectedError("Unexpected error during DNS resolution")


    def addServer(self, server_url: str):
        """Добавить постоянное подключение к серверу."""
        self.__servers[server_url] = True

    def delServer(self, server_url: str):
        """Удалить постоянное подключение к серверу."""
        if server_url in self.__servers:
            del self.__servers[server_url]
            logging.debug(f"Server removed: {server_url}")
    
    def close(self):
        if os.path.exists(self.ssl_certificate):
            os.remove(self.ssl_certificate)
Client = _Client()





