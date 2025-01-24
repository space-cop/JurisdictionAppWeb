from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Load the JSON data
with open('data/enriched_medcountyjurisd.json') as f:
    addresses = json.load(f)

# Homepage
@app.route('/')
def index():
    return render_template('index.html')

# Search API
@app.route('/search', methods=['POST'])
def search():
    query = request.json.get('query', '').lower().strip()  # Get the query
    seen = set()  # To track unique addresses
    results = []

    for addr in addresses:
        # Create a combined address string for matching
        street = addr.get('street', '').lower()
        city = addr.get('city', '').lower()
        state = addr.get('state', '').lower()
        zip_code = addr.get('zip', '')

        combined_address = f"{street}, {city}, {state} {zip_code}"

        if query in combined_address and combined_address not in seen:  # Check for uniqueness
            seen.add(combined_address)
            results.append({
                "street": addr['street'],
                "city": addr['city'],
                "state": addr['state'],
                "zip": addr['zip'],
                "agency_name": addr['agency_name'],
                "agency_phone": addr['agency_phone'],
                "website": addr.get('website', None)  # Add the website field
            })

    return jsonify(results[:10])  # Return up to 10 unique results

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
