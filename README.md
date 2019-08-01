# Ferry Schedules

Ferry Schedules is a website I am making in Flask to display ferry schedules from around the United States. Currently, only a handful of schedules are available because I am working more on the code quality than adding more content to the site.

I am currently working on refactoring all of my code, so this is considered Version 2 of the website. Version 1 was functional, but the project structure was poor (i.e. all the code was in a single python file) and there was a lot of code duplication.

In version 2, I've restructured the project into, what I believe to be, a more traditional Flask project structure as well as cleaned up a lot of the code duplication by utilizing Classes for a lot of my functionality.

Currently, I'm using Google Sheets as a psuedo-CMS to power each page in the site. Basically, each schedule page has its own tab in the Google Sheet which houses all of its meta data (title tags, h1, h2, etc..) and time tables. I then authenticate and connect to the Google Sheet using the **gspread** library to consume the schedule data.

The front-end is just basic Bootstrap, with a hint of additional CSS that I've added.

