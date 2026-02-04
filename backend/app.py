from flask import Flask, jsonify
import os, random, time
from prometheus_client import Counter, Histogram, generate_latest

app = Flask(__name__)

REQUEST_COUNT = Counter('app_requests_total', 'Total requests received')
REQUEST_LATENCY = Histogram('app_request_latency_seconds', 'Latency per request')

@app.route('/')
def index():
    start = time.time()
    delay = random.uniform(0.05, 0.3)
    time.sleep(delay)
    REQUEST_COUNT.inc()
    REQUEST_LATENCY.observe(time.time() - start)
    return jsonify({
        'server': os.environ.get('APP_NAME', 'backend'),
        'container': os.environ.get('HOSTNAME'),
        'delay': round(delay, 2)
    })

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
