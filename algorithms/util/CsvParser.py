import csv
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.MetroRoute import MetroRoute
from model.MetroShape import MetroShape
from model.MetroStop import MetroStop
from model.MetroStopTime import MetroStopTime
from model.MetroTrip import MetroTrip
from io import StringIO

class CsvParser:

    # Method to parse Routes CSV
    @staticmethod
    def parse_routes(reader):
        routes = {}
        csv_reader = reader  # Already a csv.reader object
        next(csv_reader)  # Skip the header line
        for line in csv_reader:
            if len(line) < 4:
                print(f"Warning: Skipping line with insufficient columns: {','.join(line)}")
                continue
            route_id, route_short_name, route_long_name, route_color = line
            route = MetroRoute(route_id, route_short_name, route_long_name, route_color)
            routes[route_id] = route
        return routes

    # Method to parse Stops CSV
    @staticmethod
    def parse_stops(reader):
        stops = {}
        csv_reader = reader
        next(csv_reader)  # Skip the header line
        for line in csv_reader:
            if len(line) < 4:
                print(f"Warning: Skipping line with insufficient columns: {','.join(line)}")
                continue
            stop_id, stop_name, stop_lat, stop_lon = line
            stop_lat = float(stop_lat)
            stop_lon = float(stop_lon)
            stop = MetroStop(stop_id, stop_name, stop_lat, stop_lon)
            stops[stop_id] = stop
        return stops

    # Method to parse Trips CSV
    @staticmethod
    def parse_trips(reader):
        trips = {}
        csv_reader = reader
        next(csv_reader)  # Skip the header line
        for line in csv_reader:
            if len(line) < 4:
                print(f"Warning: Skipping line with insufficient columns: {','.join(line)}")
                continue
            route_id, service_id, trip_id, shape_id = line
            trip = MetroTrip(route_id, service_id, trip_id, shape_id)
            trips[trip_id] = trip
        return trips

    # Method to parse Stop Times CSV
    @staticmethod
    def parse_stop_times(reader):
        stop_times = {}
        csv_reader = reader
        next(csv_reader)  # Skip the header line
        for line in csv_reader:
            if len(line) < 6:
                print(f"Warning: Skipping line with insufficient columns: {','.join(line)}")
                continue
            trip_id, arrival_time, departure_time, stop_id, stop_sequence, shape_dist_traveled = line
            stop_sequence = int(stop_sequence)
            shape_dist_traveled = float(shape_dist_traveled)
            stop_time = MetroStopTime(trip_id, arrival_time, departure_time, stop_id, stop_sequence, shape_dist_traveled)
            stop_times[f"{trip_id}_{stop_sequence}"] = stop_time
        return stop_times

    # Method to parse Shapes CSV
    @staticmethod
    def parse_shapes(reader):
        shapes = {}
        csv_reader = reader
        next(csv_reader)  # Skip the header line
        for line in csv_reader:
            if len(line) < 5:
                print(f"Warning: Skipping line with insufficient columns: {','.join(line)}")
                continue
            shape_id, shape_pt_lat, shape_pt_lon, shape_pt_sequence, shape_dist_traveled = line
            shape_pt_lat = float(shape_pt_lat)
            shape_pt_lon = float(shape_pt_lon)
            shape_pt_sequence = int(shape_pt_sequence)
            shape_dist_traveled = float(shape_dist_traveled)
            shape = MetroShape(shape_id, shape_pt_lat, shape_pt_lon, shape_pt_sequence, shape_dist_traveled)
            shapes[f"{shape_id}_{shape_pt_sequence}"] = shape
        return shapes


# Main function to test the parsing
# def main():
#     # For testing, we will use StringIO to simulate reading from CSV files
#     route_csv = """route_id,route_short_name,route_long_name,route_color
#     1,Red Line,Red Line,FF0000
#     2,Blue Line,Blue Line,0000FF"""
    
#     stop_csv = """stop_id,stop_name,stop_lat,stop_lon
#     101,Central Station,40.712776,-74.005974
#     102,Park Avenue,40.730610,-73.935242"""
    
#     trip_csv = """route_id,service_id,trip_id,shape_id
#     1,weekday,101,shape1
#     2,weekday,102,shape2"""
    
#     stop_time_csv = """trip_id,arrival_time,departure_time,stop_id,stop_sequence,shape_dist_traveled
#     101,08:00:00,08:05:00,101,1,0.0
#     102,08:10:00,08:15:00,102,2,1.0"""
    
#     shape_csv = """shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence,shape_dist_traveled
#     shape1,40.712776,-74.005974,1,0.0
#     shape1,40.730610,-73.935242,2,1.0"""
    
#     # Simulating reading from a file
#     route_reader = StringIO(route_csv)
#     stop_reader = StringIO(stop_csv)
#     trip_reader = StringIO(trip_csv)
#     stop_time_reader = StringIO(stop_time_csv)
#     shape_reader = StringIO(shape_csv)
    
#     # Parse data
#     routes = CsvParser.parse_routes(route_reader)
#     stops = CsvParser.parse_stops(stop_reader)
#     trips = CsvParser.parse_trips(trip_reader)
#     stop_times = CsvParser.parse_stop_times(stop_time_reader)
#     shapes = CsvParser.parse_shapes(shape_reader)
    
#     # Output the results to verify correctness
#     print("Parsed Routes:")
#     for route in routes.values():
#         print(vars(route))
    
#     print("\nParsed Stops:")
#     for stop in stops.values():
#         print(vars(stop))
    
#     print("\nParsed Trips:")
#     for trip in trips.values():
#         print(vars(trip))
    
#     print("\nParsed Stop Times:")
#     for stop_time in stop_times.values():
#         print(vars(stop_time))
    
#     print("\nParsed Shapes:")
#     for shape in shapes.values():
#         print(vars(shape))

# if __name__ == "__main__":
#     main()
