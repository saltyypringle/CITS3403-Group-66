# SukiScan 
### Description
Sukiscan is a web application designed for users to understand their taste in anime characters by analysing the traits of the characters they like. 

The application allows users to upload anime characters, along with key attributes such as the character’s name, MBTI personality type, physical traits (e.g., hair colour and height), and other details like age, profession and character type. Sukiscan then analyses the common patterns and trends in the user’s preferences and provides data visualisations highlighting trends, similarities, and a character that best fits the user’s profile. 

Additionally, the application includes social features. Users can friend others, and once connected, they can view their friends’ taste profiles and character uploads. Sukiscan also includes discussion forums, where users can post, reply, and engage in conversations about characters, trends, and shared interests with others.

### Technology Stack, Implementation and Data Setup
Sukiscan is built with Flask on the backend and uses HTML, Bootstrap, and JavaScript on the frontend. Core Flask features like routing, sessions, and form handling are used alongside Flask-Login for authentication and Werkzeug for password hashing.

The app is structured into modules (routes, models, forms) and initialised in SukiScan/sukiscan.py. The database is managed with SQLAlchemy and created dynamically on startup from model definitions — no pre-built .db file is needed. The blank database can be seeded with initial data using seed.py, which includes a list of characters to populate the application. Running the seed script will insert these entries into the database.

### Group Members
| UWA ID    | Name              | GitHub Username  |
|-----------|-------------------|------------------|
| 23970776  | Ganesh Chinnasamy | ganeshcy         |
| 23779727  | Dipika Choudhury  | saltyypringle    |
| 23873958  | Minh Nguyen       | PapaClaudee      |
| 23926055  | Henry Yau         | HenryGod69       |


### Launching Application


1. Set Up
   **Cloning Git Repo**
   
   ```sh
   https://github.com/saltyypringle/CITS3403-Group-66.git
   ```

   **Unzip File**
   ```sh
   Unzip the project file
   ```

2. Open and run in terminal
   ```sh
    cd CITS3403-Group-66
   ```
3. Create a virtual environment:

    **For Windows(Command Prompt)**

    ```sh
    python -m venv venv
    venv\Scripts\activate
    ```
    
   **For Windows(Powershell)**

    ```sh
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    ```

    **For Mac/Linux**

    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```
5. Install Dependencies
   ```sh
   pip install -r requirements.txt
   ```

6. Set Environment Variable

    **For Windows(Command Prompt)**

    ```sh
    set FLASK_APP=SukiScan
    ```
    
   **For Windows(Powershell)**

    ```sh
    $env:FLASK_APP = "SukiScan"
    ```

    **For Mac/Linux**

    ```sh
    export FLASK_APP=SukiScan
    ```
7. Create the data directory (if it does not exist)
   ```sh
   mkdir data

8. Apply Existing Database Migrations

   The database schema is already defined in the repository’s migrations/ folder. To set up the database, simply run:
      ```sh
      flask db upgrade
      ```

9. Run seed.py to seed the database
   ```sh
   python seed.py
    ```

10. Run the application
   ```sh
   python sukiscan.py

   ```

### Run test 
1. Run the tests.py file
   **Run in terminal**

   ```sh
   python -m unittest tests/unittests.py
   ```


### Markers Guide
```sh
Note: This is just a friendly recommendation of the most efficient way to navigate our website, by all means explore however you wish to :)
```

