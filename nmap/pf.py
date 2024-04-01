# from flask import Flask, jsonify
# import nmap
# import socket
# import pyxploitdb

# app = Flask(__name__)

# def get_protocol_name(port):
#     try:
#         protocol_name = socket.getservbyport(int(port))
#     except OSError:
#         protocol_name = "Unknown"
#     return protocol_name

# def resolve_target(target):
#     try:
#         ip_address = socket.gethostbyname(target)
#         return ip_address
#     except socket.gaierror:
#         return None

# def nmap_scan(target):
#     scanner = nmap.PortScanner()
#     scanner.scan(target, arguments='-A -T4 ')
#     return scanner[target]['tcp']



# @app.route('/')

# def scan_results():
#     target = 'scanme.nmap.com'  # Default target
#     resolved_target = resolve_target(target)

#     if resolved_target:
#         results = nmap_scan(resolved_target)
#         scan_results = []

#         for port in results:
#             if results[port]['state'] == 'open':
#                 protocol = results[port]['name']
#                 product = results[port]['product']
#                 version = results[port]['version']
#                 protocol_name = get_protocol_name(port)
#                 exploit_list = []

#                 term = product + version
#                 if term:
#                     exploits = pyxploitdb.searchEDB(term)
#                     for exploit in exploits:
#                         exploit_list.append(exploit.description)

#                 scan_results.append({
#                     "port": port,
#                     "protocol_name": protocol_name,
#                     "product": product,
#                     "version": version,
#                     "exploits": exploit_list
#                 })

#         # Format the scan results into HTML
#         html_content = '<h1>Scan Results</h1>'
#         for result in scan_results:
#             html_content += f'<p>Port {result["port"]}/{result["protocol_name"]} is open, service version: {result["product"]} {result["version"]}</p>'
#             html_content += '<ul>'
#             for exploit in result["exploits"]:
#                 html_content += f'<li>{exploit}</li>'
#             html_content += '</ul>'

#         return html_content 
#     else:
#         return jsonify({"error": "Failed to resolve the target hostname."})

# if __name__ == '_main_':
#     app.run(debug=True)