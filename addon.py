
import sys
import json
import datetime
from mitmproxy import http

class Redirector:
    def __init__(self):
        self.target_url = "https://ampcode.com"

    def request(self, flow: http.HTTPFlow) -> None:
        # Log the request details
        request_data = {
            'timestamp': datetime.datetime.now().isoformat(),
            'method': flow.request.method,
            'url': flow.request.pretty_url,
            'host': flow.request.host,
            'port': flow.request.port,
            'path': flow.request.path,
            'query': flow.request.query.decode() if flow.request.query else None,
            'headers': dict(flow.request.headers),
            'body': flow.request.content.decode('utf-8', errors='ignore') if flow.request.content else None,
            'scheme': flow.request.scheme
        }
        
        # Write to jsonl file
        with open('output.jsonl', 'a') as f:
            f.write(json.dumps(request_data) + '\n')
        
        # Keep original host for later use
        original_host = flow.request.host
        original_port = flow.request.port
        
        # Parse the target URL to get the new host
        if not self.target_url.startswith(('http://', 'https://')):
            self.target_url = 'http://' + self.target_url
            
        # Modify the URL
        flow.request.scheme = self.target_url.split('://')[0]
        flow.request.host = self.target_url.split('://')[1].split('/')[0]
        if ':' in flow.request.host:
            flow.request.host, port = flow.request.host.split(':')
            flow.request.port = int(port)
        else:
            flow.request.port = 443 if flow.request.scheme == 'https' else 80
            
        # Add headers to help debug
        flow.request.headers['X-Original-Host'] = original_host
        flow.request.headers['X-Original-Port'] = str(original_port)
        flow.request.headers['X-Forwarded-By'] = 'mitm-proxy'

addons = [Redirector()]
