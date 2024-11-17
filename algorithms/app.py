from flask import Flask, request, jsonify
from flask_cors import CORS
from service.MetroNetworkService import MetroNetworkService  # Import your service class

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Initialize the service
metro_network_service = None

@app.before_first_request
def initialize_service():
    global metro_network_service
    metro_network_service = MetroNetworkService(2)

@app.route('/api/findRoute', methods=['GET'])
def find_route():
    try:
        # Validate query parameters
        start_stop_id = request.args.get('startStopId')
        end_stop_id = request.args.get('endStopId')
        choice = request.args.get('choice')

        if not all([start_stop_id, end_stop_id, choice]):
            return jsonify({"error": "Missing required parameters: startStopId, endStopId, or choice"}), 400

        # Convert choice to integer
        try:
            choice = int(choice)
        except ValueError:
            return jsonify({"error": "Invalid choice parameter. It must be an integer."}), 400

        # Reinitialize the service with the given choice
        global metro_network_service
        metro_network_service = MetroNetworkService(choice)

        # Call the service method to find the shortest path
        route = metro_network_service.findShortestPath(start_stop_id, end_stop_id, choice)

        return jsonify(route)
    except Exception as e:
        # Log and handle exceptions
        r        # Handle exceptions
        return jsonify({'error': f"Error initializing the Metro Network Service: {str(e)}"}), 500
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
