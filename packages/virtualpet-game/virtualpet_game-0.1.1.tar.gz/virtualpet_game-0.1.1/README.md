# Python Package Exercise - Virtual Pet 🐾
[![log github events](https://github.com/software-students-fall2024/3-python-package-straight-a/actions/workflows/event-logger.yml/badge.svg)](https://github.com/software-students-fall2024/3-python-package-straight-a/actions/workflows/event-logger.yml)

## Description

**Virtual Pet** is a Python package for creating and interacting with a virtual pet, providing a playful and nostalgic experience for developers. The pet has attributes like happiness, cleanness, and sleep status, which can be managed through various actions. Users can feed, play with, and take care of their pet by giving it hugs, kisses, or showers, and can even put it to sleep. The virtual pet responds with different emojis based on its current state, adding a whimsical element to the interactions. The goal of this package is to add a bit of joy to everyday coding routines by incorporating a fun, interactive companion.

## How to Install and Use the VirtualPet Package 

1. **Set Up a Virtual Environment and Install the Package**：
   - Create a pipenv-managed virtual environment and install your package:
   Run the following command to install the virtualpet package from TestPyPI:
   pypi to be updated...
   - Activate the Virtual Environment:
     ```bash
     pipenv shell
     ```

2. **Create a Python Program to Use the Package**:
   - Create a Python file to test the package. To see a full code example using all functions of the virtualpet package, check out the Code example for all functions file.
   [Code example for all functions](use_virtual_pet.py)


3. **Run the Package Directly from the Command Line**;
   - Set up and activate the pipenv virtual environment as before:
     ```bash
     pip install --index-url https://test.pypi.org/simple/ virtualpet-game
     pipenv shell
     ```
   - Run the Package Directly:
     ```bash
     python3 -m virtualpet
     ```
   - Exit the Virtual Environment:
     ```bash 
     exit
     ```


## Steps necessary to run the software(for Development)

1. **Install Python**:
   - Make sure Python 3.8 or higher is installed on your system. You can download it from python.org.

2. **Clone the repository**:
   - Run the following commands to create and activate the virtual environment:
     ```bash
     git clone https://github.com/software-students-fall2024/3-python-package-straight-a.git
     cd your-repository-folder
     ```

3. **Set up a Virtual Environment**:
   - Run the following commands to create and activate the virtual environment:
     ```bash
     python3 -m venv venv
     ```
   - Activate the virtual environment:
     - On Windows:
       ```bash
       .\venv\Scripts\activate
       ```
     - On macOS/Linux:
       ```bash
       source venv/bin/activate
       ```

4. **Install Dependencies:**:
   -  With the virtual environment activated, install the necessary dependencies, including pytest for testing and twine for PyPI uploads (if needed):
   ```bash
   pip install -r requirements.txt
   ```

5. **Build and Test the Package:**:
   - Build the Package:
     Use build to package the project:
       ```bash
       python3 -m build
       ```
   - Install the Package Locally:
     Install the package locally to test its functionality:
         ```bash
         pip install .
         ```
   - Run Tests:
     Use pytest to run the test suite and verify that everything is working correctly:
         ```bash
         pytest
         ```



## Team Members 

- [Elaine Lyu](https://github.com/ElaineR02)
- [Linda Li](https://github.com/Applejam-ovo)
- [Rita He]( https://github.com/ritaziruihe)
- [Hannah Liang](https://github.com/HannahLiang627)