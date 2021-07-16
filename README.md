# Expense Tracker
An easy, user-friendly web application that tracks expenses through categorisation on database based on a particular user's details. 

Some features include:
- Categorisation of expenses which are tracked on the home page
- A page including the history of past expenses ordered by oldest to newest expenses
- A user based system in which different users/accounts can be created to have seperate expense tracking for each user (business expenses vs. personal expenses)
- Easy visualisation of expenses and the corresponding categories are shown as a percentage of the total expense on a dynamic pie chart shown on the index/home page.


The application file is written with the following functions in mind:
1. The /index function for the index app route in flask returns the home page of the web application, where the expense data is loaded from the database based on their category and all expenses within the same category 
are summed together. This data is displayed in the table shown in index.html
In addition to the numerical amounts, the percentage that each category takes up relative to the total expense is also shown and displayed using a dynamic pie chart (credits to "easy pie chart"). The values of the percentages
were calculated after the initial for loop for loading the category values had been completed.

2. The /add function adds expenses that the user chooses from a dropdown menu which includes a predetermined range of categories. Users can also choose to add a note that is attached to the corresponding expense
as well as of course the amount of the expense. This data is then stored into expenses.db under the expense table which also then corresponds that data to the current user's id in the system. 

3. The /history function loads all the expense data that the current user has inputted into the database. This is loaded in chronological order for the convenience of the user. However, in the future an additional feature allowing
the user to choose what variable to order the expenses by, whether that be by the category, amount or date.

4. /login, /logout, /register are all the same functions used in Finance with problem set 9.


The files within templates are:
- add.html returns the page where users are able to add expenses
- apology.html returns the page where errors are redirected towards, with the corresponding error code and message shown as a meme of a cat
- history.html returns the page where users are able to view the history of past expenses order by chronological order
- index.html returns the home page where users are shown a summary of their current expense, both in table and graphical form. The table displays the total expenses under each category while the pie chart shows each category's expenses
as a percentage of the total expense
- login.html show the login page where users are asked for their username and password
- register.html allows user's to register a username and password which is then stored in the users table in expenses.db

The files within static are:
- favicon.ico is the picture displayed at the header of the page
- styles.css is the CSS file including various templates from Bootstrap
- js contains the javascript files allowing for the animation of the piecharts seen in index.html 
