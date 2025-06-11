# PyFCS Dental Shades

## Description

This repository contains the execution framework for the **Expert Validation Interface** and **PyFCS Dental GUI** software, including everything needed to install and use it.

All the code in this project builds upon the core components of the [**PyFCS**](https://github.com/RafaelConejo/PyFCS) ecosystem, developed by the same author. The PyFCS repository also includes documentation on the fuzzy reasoning engine and the graphical user interface.

The validation software allows clinical and expert users to evaluate dental shade classifications based on fuzzy conceptual models. It integrates seamlessly with the fuzzy color space constructed via the PyFCS GUI and supports reproducible evaluation workflows aligned with perceptual reasoning.

For an overview of how the repositories are organized and how each component contributes to the system, see the section [Repository Structure and Component Distribution](#repository-structure-and-component-distribution).

---

## Repository Structure and Component Distribution

The complete system for expert validation and visualization of the fuzzy color space in dentistry is distributed across two main repositories:

### 🔹 Expert_Validation_Interface

This repository contains all components required to run the **expert validation module**, which is fully integrated into the **PyFCS** ecosystem. Key features include:

- Implemented in **Python** using the **Tkinter** framework.
- Supports reproducible evaluation workflows.
- Seamless integration with the fuzzy reasoning core.
- Full documentation and usage instructions available in the main repository: [`PyFCS_DentalShades`](https://github.com/RafaelConejo/PyFCS_DentalShades).

### 🔹 PyFCS_Dental_GUI

This repository hosts the graphical interface for **interactive creation and visualization** of the fuzzy color space. Key functionalities include:

1. **Construction of the fuzzy color model**: allows users to input CIE-L\*a\*b\* coordinates for each shade prototype, define positive and negative reference categories, and generate the corresponding fuzzy color volumes. This process includes:
   - Voronoi-based tessellation.
   - Scaling to define *core*, *α-cut* (e.g., 0.5 level), and *support* regions.
   - An additional prototype representing the black background commonly used in dental photography to reduce misclassification.

   The resulting fuzzy color space includes 17 fuzzy colors (16 shades from the VITA Classical Shade Guide plus the black background).

2. **Interactive 3D visualization**: offers an intuitive environment to explore and analyze the constructed fuzzy color space, featuring:
   - Menus for loading images, selecting shades, and managing model components.
   - Panels displaying the geometric volumes of each fuzzy region (*core*, *α-cut*, *support*).
   - Interactive controls for zooming, panning, and rotating to inspect spatial relationships and distribution patterns.

These enhanced visualization tools support both verification and interpretation of the fuzzy color model, bridging technical modeling and perceptual reasoning in clinical dental shade matching.

The full source code is available at: [`PyFCS_DentalShades`](https://github.com/RafaelConejo/PyFCS_DentalShades).


---

## Expert_Validation_Interface
### 🔧 Installation

1. Download the repository:
   - Either via the **"Clone or Download"** button on GitHub, or
   - From the **Releases** section as a `.zip` file.

2. Extract the contents to a local directory.

3. Open a terminal and navigate to the root folder of the project.

4. Create and activate a virtual environment:

   - **On Windows (not mandatory):**
     ```bash
     python -m venv venv_expert
     venv_expert\Scripts\activate
     ```

   - **On Linux/macOS:**
     ```bash
     python3 -m venv venv_expert
     source venv_expert/bin/activate
     ```

5. Install the required dependencies:

   - **On Windows:**
     ```bash
     python -m pip install -r Expert_Validation_Interface\Datasets\requirements.txt
     ```

   - **On Linux/macOS:**
     ```bash
     python3 -m pip install -r Expert_Validation_Interface/Datasets/requirements.txt
     ```

6. Run the **Tooth Color Validation** interface:

   - **On Windows:**
     ```bash
     python Expert_Validation_Interface\VITA_validation_software.py
     ```

   - **On Linux/macOS:**
     ```bash
     python3 Expert_Validation_Interface/VITA_validation_software.py
     ```




### Results and Evaluation
- The **Results/** directory stores expert-generated classification data created through the GUI.
- The **Results_evaluation/** folder includes Jupyter Notebooks that analyze and compare expert classifications with the predictions produced by the PyFCS fuzzy model.

---

## PyFCS_Dental_GUI
### 🔧 How to Use

If no modifications to the source code are needed, follow these steps for a quick installation:

#### 📦 1. Download the Project

Access the project repository on GitHub and download the library using the **"Clone or Download"** button, or from the **Releases** section by downloading the `.zip` file.

Extract the contents of the `.zip` file to a preferred local folder.

#### 🐍 2. Make Sure Python is Installed

Ensure you have **Python 3.9 or higher** installed, along with **pip**. You can also use a virtual environment manager like [Anaconda](https://www.anaconda.com/).

If `pip` is not available, you can install it manually with:

  ```bash
  python -m ensurepip --upgrade
  ```

#### </> 3. Open a terminal, navigate to the root directory of the project, and install the required dependencies:

  - **🪟 Windows**
    ```bash
    pip install -r PyFCS\external\requirements.txt

    # Once the dependencies are installed, launch the main interface structure by executing:
    python PyFCS\visualization\basic_structure.py
    ```

  - **🐧 Linux**
    ```bash
    python3 -m venv venv_pyfcs
    source venv_pyfcs/bin/activate
    python3 -m pip install -r PyFCS/external/requirements.txt

    # Install system dependencies (required manually)
    sudo apt install python3.12-tk
    python3 -m pip install PyQtWebEngine

    # Launch the interface
    python3 PyFCS/visualization/basic_structure.py
    ```

    These steps ensure full compatibility with features such as Tkinter-based dialogs and enhanced Qt-based rendering on Linux systems.

  - **🍎 macOS**
    ```bash
    python3 -m venv venv_pyfcs
    source venv_pyfcs/bin/activate
    python3 -m pip install -r PyFCS/external/requirements.txt

    # (If needed) Install Tkinter via Homebrew
    brew install python-tk

    # Launch the interface
    python3 PyFCS/visualization/basic_structure.py
    ```

---

## 📖 Interface Manual

A complete manual explaining the use of the GUI, including examples and step-by-step guides, is available in the following folder of the repository:  
🔗 [PyFCS_GUI_Manual](https://github.com/RafaelConejo/PyFCS_GUI/tree/main/PyFCS_GUI_Manual)

---

## 📬 Contact & Support
For support or questions, feel free to contact: rafaconejo@ugr.es
