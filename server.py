#!/usr/bin/env python3
"""
Love Over Coffee (LOC) Jaipur - Full-Stack Local Server
Serves static frontend assets and provides backend API endpoints for:
- Placing orders (dispatch to Zomato, Swiggy, WhatsApp, or Direct)
- Saving order history to orders.json
- Healthcheck & menu lookup
"""

import http.server
import socketserver
import json
import os
import urllib.parse
from datetime import datetime

PORT = 4321
DIRECTORY = os.path.dirname(os.path.abspath(__file__))
ORDERS_FILE = os.path.join(DIRECTORY, 'orders.json')

# Zomato & Swiggy Jaipur Outlet URL mappings
PLATFORM_URLS = {
    'zomato_c_scheme': 'https://www.zomato.com/jaipur/love-over-coffee-1-c-scheme/order',
    'zomato_b2_bypass': 'https://link.zomato.com/xqzv/rshare?id=5673658930563eba',
    'swiggy_c_scheme': 'https://www.swiggy.com/city/jaipur/love-over-coffee-c-scheme-rest382901',
    'swiggy_b2_bypass': 'https://www.swiggy.com/city/jaipur/love-over-coffee-tonk-road-rest382902',
    'whatsapp_c_scheme': '917976198506',
    'whatsapp_b2_bypass': '919928783999'
}

class LOCHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path)

        if parsed_path.path == '/api/order':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            try:
                order_data = json.loads(post_data.decode('utf-8'))
            except Exception as e:
                self.send_error(400, f"Invalid JSON payload: {str(e)}")
                return

            # Enrich order metadata
            order_id = f"LOC-{int(datetime.now().timestamp())}"
            order_record = {
                "order_id": order_id,
                "timestamp": datetime.now().isoformat(),
                "customer": {
                    "name": order_data.get("name", "Guest"),
                    "phone": order_data.get("phone", ""),
                    "address": order_data.get("address", "")
                },
                "outlet": order_data.get("outlet", "c_scheme"),
                "platform": order_data.get("platform", "whatsapp"),
                "items": order_data.get("items", []),
                "subtotal": order_data.get("subtotal", 0),
                "instructions": order_data.get("instructions", "")
            }

            # Save order to orders.json
            try:
                orders = []
                if os.path.exists(ORDERS_FILE):
                    with open(ORDERS_FILE, 'r') as f:
                        orders = json.load(f)
                orders.append(order_record)
                with open(ORDERS_FILE, 'w') as f:
                    json.dump(orders, f, indent=2)
            except Exception as e:
                print(f"[Warning] Error saving order to file: {e}")

            # Prepare platform redirect / message payload
            platform = order_record["platform"]
            outlet = order_record["outlet"]

            # Construct formatted message for WhatsApp / direct delivery
            items_summary = "\n".join([f"• {i.get('qty', 1)}x {i.get('title')} (₹{i.get('price')})" for i in order_record["items"]])
            wa_text = (
                f"☕ *New Order #{order_id} - Love Over Coffee ({outlet.replace('_', ' ').title()})*\n\n"
                f"*Items Ordered:*\n{items_summary}\n\n"
                f"*Total Amount:* ₹{order_record['subtotal']:.2f}\n"
                f"*Customer:* {order_record['customer']['name']} ({order_record['customer']['phone']})\n"
                f"*Address / Notes:* {order_record['customer']['address'] or 'Dine-in / Direct Pickup'}"
            )
            encoded_wa = urllib.parse.quote(wa_text)

            phone_number = PLATFORM_URLS.get(f"whatsapp_{outlet}", "917976198506")
            whatsapp_link = f"https://wa.me/{phone_number}?text={encoded_wa}"

            # Platform redirection URL
            redirect_url = whatsapp_link
            if platform == 'zomato':
                redirect_url = PLATFORM_URLS.get(f"zomato_{outlet}", PLATFORM_URLS['zomato_c_scheme'])
            elif platform == 'swiggy':
                redirect_url = PLATFORM_URLS.get(f"swiggy_{outlet}", PLATFORM_URLS['swiggy_c_scheme'])

            response_payload = {
                "success": True,
                "order_id": order_id,
                "platform": platform,
                "outlet": outlet,
                "whatsapp_link": whatsapp_link,
                "redirect_url": redirect_url,
                "order_summary": wa_text
            }

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response_payload).encode('utf-8'))
            return

        elif parsed_path.path == '/api/orders':
            # Retrieve all orders
            orders = []
            if os.path.exists(ORDERS_FILE):
                with open(ORDERS_FILE, 'r') as f:
                    orders = json.load(f)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(orders).encode('utf-8'))
            return

        self.send_error(404, "Endpoint not found")

class ReusableTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True

if __name__ == '__main__':
    with ReusableTCPServer(("", PORT), LOCHandler) as httpd:
        print(f"☕ Love Over Coffee Backend & Static Server running at http://localhost:{PORT}")
        httpd.serve_forever()
