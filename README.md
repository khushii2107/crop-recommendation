🌾 Crop Recommendation System

A simple and user-friendly Python-based application that recommends the most suitable crop to grow based on temperature, humidity, and soil moisture. It also includes interactive graphs to visualize environmental data trends over time.

 📌 Features

- 🚜 **Crop Prediction** using user input (temperature, humidity, soil moisture)
- 📈 **Graphical Visualization** of:
  - Temperature
  - Humidity
  - Soil Moisture
- 🌗 **Light/Dark Mode** toggle for better UI experience
- 🖼️ Attractive **background image and layout**
- 🧾 Export graphs as **image or PDF**
- 🗂️ Clean, organized layout with **tabbed graphs** (optional)

🛠️ Tech Stack

- **Python**
- **Tkinter** – for GUI
- **Pandas** – for data handling
- **Matplotlib** – for data visualization
- **Pillow** – for image rendering

📂 Project Structure

📁 crop-recommendation/
│
├── background.jpg # Background UI image
├── crop_data_sample.csv # Input dataset
├── croprecomandadation.py # Main Python GUI application
├── temperature_graph.png # Exported graph sample
├── models/
│ └── model.pkl # (Optional) saved model
└── README.md # You are here!

🚀 Getting Started

 1. Clone the repository
git clone https://github.com/khushii2107/crop-recommendation.git
cd crop-recommendation
2. Install dependencies
Make sure you have Python installed, then install:
pip install pandas matplotlib pillow
3. Run the app
python croprecomandadation.py

📝 Notes
Ensure background.jpg is in the same directory as your Python file.
crop_data_sample.csv should contain date, temperature, humidity, soil_moisture, and crop_recommendation columns.

👩‍💻 Author
Khushi Thakur
GitHub:[@khushii2107](https://github.com/khushii2107) 

📄 License
This project is licensed under the MIT License.

✅ How to Add This in Your Repo
1. In VS Code, create a new file: `README.md`
2. Paste the content above.
3. Then push it to GitHub:

git add README.md
git commit -m "Add README file"
git push origin master
