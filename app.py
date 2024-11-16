from flask import Flask, request, jsonify
from flask_cors import CORS
from service.MetroNetworkService import MetroNetworkService  # Import your service class

app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes
CORS(app, resources={r"/api/*": {"origins": "*"}}) 

# Initialize the service with a default choice
metro_network_service = MetroNetworkService(1)

@app.route('/api/findRoute', methods=['GET'])
def find_route():
    try:
        # Get parameters from the request
        start_stop_id = request.args.get('startStopId')
        end_stop_id = request.args.get('endStopId')
        choice = int(request.args.get('choice'))

        # Reinitialize the service with the new choice
        global metro_network_service
        metro_network_service = MetroNetworkService(choice)

        # Call the service method to find the shortest path
        route = metro_network_service.findShortestPath(start_stop_id, end_stop_id, choice)

        return jsonify(route)
    except Exception as e:
        # Handle exceptions
        return jsonify({'error': f"Error initializing the Metro Network Service: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
