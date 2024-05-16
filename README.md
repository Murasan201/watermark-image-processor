
# Watermark Image Processor

## Overview
This repository contains a Streamlit application that allows users to automatically add watermarks to images within a ZIP file uploaded by the user, and then download the images as a ZIP file. It is especially useful for batch processing a large number of images.

## Main Features
- Adds watermarks to images within a ZIP file.
- Compresses the watermarked images into a ZIP file for download.
- Allows customization of watermark text, position, and font size through the browser interface.
- Supports image files with both lowercase and uppercase file extensions.

## Requirements
- Python 3.x
- Streamlit library
- Pillow library

## Setup
Follow these steps to install the required libraries:

```bash
pip install streamlit pillow
```

## Usage
1. Navigate to the directory where the script is located.
2. Run the following command:

```bash
streamlit run streamlit_watermark_app.py
```

3. Your browser will open automatically, displaying the application's interface. Follow the instructions to upload a ZIP file, customize the watermark settings, and download the images with the watermark applied.

## License
This project is licensed under the [MIT License](LICENSE). See the `LICENSE` file for details.

## Author
Murasan201  
[https://murasan-net.com/](https://murasan-net.com/)

## Acknowledgements
Thanks to everyone who contributed to this project.
