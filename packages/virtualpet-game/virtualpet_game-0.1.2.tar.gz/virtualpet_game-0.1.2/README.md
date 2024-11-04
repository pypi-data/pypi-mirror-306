# Python Package Exercise - Virtual Pet 🐾
[![log github events](https://github.com/software-students-fall2024/3-python-package-straight-a/actions/workflows/event-logger.yml/badge.svg)](https://github.com/software-students-fall2024/3-python-package-straight-a/actions/workflows/event-logger.yml)     

[![Link to PyPI](https://pypi.org/project/virtualpet-game/)](https://pypi.org/project/virtualpet-game/)

## Description

**Virtual Pet** is a Python package for creating and interacting with a virtual pet, providing a playful and nostalgic experience for developers. The pet has attributes like happiness, cleanness, and sleep status, which can be managed through various actions. Users can feed, play with, and take care of their pet by giving it hugs, kisses, or showers, and can even put it to sleep. The virtual pet responds with different emojis based on its current state, adding a whimsical element to the interactions. The goal of this package is to add a bit of joy to everyday coding routines by incorporating a fun, interactive companion.

## How to Install and Use the VirtualPet Package 

1. **Set Up a Virtual Environment and Install the Package**：
   - Create a pipenv-managed virtual environment and install your package:
   Run the following command to install the virtualpet package from TestPyPI:
    ```bash
     pipenv install virtualpet-game
     ```
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
     pipenv install virtualpet-game
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

## Available Functions

`feed_pet()`: Feed your pet to increase its happiness and reduce its cleanness.
```bash
pet.feed_pet()
```
`play_with_pet(action: Literal['hug', 'pet', 'kiss'])`: Play with your pet to make it happier. You can use the actions:`hug`, `pet`, or `kiss`
```bash
pet.play_with_pet('hug')
pet.play_with_pet('pet')
pet.play_with_pet('kiss')
```
`take_shower()`: Give your pet a shower to reset its cleanness level.
```bash
pet.take_shower()
```
`pet_sleep()`: Put your pet to sleep for a random amount of time (between 20 to 25 seconds in the current version).
```bash
pet.pet_sleep()
```
`restart()`: Restart your pet to default levels for both happiness and cleanness.
```bash
pet.restart()
```
`exit()`: Exit and say goodbye to your pet. This will end the program.
```bash
pet.exit()
```
`_display_status()`: Display your pet's current happiness, cleanness, and state with a cute emoji representation. 

**Note**: `_display_status()` is used internally, but you can call it directly to check the current status.
```bash
pet._display_status()
```
You can see how to use all of the functions in an example Python program: [Example Python Program](use_virtual_pet.py)

**Example of Use**
- Here is a snippet from the `use_virtual_pet.py` file:
  ```bash
  from virtualpet.pet import VirtualPet

  def main():
      pet_name = input("What would you like to name your pet? ")
      pet = VirtualPet(pet_name)

      while pet.active:
          action = input("(Options: feed/play/take shower/check status/sleep/restart/exit): ").strip().lower()
          if action == "feed":
              pet.feed_pet()
          elif action == "play":
              sub_action = input("Choose how to play with your pet (hug/pet/kiss): ").strip().lower()
              pet.play_with_pet(sub_action)
          elif action == "take shower":
              pet.take_shower()
          elif action == "check status":
              pet._display_status()
          elif action == "sleep":
              pet.pet_sleep()
          elif action == "restart":
              pet.restart()
          elif action == "exit":
              pet.exit()
          else:
              print("Invalid action. Please choose a valid action.")

  if __name__ == "__main__":
      main()
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