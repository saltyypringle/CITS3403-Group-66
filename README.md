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
1. Index
   Feel free to navigate anywhere you wish to confirm that only home page is accessible and the login and signup pages are accessible.
   
   Note: Click the logo at top left to return to index if you wish

2. Home Empty
   You will see that there is a section for the most popular characters and also recent forum posts. Those parts are most likely empty right now because there are no users so we will fill those up later.

3. Login User Not Found
   Navigate to the login page and try logging in right now and there should be an error message about user not existing

4. Signup Details 1
   Fill in your details for email, username and password. Click submit and it should instantly log you in.

5. Mypage Empty
   In your my page it'll tell you "Welcome <username>". Look around and you'll see that your page is currently empty. Also navigate to waifu, husbando, and others to see that you currently have no data to analyse

6. Social
   Navigate to socials and make a post, feel free to comment in the post too

7. Add Characters
   Enter fields and add an image of your liking. Open up the database to check that the information was added to either WaifuCheck, HusbandoCheck, OtherCheck tables. Also check that the image was uploaded to image_checker in static.

   Note: This data will not be displayed in the website. It was a unanimous decision that entries of characters should be verified by developers prior to being in use.

8. Search Characters
   On the search bar search Satoru and press go. This should navigate to the search page which should have satoru gojo already in the search page now. 
   Then add at least 10 characters of your liking (Preferably from different categories Waifu, Husbando, Other).
   Add one character an extra time to see that there is an error.

9. Analysis
   Return to mypage and at the bottom you can see who your ideal type is for all 3 categories. 
   Navigate to all the Waifu, Husbando and Other pages to see pie charts and also the list of your characters.
   Remove some characters to see pie charts change.

10. Home Populated
   Now if you navigate to Home page you'll see a latest post and top 10 list populated.

11. Logout
   Logout of your account by pressing on the icon on the top right and pressing logout.

12. Signup Details 2
   Signup with same email and it'll show an error for using pre-existing email.
   Signup with same username and it'll show an error for using pre-existing username. (Make sure email is changed, because it checks email as the first instance)
   Signup and make a new account.

13. Populate Account 2
   Add your data and also comment under the post made prior or add a new post. See the home page change again.
   Note down the data of the pie charts to be checked later.

14. Share Data
   Press the icon up the top right.
   Click friends.
   Search your other account with the username.

15. Back to Account 1
   Navigate to the friends list again.
   You should see under shared with you your other accounts name. And you can see the view button.
   Click on view and check the data shared with you.

16. Change Credentials
   Press icon top right.
   Navigate to details.
   Change your details.
   Check that it's been changed on other pages.

17. Removing friends
   Go back to other account and see that the account name for your friend has changed.
   Remove him from your list.

18. Credentials Changed
   Login with old credentials to check.
   Login with new credentials to check it all works

19. Removed friend
   Check that you can no longer view friends account


