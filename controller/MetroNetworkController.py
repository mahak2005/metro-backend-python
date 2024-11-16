# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from service import MetroNetworkService  # Import your service

# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes

# # Initialize the service with a default choice (if needed globally)
# metro_network_service = MetroNetworkService(1)

# @app.route('/api/findRoute', methods=['GET'])
# def find_route():
#     try:
#         # Get parameters from the request
#         start_stop_id = request.args.get('startStopId')
#         end_stop_id = request.args.get('endStopId')
#         choice = request.args.get('choice')

#         # Validate required parameters
#         if not start_stop_id or not end_stop_id or not choice:
#             return jsonify({'error': 'Missing required parameters: startStopId, endStopId, and choice are required.'}), 400

#         # Convert 'choice' to an integer
#         try:
#             choice = int(choice)
#         except ValueError:
#             return jsonify({'error': 'Choice must be an integer.'}), 400

#         # Reinitialize the service with the new choice
#         global metro_network_service
#         metro_network_service = MetroNetworkService(choice)

#         # Call the service method to find the shortest path
#         route = metro_network_service.find_shortest_path(start_stop_id, end_stop_id, choice)

#         return jsonify(route)
#     except Exception as e:
#         # Handle exceptions
#         return jsonify({'error': f"Error initializing the Metro Network Service: {str(e)}"}), 500


# if __name__ == '__main__':
#     app.run(debug=True)
