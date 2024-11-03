import os
import time
import requests
import urllib.parse
import re
import socket
import ssl

# Constants
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0"


def req(url, method='get', headers={}, params=None, data=None, timeout=30, proxies={}, parsed=False, selector=None, **kwargs):
    """
    Unified request function resembling Axios signatures, using kwargs.

    Args:
        url (str): The URL to request.
        method (str): HTTP method (default: 'get').
        headers (dict): Request headers (default: None).
        params (dict): URL parameters (default: None).
        data (dict): Request body for POST requests (default: None).
        timeout (int): Request timeout in seconds (default: 30).
        proxy (str): Proxy to use for the request (default: None).
        parse_html (bool): Whether to parse the HTML response (default: False).
        selector (str): CSS selector for parsing HTML (default: None).
        **kwargs: Additional keyword arguments to pass to the requests method.

    Returns:
        dict: Response object with data, status, headers, etc.
    """
    method = method.lower()
    headers = {**headers, 'User-Agent': DEFAULT_USER_AGENT}

    session = requests.Session()
    try:
        if method == 'get':
            response = session.get(url, headers=headers, params=params, proxies=proxies, timeout=timeout, **kwargs)
        elif method == 'post':
            response = session.post(url, headers=headers, params=params, data=data, proxies=proxies, timeout=timeout, **kwargs)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        result = {
            'data': response.text,
            'status': response.status_code,
            'statusText': response.reason,
            'headers': dict(response.headers),
            'config': {
                'url': url,
                'method': method,
                'headers': headers,
                'params': params,
                'data': data,
                'timeout': timeout,
                'proxies': proxies,
                'parse_html': parsed,
                'selector': selector,
                **kwargs,
            },
        }

        if parsed:
            result['parsed'] = parse(response.text, selector)

        return result
    except requests.RequestException as e:
        return {
            'error': str(e),
            'config': {
                'url': url,
                'method': method,
                'headers': headers,
                'params': params,
                'data': data,
                'timeout': timeout,
                'proxy': proxy,
                'parse_html': parsed,
                'selector': selector,
                **kwargs,
            },
        }


def parse():
    from selectolax.parser import HTMLParser

    html = HTMLParser(response.text)
    if selector:
        return html.css(selector)
    return html


def make_playwright_browser(headless=False):
    from playwright.sync_api import sync_playwright

    playwright = sync_playwright().start()
    return playwright.firefox.launch(headless=headless), playwright


def get_page_playwright(browser, url, new_context=False, delay=2, waitcondition=lambda: True, waitcondition_polling=0.2, waitcondition_retries=10):
    try:
        context = browser.new_context() if new_context else None
        page = context.new_page() if new_context else browser.new_page()
        page.goto(url)
        for retry in range(waitcondition_retries):
            if waitcondition():
                break
            time.sleep(waitcondition_polling)
        return page.content()
    except Exception as e:
        print(repr(e))


def parse_header(*firefoxAllHeaders, file=""):
    rawheader = firefoxAllHeaders[0] if firefoxAllHeaders else jload(file)
    serializedHeaders = list(rawheader.values())[0]["headers"]
    return {k: v for k, v in [x.values() for x in serializedHeaders]}


def parse_raw_headers(fpath, log=0):
    headers = {}
    for x in open(fpath).read().split('\n'):
        d = dict([y.strip() for y in x.split(':', 1)])
        headers.update(d)
        if log:
            print(d)
    return headers


def make_cookie(req):
    return ";".join([f"{k}={v}" for k, v in req.cookies.items()])


def auto_encoder(d):
    '''encode dict to url get params'''
    return "&".join([f"{k}={urllib.parse.quote_plus(str(v))}" for k, v in d.items()])


# Socket utility functions
def create_ssl_context(verify=True, cert=None):
    context = ssl.create_default_context()
    if not verify:
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
    if cert:
        context.load_cert_chain(cert)
    return context


def socket_request(host, port, request, use_ssl=False, timeout=30):
    """
    Make a raw socket request.

    Args:
        host (str): The hostname to connect to.
        port (int): The port to connect to.
        request (str): The raw request string.
        use_ssl (bool): Whether to use SSL/TLS.
        timeout (int): Connection timeout in seconds.

    Returns:
        str: The response from the server.
    """
    sock = socket.create_connection((host, port), timeout=timeout)

    try:
        if use_ssl:
            context = create_ssl_context()
            sock = context.wrap_socket(sock, server_hostname=host)

        sock.sendall(request.encode())

        response = b""
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response += chunk

        return response.decode()
    finally:
        sock.close()


def to_md(inpt, select="main"):
    from markdownify import markdownify
    import selectolax

    if isinstance(inpt, selectolax.parser.HTMLParser):
        dom = inpt
    else:
        dom = selectolax.parser.HTMLParser(inpt)

    for el in dom.css('script, style, link, footer'):
        el.decompose()

    html = dom.html
    if select:
        html = dom.css_first(select).html
    result: str = markdownify(html)
    return result


if __name__ == "__main__":
    from markdownify import markdownify

    # Example usage:
    url = "https://www.lesswrong.com/posts/Sdi7gkKSHkRspqqcG/liquid-vs-illiquid-careers?utm_source=tldrnewsletter#Navigating_Illiquid_Paths__Psychology__Career_Management__and_Social_Capital"
    response = req(url)

    print(markdownify(response['data']))
