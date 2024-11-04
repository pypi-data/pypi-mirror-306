# Python Package Exercise: PetPy

## Description
This Python package, PetPy, is an exciting and interactive Python package that brings your very own virtual pets to life! Imagine caring for a unique pet, whether it’s a playful dog, a magical unicorn, or even a fierce T-Rex! With Petpy, you’re in control – create your pet, feed it fun foods, train it to level up, and watch its mood and health evolve with every action you take. Each pet has its own personality and stats, and you can experiment with a range of foods that impact mood and health in surprising ways. Dive in, unleash your creativity, and enjoy endless hours of fun with Petpy – where coding meets companionship!

## To Do
- [ ] badge
- [ ] link to show package on PyPI

## Instructions for Contributing to PetPy
1. **Install Python**:
    - Make sure you have Python version 3.8 or higher on your computer. If not, you can download it from python.org.

2. **Clone the repository**:
    - First, clone the repository to your local machine:
        ```bash
        git clone https://github.com/software-students-fall2024/3-python-package-job-offer-plz.git
        cd your-cloned-directory
        ```

3. **Set up a Virtual Environment**:
    - It’s best to work in a virtual environment to manage dependencies and avoid conflicts. You can create a virtual environment with the following command:
        ```bash
        python3 -m venv .venv
        ```
    - Activate the Virtual Environment
        - On Windows:
            ```bash
            .venv\Scripts\activate
            ```
        - On macOS/Linux:
            ```bash
            source .venv/bin/activate
            ```

4. **Install Dependencies**:
    - Install the required dependencies by running the following command:
        ```bash
        pip install -r requirements.txt
        ```

5. **Build the Package**:
    - First, make sure pyproject.toml is in the root directory of your project file. Install the build package by running the following command:
        ```bash
        pip install build
        ```
    - Then, run the build command:
        ```bash
        python -m build
        ```
    - This command will generate distribution files in the dist/ directory, such as a .tar.gz source distribution and a .whl wheel file.

6. **Running the Tests**:
    - Testing is essential to ensure your changes work as expected. Petpy uses pytest for testing, so make sure it’s installed (should be in requirements.txt)
    - To run all tests, use:
        ```bash
        pytest tests/
        ```
7. **Guildlines for Contributing**:
    - Create a New Branch for each feature or bug fix:
        ```bash
        git checkout -b feature-name
        ```
    - Make sure to write clear and descriptive commit messages:
        ```bash
        git add .
        git commit -m "Description of the changes"
        ```
    - Push your changes to the remote repository:
        ```bash
        git push origin feature-name
        ```
    - Create a Pull Request to the main branch:
        - Go to the repository on GitHub
        - Click on the "Pull Request" button on the top right
        - Select the branch you want to merge into the main branch
        - Click on the "Create Pull Request" button

## Instructions for Running PetPy
- To run all parts of the PetPy package, follow steps 1-6 in the "Contributing to PetPy" section.
- To run the program, follow the steps below:
    - Open a new terminal window and navigate to the root directory of the cloned repository.
    - Activate the virtual environment:
        - On Windows:
            ```bash
            .venv\Scripts\activate
            ```
        - On macOS/Linux:
            ```bash
            source .venv/bin/activate
            ```
    - Run the program:
        ```bash
        python petpy/src/main.py
        ```
    - Follow the prompts to create a new pet and explore its features!

## Using PetPy in Your Project
1. **Installation**:
    - Install the package using pip:
        ```bash
        pip install petpy
        ```
    - Once installed, you can import and use it in your project.

2. **Importing the Package**:
    - To import the package, use the following code:
        ```python
        from petpy.src import petpy
        from petpy.src.petpy import pets
        ```
    ### Class and Function Documentation
    1. **Pet Class**:
        - Defines a virtual pet with attributes like name, type, emoji, level, experience, health, and mood.
            - **name**: The name of the pet.
            - **type**: The type of the pet.
            - **emoji**: The emoji of the pet.
            - **level**: The level of the pet.
            - **experience**: The experience of the pet.
            - **health**: The health of the pet, max health is 20 and varies between 15-20 when pet is first created.
            - **mood**: The mood of the pet, max mood is 10.
    2. **Functions**:
        - **create_pet(pet_name, pet_type)**: Creates a new pet and adds it to the global pets dictionary.
            - Example:
                ```python
                    my_pet = create_pet("Buddy", "dog")
                    print(f"{my_pet.name} has been created as a {my_pet.type}!")
                ```
        - **feed_pet(pet_name, food_name)**: Feeds a pet, adjusting its mood and health based on the food type. Pets may leave if their mood goes too high or too low during feeding.
            - Example:
                ```python
                    feed_result = feed(my_pet, "kfc")
                    print(feed_result)  
                ```
        - **get_pet_mood(pet)**: Returns the pet's mood level with a description.
            - Example:
                ```python
                    print(get_pet_mood(my_pet))
                ```
        - **get_pet_health(pet)**: Returns the pet's current health level.
            - Example:
                ```python
                    print(get_pet_health(my_pet))
                ```
        - **train_pet(pet_name, skill_name)**: Trains the pet, boosting experience but reducing mood based on training intensity.
            - Example:
                ```python
                    train_pet(my_pet)
                ```
        - **get_pet_level(pet)**: Returns the pet's current level and experience.
            - Example:
                ```python
                    print(get_pet_level(my_pet))
                ```
        - **get_pet_stats(pet, pet_name)**: Returns all stats of the pet if the name matches.
            - Example:
                ```python
                    stats_info = get_pet_stats(my_pet, "Buddy")
                    print(stats_info)  # Displays comprehensive stats for Buddy.
                ```
        - **fight(pet)**: Engages the pet in a fight with a random outcome based on mood.
            - Example:
                ```python
                    fight(my_pet)   
                ```
        - **release(pet_name)**: Releases a pet from the pets dictionary, removing it permanently.
            - Example:  
                ```python                    
                    release_message = release_pet("Buddy")
                    print(release_message)  # Output: "Buddy has been released :("
                ```
    3. **Example Program**:
        - Here is a sample program demonstrating how to create a pet, interact with it, and display its stats:
            - [example.py](https://github.com/software-students-fall2024/3-python-package-job-offer-plz/blob/main/example.py)

## Team Members    
- [Alex Ruan](https://github.com/axruan)
- [Angela Zhang](https://github.com/angelazzh)
- [Leo Bernarbezheng](https://github.com/leonaurdo)
- [David Lai](https://github.com/danonymouse)
