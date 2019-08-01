# Ferry Schedules

Ferry Schedules is a website I am making in Flask to display ferry schedules from around the United States. Currently, only a handful of schedules are available because I am working more on the code quality than adding more content to the site.

I am currently working on refactoring all of my code, so this is considered Version 2 of the website. Version 1 was functional, but the project structure was poor (i.e. all the code was in a single python file) and there was a lot of code duplication.

In version 2, I've restructured the project into, what I believe to be, a more traditional Flask project structure as well as cleaned up a lot of the code duplication by utilizing Classes for a lot of my functionality.

Currently, I'm using Google Sheets as a psuedo-CMS to power each schedule page on the site. Basically, each schedule page has its own tab in the Google Sheet which houses all of its meta data (title tags, h1, h2, etc..) and time tables. I then authenticate and connect to the Google Sheet using the **gspread** library to consume the schedule data.

Google Sheet API calls are slow, so consuming this data without caching it is not ideal. Each of these schedules do not change frequently, so version 1 had caching via memcache, using the memcachier service in particular. I've yet to re-implement the caching in version 2, but it is high on my to-do list.

The front-end is just basic Bootstrap, with a hint of additional CSS that I've added to make things look presentable.

I've deployed the app via pythonanywhere and it can be viewed at allferryschedules.com. However, due to the lack of caching, please do not click around too fast because it will quickly reach its Google API limits and starting timing out.

