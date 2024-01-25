# moneyball

To do:

1. Create the frontend templates for the home page, about page, sign up, sign in, user home, and admin home. These templates will be created using HTML and will be styled with CSS to match the modern, soccer-themed design requirements.

2. Implement the backend logic for user authentication. This includes handling the sign-up process by storing user credentials in the database and handling the sign-in process by authenticating users against the stored credentials.

3. Implement the game management logic. This includes allowing the admin to start a new round, input games for the week, and close registration for a new round.

4. Implement the leaderboard display logic. This includes querying the database for past winners and displaying them on the home page.

5. Create the necessary styles and scripts to enhance the user interface and user experience.

6. Update the `requirements.txt` file if any new dependencies are introduced during the implementation.

7. Write the necessary route handlers in `routes.py` to serve the new templates and handle form submissions.

8. Update the `models.py` file to include any new models or relationships needed for the game management and leaderboard features.

9. Create a new admin account with the ability to manage the game rounds.

10. Implement the logic for users to make their picks and display their current picks, previous round performance, total all-time winnings, and progress this round on their home page.

11. Implement the logic to automatically generate an overview summary table of every pick and which team they picked that round once the admin closes the registration for a new round.




old stuff:
you have started the moneyball website:

now, 
Next, we will implement the frontend templates, styles, and scripts, and complete the backend logic for user authentication, game management, and leaderboard display.

Please note that this is a complex project and the implementation provided here is a high-level overview. A fully working implementation would require more detailed code for each component, including proper form validations, database interactions, user authentication logic, admin functionalities

old instructions: Build a website titled Moneyball. Make sure the code you write has ALL the following elements and ALL the necessary templates. The style should be very clean and modern and be soccer themed. It should look very modern and include creative fun elements that make it look good. The nav bar should have Home, About, and sign in and sign up buttons. The about page should include the rules of the game. The home page for now should say "Welcome to Moneyball", and then include a leaderboard of past winners (will be described later). 

Once users sign up using username, email and password, that is then stored in the back end. Users can now then sign in using that account using their username and password and once they are signed in, they have their own home page which has the players' current picks, previous round performance, total all-time winnings and progress this round. 

There should also be one admin account which has the ability to start a new round. The admin gets to start the new round and can input the games that will be happening that week and the date for everyone to see. People can then see these games on their own home pages and can pick a team as per the rules below. The admin cannot participate in the game himself. 

FYI, The rules of the game are as follows:
Each player has 2 picks. Every round, each players gets two choose 2 (one for each pick) English premier league soccer teams that are currently playing. When a game week starts, your pick stays alive if your chosen team wins , and your pick is eliminated if your team draws or loses. If your pick stays alive, you get to submit a new pick of another different team (you cannot pick the same team twice in any given round). The game continues for as many gameweeks as it takes until there is only one pick left alive. To enter, each player must pay for their pick, which is entered into the pot. The game is winner takes all. 

Once the admin closes the registration for a new round, the players entered cannot change. I want it to automatically also include an overview summary table of every pick and which team they picked that round. 
