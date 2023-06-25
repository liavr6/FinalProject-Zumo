import threading
import csv
import time
import Driver

class Plotter:
    def __init__(self, file_path):
        self.file_path = file_path
        self.running = True
        self.lock = threading.Lock()
        self.measurements = []

    def plot(self):
        start_time = time.time()
        while self.running:
            # Calculate the time elapsed
            elapsed_time = time.time() - start_time

            # Save the measurements
            self.lock.acquire()
            self.measurements.append([elapsed_time, Driver.status, Driver.fwd_dist, Driver.right_dist, Driver.right_ang])
            self.lock.release()

            # Sleep for a desired interval
            time.sleep(0.01)  # Adjust the interval as needed

    def stop(self):
        self.running = False

    def save_measurements_to_csv(self):
        with open(self.file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Time', 'Status', 'Forward Distance', 'Right Distance', 'Right Angle'])
            writer.writerows(self.measurements)

# Example usage
# if __name__ == '__main__':
#     file_path = 'measurements.csv'

#     # Create an instance of Plotter
#     plotter = Plotter(file_path)

#     # Create and start the plotter thread
#     plotter_thread = threading.Thread(target=plotter.plot, args=('OK', 1.5, 2.3, 90))
#     plotter_thread.start()

#     # Let the measurements run for a while (10 seconds in this example)
#     time.sleep(10)

#     # Stop the plotter thread
#     plotter.stop()
#     plotter_thread.join()

#     # Save the measurements to a CSV file
#     plotter.save_measurements_to_csv()
