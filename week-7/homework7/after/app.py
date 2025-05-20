from flask import Flask, request, jsonify
import os
import subprocess
import ipaddress
import ast
app = Flask(__name__)

# Get password from environment variable 
PASSWORD = os.environ.get('APP_PASSWORD')

@app.route('/')
def hello():
    name = request.args.get('name', 'World')
    if not name.isalnum():
        return jsonify({"error": "Invalid name"}), 400
    return f"Hello, {name}!"

# Hardened Command injection vulnerability
@app.route('/ping')
def ping():
    ip = request.args.get('ip')
    if not ip: 
        return jsonify({"error": "IP address not provided"}), 400
    try:
        ipaddress.ip_address(ip)
        result = subprocess.check_output(["ping","-c", "1", ip])
        return result
    except ValueError:
        return jsonify({"error": "Invalid ip address format"}), 400
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Ping Command Timed Out"}), 504
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Ping Command Failed", "details": e.output.decode('utf-8')}), 500
   

# Secured use of eval
@app.route('/calculate')
def calculate():
    expression = request.args.get('expr')
    try:
        result= ast.literal_eval(expression)
        return str(result)
    except (SyntaxError, ValueError, TypeError) as e:
        return jsonify({"error": "Invalid or Unsafe Expression", "details": e.output.decode('utf-8')}), 400    

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
