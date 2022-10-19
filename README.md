# interview-scheduler
This is an Interview Scheduling Portal where admins can create interviews by selecting participants, interview start time and end time based on certain validations.

Made as part of my Scaler Interview Process this is a Single Page Application developed using Django Rest Framework.
To access:
1. Open the repository in an editor of your choice and open the terminal.
2. Use the command "python manage.py runserver" to start your local server.
3. Open the provided link in your browser (eg: http://127.0.0.1:8000/).
4. You can now access the page to create an interview meet and view all the upcoming Interviews as the admin.

Since this page is only meant to be accessed by the admin, user will have to create their own data entries of the participants. This can be done by django's inbuilt Database Management System.
To create user entries:
1. Open the repository in an editor of your choice and open the terminal.
2. Use the command "python manage.py createsuperuser" to create an admin and set your credentials.
3. Go to your webpage and add "/admin" at the end of your url (eg: http://127.0.0.1:8000/admin).
4. login using your set superuser credentials.
5. Go to the "Candidates" table and enter your user data.

Once Interviews are scheduled, Admin can view them all in the "Upcoming Interviews" section and individually re-schedule (update) and delete them. It is given that any new or updated meet cannot clash with an existed meet. Additionally, there can not be less than 2 participants in a given interview slot.


Note: Participants will be notified on their mail about the interview schedule.
