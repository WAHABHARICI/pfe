from flask import Flask, request, render_template, jsonify
import nmap
import socket
import pyxploitdb

app = Flask(__name__)

# Print a message when the server starts running
print("Server is running. Ready to scan.")

def get_protocol_name(port):
    try:
        protocol_name = socket.getservbyport(int(port))
    except OSError:
        protocol_name = "Unknown"
    return protocol_name

def nmap_scan(target):
    try:
        scanner = nmap.PortScanner()
        scanner.scan(target, arguments='-sV -T4')
        return scanner[target]['tcp']
    except Exception as e:
        print(f"An error occurred during the Nmap scan: {e}")
        return None

def search_exploits(term):
    try:
        exploits = pyxploitdb.searchEDB(term)
        if exploits:
            return [exploit.description for exploit in exploits]
        else:
            return ["No exploit found"]
    except Exception as e:
        print(f"An error occurred during exploit search: {e}")
        return []

@app.route('/')
def index():
    return render_template('index.html', results=None)

@app.route('/pfe2', methods=['POST'])
def scan_results():
    target = request.form.get('target')
    if target:
        results = nmap_scan(target)
        if results:
            scan_results = []
            for port in results:
                if results[port]['state'] == 'open':
                    protocol_name = get_protocol_name(port)
                    product = results[port]['product']
                    version = results[port]['version']
                    term = product + version
                    exploit_list = search_exploits(term)
                    scan_results.append({
                        "port": port,
                        "protocol_name": protocol_name,
                        "product": product,
                        "version": version,
                        "exploits": exploit_list
                    })

            # Print scan results in the terminal
            for result in scan_results:
                print(f"Port {result['port']}/{result['protocol_name']} is open, service version: {result['product']} {result['version']}")
                for exploit in result['exploits']:
                    print(f"   - {exploit}")

            return render_template('index.html', results=scan_results)
        else:
            return jsonify({"error": "No open ports found."})
    else:
        return jsonify({"error": "No target provided."})

if __name__ == '__main__':
    app.run(debug=True)
