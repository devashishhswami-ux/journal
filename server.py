import http.server
import socketserver
import urllib.request
import urllib.parse
import json
import os

PORT = 8080

class JournalHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Handle Translation API Proxy
        if self.path.startswith('/api/translate'):
            try:
                # Parse query parameters
                query = urllib.parse.urlparse(self.path).query
                params = urllib.parse.parse_qs(query)
                text = params.get('text', [''])[0]
                target_lang = params.get('target', ['es'])[0] # Default to Spanish

                if not text:
                    self.send_response(400)
                    self.end_headers()
                    return

                # Reliable Google Translate Script Endpoint (GTX)
                # Client=gtx is often used for this.
                google_url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target_lang}&dt=t&q={urllib.parse.quote(text)}"
                
                # Make request from Server (Bypasses Browser CORS)
                req = urllib.request.Request(google_url)
                req.add_header('User-Agent', 'Mozilla/5.0') # Fake UA helps
                
                with urllib.request.urlopen(req) as response:
                    data = response.read()
                    
                    # Google returns raw nested lists. We forward this raw JSON or process it.
                    # Let's process it slightly to ensure we return a clean JSON object.
                    raw_json = json.loads(data.decode('utf-8'))
                    
                    # Extract translated text
                    translated_text = ""
                    if raw_json and isinstance(raw_json, list) and len(raw_json) > 0:
                        # Iterating over segments
                        for segment in raw_json[0]:
                            if segment and len(segment) > 0:
                                translated_text += segment[0]
                    
                    response_data = json.dumps({'translatedText': translated_text})
                    
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(response_data.encode('utf-8'))

            except Exception as e:
                print(f"Translation Error: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
        else:
            # Default Static File Serving
            super().do_GET()

print(f"Starting Robust Journal Server at http://localhost:{PORT}")
print("Features: Local File Serving + Translation Proxy Endpoint")

with socketserver.TCPServer(("", PORT), JournalHandler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
