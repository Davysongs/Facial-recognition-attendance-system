# Facial Recognition Attendance System

This project is a facial recognition attendance system that uses an ESP32-CAM module to capture images and a Python script to process the images, recognize faces, and log attendance in a CSV file.

## Components

- ESP32-CAM
- FTDI Programmer (USB to Serial Adapter)
- Python 3.x
- Libraries: `pandas`, `opencv-python`, `numpy`, `face_recognition`, `urllib3`

## Setup Instructions

### Hardware Setup

1. **ESP32-CAM Module:**
    - Connect the ESP32-CAM to the FTDI Programmer as follows:
        - `U0T` to `TX`
        - `U0R` to `RX`
        - `GND` to `GND`
        - `5V` to `VCC`
        - `IO0` to `GND` (only during uploading the code)
    - Connect the FTDI Programmer to your computer via USB.

### Software Setup

1. **Arduino Script:**
    - Install the [Arduino IDE](https://www.arduino.cc/en/software).
    - In the Arduino IDE, install the `ESP32` board support:
        - Go to `File` > `Preferences`.
        - Add the following URL to the `Additional Board Manager URLs`: `https://dl.espressif.com/dl/package_esp32_index.json`
        - Open the `Boards Manager` from `Tools` > `Board` > `Boards Manager`.
        - Search for `ESP32` and install the `esp32` by Espressif Systems.
    - Load the `ESP32_CAM_WebServer.ino` sketch from the `arduino` folder of this repository.
    - Update the WiFi SSID and password in the script.
    - Select `AI Thinker ESP32-CAM` from `Tools` > `Board`.
    - Upload the sketch to the ESP32-CAM.

2. **Python Script:**
    - Clone this repository to your local machine.
    - Install the required Python libraries:
      ```bash
      pip install pandas opencv-python numpy face_recognition urllib3
      ```
    - Place your training images in the `image_folder` directory.
    - Run the Python script `main.py`:
      ```bash
      python main.py
      ```

## Project Structure

```plaintext
.
├── arduino
│   └── ESP32_CAM_WebServer.ino
├── image_folder
│   └── (place your training images here)
├── attendance
│   └── (attendance CSV files will be saved here)
├── main.py
└── README.md
```
## Usage

1. **Start the ESP32-CAM Web Server:**
    - Power on the ESP32-CAM module.
    - Connect to the serial monitor of the Arduino IDE to find the IP address.
    - Access the camera feed using the URL displayed in the serial monitor.

2. **Run the Python Script:**
    - Ensure the ESP32-CAM is connected to the same network as your computer.
    - Run `main.py` script to start capturing images from the ESP32-CAM and marking attendance.


### Notes:
1. **Folder Structure**: Ensure that the folder structure matches the one described in the `Project Structure` section.
2. **WiFi Configuration**: Update the WiFi SSID and password in the Arduino script to match your network.
3. **IP Address**: Update the `url` variable in the Python script with the actual IP address of your ESP32-CAM module.
