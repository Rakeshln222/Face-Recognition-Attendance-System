
# Face Recognition Attendance System

A system that detects faces via webcam, recognizes students/employees from a stored dataset and automatically marks attendance (name, date, time) in a database or CSV. No manual attendance marking needed.  

## Table of Contents

- [Features](#features)  
- [Technologies Used](#technologies-used)  
- [Getting Started](#getting-started)  
  - [Prerequisites](#prerequisites)  
  - [Installation](#installation)  
  - [Usage](#usage)  
- [Project Structure](#project-structure)  
- [How It Works](#how-it-works)  
- [Supported Storage Options](#supported-storage-options)  
- [Contributing](#contributing)  
- [License](#license)  
- [Contact](#contact)  

## Features

- Real-time face detection using webcam  
- Face recognition against a pre-collected dataset  
- Automatically mark attendance with name, date and time  
- Support for multiple storage/database backends (SQLite, MySQL, CSV)  
- Optionally use different face-recognition algorithms (e.g. LBPH)  

## Technologies Used

- Python  
- OpenCV (for face detection & recognition)  
- MySQL / SQLite / CSV for storing attendance data  
- (Any additional libs you’ve used: e.g. `face_recognition`, `dlib`, etc.)  

## Getting Started

### Prerequisites

Make sure you have:

- Python 3.x installed  
- Webcam or other video input device  
- Required Python packages (see below)  
- Database setup (if using MySQL or SQLite)  

 Installation

1. Clone the repo  
   ```bash
   git clone https://github.com/Rakeshln222/Face-Recognition-Attendance-System.git
   cd Face-Recognition-Attendance-System
````

2. (Recommended) Create and activate a virtual environment

   ```bash
   python3 -m venv env
   source env/bin/activate       # on Linux/macOS
   env\Scripts\activate          # on Windows
   ```

3. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

4. Setup database (if using MySQL or SQLite)

   * For SQLite, ensure a `.db` file or path is configured.
   * For MySQL, configure host, user, password, database in the config file or in code.

### Usage

Here’s a typical workflow:

1. **Capture Dataset**
   Run `capture_dataset.py` to collect face images for each person (student/employee).

   ```bash
   python capture_dataset.py
   ```

2. **Encode Faces**
   Process collected images to encode faces for quicker recognition.

   ```bash
   python encode_faces.py
   ```

3. **Train (LBPH, optional)**
   If using LBPH based algorithm, run the training script.

   ```bash
   python train_lbph.py
   ```

4. **Recognize & Mark Attendance**
   Run the recognition attendance script. This opens webcam, recognizes faces, and marks attendance.

   ```bash
   python recognize_attendance.py
   ```

5. **Alternative / Lightweight version**
   If using LBPH version:

   ```bash
   python recognize_lbph.py
   ```

## Project Structure

Here’s a high-level view of the files in this repo:

| File                      | Purpose                                                           |
| ------------------------- | ----------------------------------------------------------------- |
| `capture_dataset.py`      | Collects face images for individuals to build dataset.            |
| `encode_faces.py`         | Computes face encodings (feature vectors) for recognition.        |
| `train_lbph.py`           | Trains a Local Binary Patterns Histograms (LBPH) face recognizer. |
| `recognize_attendance.py` | Recognise faces using encodings + webcam; mark attendance.        |
| `recognize_lbph.py`       | Recognise faces using LBPH method; alternate workflow.            |
| Database / CSV            | Stores attendance logs: name, time, date.                         |

## How It Works

1. **Data Collection**
   Collect multiple images per person (varied orientations, lighting) via `capture_dataset.py`.

2. **Encoding / Training**

   * If using face encodings (e.g. via `face_recognition` or similar), compute embeddings in `encode_faces.py`.
   * If using LBPH (“Local Binary Patterns Histogram”), then `train_lbph.py` builds the model.

3. **Recognition**
   Webcam feed is processed; faces detected → recognized by comparing against encodings or model.

4. **Attendance Marking**
   When a known face is identified, system logs the user’s name along with current date + time in the selected storage (CSV, SQLite, or MySQL).

5. **Avoiding Duplicates**
   The scripts are designed to avoid marking multiple entries for the same person for the same session (you can set rules: e.g. once per day, or once per launch).

## Supported Storage Options

* **CSV** – Simple, no setup; for small/basic usage
* **SQLite** – Local file-based DB; lightweight
* **MySQL** – For more robust, multi-user or networked use


## Contributing

If you’d like to contribute:

1. Fork the repository
2. Create a new branch for your feature/fix
3. Make your changes, add tests/documentation where needed
4. Submit a pull request

Please adhere to standard code style, and ensure your additions are well documented.

## Contact

For questions or feedback, you can reach out to:

* **Author**: Rakesh L N
* **GitHub**: [https://github.com/Rakeshln222](https://github.com/Rakeshln222)
* **Email**: rakeshln0000@gmail.com
