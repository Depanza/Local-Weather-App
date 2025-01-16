import requests

try:
    import tkinter as tk
    from tkinter import filedialog, messagebox
except ImportError:
    raise ImportError("The 'tkinter' module is required to run this application. Please ensure it is installed and available in your Python environment.")

def get_weather(city, api_key):
    # Function to fetch weather data from OpenWeatherMap API
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,          # City name
        'appid': api_key,   # API key for authentication
        'units': 'metric'   # Use 'metric' for Celsius, 'imperial' for Fahrenheit
    }
    try:
        # Send GET request to the API
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()       # Parse the JSON response

        # Extract relevant weather information
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']

        # Return formatted weather information
        return f"Weather in {city}:\n" \
               f"Description: {weather_description.capitalize()}\n" \
               f"Temperature: {temperature}°C\n" \
               f"Humidity: {humidity}%\n" \
               f"Wind Speed: {wind_speed} m/s"

    except requests.exceptions.HTTPError as http_err:
        # Handle HTTP errors
        return f"HTTP error occurred: {http_err}"
    except requests.exceptions.RequestException as err:
        # Handle general request errors
        return f"Error: {err}"
    except KeyError:
        # Handle missing data in the API response
        return "Invalid response received from the weather API."

def read_api_key(file_path):
    # Function to read the API key from a text file
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()  # Remove any extra whitespace or newlines
    except FileNotFoundError:
        # Handle case where file is not found
        return None
    except Exception as e:
        # Handle other file read errors
        return None

def browse_file():
    # Function to open a file dialog for selecting the API key file
    file_path = filedialog.askopenfilename(title="Select API Key File", filetypes=[("Text Files", "*.txt")])
    if file_path:
        # Insert the selected file path into the entry widget
        api_key_entry.delete(0, tk.END)
        api_key_entry.insert(0, file_path)

def show_weather():
    # Function to display weather information in the GUI
    city = city_entry.get()  # Get the city name from the entry widget
    api_key_path_or_key = api_key_entry.get()  # Get the API key file path or API key text
    
    if not city:
        # Show error if the city name is empty
        messagebox.showerror("Error", "City name cannot be empty.")
        return

    if api_key_path_or_key.endswith(".txt"):
        # If the input is a file path, read the API key from the file
        api_key = read_api_key(api_key_path_or_key)
    else:
        # Otherwise, assume the input is the API key itself
        api_key = api_key_path_or_key.strip()

    if not api_key:
        # Show error if the API key is invalid or missing
        messagebox.showerror("Error", "Invalid or missing API key.")
        return

    # Fetch and display the weather information
    weather_info = get_weather(city, api_key)
    weather_text.delete(1.0, tk.END)  # Clear the text box
    weather_text.insert(tk.END, weather_info)  # Insert the weather information

# GUI Setup
root = tk.Tk()  # Create the main application window
root.title("Local Weather App")  # Set the window title

# Create a frame to organize widgets
frame = tk.Frame(root, padx=10, pady=10)
frame.pack(pady=20)

# Create and place the city label and entry widget
city_label = tk.Label(frame, text="City:")
city_label.grid(row=0, column=0, sticky="w")

city_entry = tk.Entry(frame, width=30)
city_entry.grid(row=0, column=1, pady=5)

# Create and place the API key label and entry widget
api_key_label = tk.Label(frame, text="API Key/File:")
api_key_label.grid(row=1, column=0, sticky="w")

api_key_entry = tk.Entry(frame, width=30)
api_key_entry.grid(row=1, column=1, pady=5)

# Create and place the browse button
browse_button = tk.Button(frame, text="Browse", command=browse_file)
browse_button.grid(row=1, column=2, padx=5)

# Create and place the Get Weather button
get_weather_button = tk.Button(frame, text="Get Weather", command=show_weather)
get_weather_button.grid(row=2, column=0, columnspan=3, pady=10)

# Create and place the text widget for displaying weather information
weather_text = tk.Text(root, width=50, height=10, wrap="word")
weather_text.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
