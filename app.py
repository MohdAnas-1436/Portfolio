#!/usr/bin/env python3
"""
Portfolio Website Server
A Flask-style portfolio website using Python's built-in HTTP server
"""

import http.server
import socketserver
import os
import urllib.parse
from datetime import datetime
import json

class PortfolioHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.serve_index()
        elif self.path.startswith('/static/'):
            self.serve_static_file()
        else:
            super().do_GET()
    
    def do_POST(self):
        if self.path == '/contact':
            self.handle_contact_form()
        else:
            self.send_error(404)
    
    def serve_index(self):
        try:
            with open('templates/index.html', 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except FileNotFoundError:
            self.send_error(404)
    
    def serve_static_file(self):
        # Remove /static/ prefix and serve from static directory
        file_path = self.path[8:]  # Remove '/static/'
        try:
            if file_path.endswith('.css'):
                content_type = 'text/css'
            elif file_path.endswith('.js'):
                content_type = 'application/javascript'
            else:
                content_type = 'text/plain'
            
            with open(f'static/{file_path}', 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except FileNotFoundError:
            self.send_error(404)
    
    def handle_contact_form(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            form_data = urllib.parse.parse_qs(post_data)
            
            # Extract form data
            name = form_data.get('name', [''])[0]
            email = form_data.get('email', [''])[0]
            message = form_data.get('message', [''])[0]
            
            # Save to file
            timestamp = datetime.now().isoformat()
            submission = f"""
=== Contact Form Submission ===
Date: {timestamp}
Name: {name}
Email: {email}
Message: {message}
================================

"""
            
            with open('contact_submissions.txt', 'a', encoding='utf-8') as f:
                f.write(submission)
            
            # Send success response
            response_html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Message Sent - Mohd Anas Portfolio</title>
                <style>
                    body { 
                        font-family: Arial, sans-serif; 
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                    }
                    .container { 
                        text-align: center; 
                        background: rgba(0,0,0,0.3);
                        padding: 2rem;
                        border-radius: 10px;
                        backdrop-filter: blur(10px);
                    }
                    .success { color: #4ade80; }
                    a { 
                        color: #a855f7; 
                        text-decoration: none;
                        background: rgba(168, 85, 247, 0.2);
                        padding: 0.5rem 1rem;
                        border-radius: 5px;
                        display: inline-block;
                        margin-top: 1rem;
                    }
                    a:hover { background: rgba(168, 85, 247, 0.4); }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1 class="success">✓ Message Sent Successfully!</h1>
                    <p>Thank you for your message. I'll get back to you soon!</p>
                    <a href="/">← Back to Portfolio</a>
                </div>
            </body>
            </html>
            """
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(response_html.encode('utf-8'))
            
        except Exception as e:
            self.send_error(500, f"Server Error: {str(e)}")

def run_server(port=8000):
    """Run the portfolio server"""
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    with socketserver.TCPServer(("", port), PortfolioHandler) as httpd:
        print(f"🚀 Portfolio server running at http://localhost:{port}")
        print("📁 Serving Flask-style portfolio website")
        print("💜 Purple neon future funk theme activated!")
        print("\nPress Ctrl+C to stop the server")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped")

if __name__ == "__main__":
    run_server()