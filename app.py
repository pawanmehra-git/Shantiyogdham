from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Create submissions directory if it doesn't exist
if not os.path.exists('form_submissions'):
    os.makedirs('form_submissions')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    try:
        # Get form data
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['firstName', 'lastName', 'phone', 'email']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'success': False,
                    'message': f'Missing required field: {field}'
                }), 400
        
        # Add timestamp to data
        data['submission_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'form_submissions/submission_{timestamp}.json'
        
        # Save data to file
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        return jsonify({
            'success': True,
            'message': 'Form submitted successfully!'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'An error occurred: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True) 