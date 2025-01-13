from flask import Flask, request, render_template, send_from_directory
import os




app = Flask(__name__, static_folder='public')


# Function to load and parse data from data.txt
def load_data():
    data = []
    with open('data.txt', 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                parts = line.split('#')
                if len(parts) == 4:
                    entry = {
                        'specialty': parts[0].strip(),
                        'location': parts[1].strip(),
                        'year': parts[2].strip(),
                        'description': parts[3].strip()
                    }
                    data.append(entry)
    print(data)  # Check the printed output here
    return data

def filter_data(year, location, specialty):
    data = load_data()  # Load data again
    print(f"Filtering Data: Year: {year}, Location: {location}, Specialty: {specialty}")  # Debug output
    
    filtered_items = []
    
    for item in data:
        print(f"Checking Item: {item}")  # Debug each item
        
        # Normalize item fields
        item_year = item['year'].strip() if item['year'] else None
        item_location = item['location'].lower() if item['location'] else None
        item_specialty = item['specialty'].lower() if item['specialty'] else None
        
        # Check if the item matches the filters
        if (not year or item_year == year) and \
           (not location or item_location == location) and \
           (not specialty or specialty in item_specialty):
            filtered_items.append(item)
    
    print(f"Filtered Items: {filtered_items}")  # Debug filtered results
    return filtered_items

@app.route('/')
def home():
    return render_template('website.html')

@app.route('/results')
def results():
    # Get query parameters
    year = request.args.get('year')
    location = request.args.get('location')
    specialty = request.args.get('specialty')

 
    # Normalize query parameters
    location = location.lower() if location else None
    specialty = specialty.replace("_", " ").lower() if specialty else None
    year = year.strip() if year else None
    
    # Filter the data
    filtered_items = filter_data(year, location, specialty)
    
    # Pass filtered data to template
    return render_template('results.html', results=filtered_items)


@app.route('/public/<path:filename>')
def serve_static_files(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
