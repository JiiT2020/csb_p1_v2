# MOOC CSB Project I

LINK: [link to the repository](https://github.com/JiiT2020/csb_p1_v2/tree/master)

This application is based on Django starter webapp (polls) [ref: https://docs.djangoproject.com/en/3.1/intro/tutorial01/] which was pointed out in Project I exercise instructions. I have additionally extended the service and briefly the user can: register to the service, login/logout, cast votes in polls, leave anonymous comments per poll after voting, search for polls and upload new polls using xml-template.

I have chosen below five OWASP-flaws according to OWASP 2017 top-ten-list. However, there are other vulnerabilities and/or vulnerability strawmans in the code. I sketched those during the process but they didn't qualify / end up to my selection of five real threats.

Installation in virtual environment:
```bash
python3 -m venv poll_app
source poll_app/bin/activate
pip install -r requirements.txt
python3 manage.py runserver
```
Service then runs in http://127.0.0.1:8000

Removing venv after use:
```bash
deactivate
rm -rf venv
```

## FLAW 1: A07:2017-CROSS-SITE SCRIPTING (XSS-injection)

exact source link pinpointing flaw 1...
description of flaw 1...
how to fix it...

polls/models.py, row 27

This flaw allows XSS-injection via comment's text field. Once a vulnerability is injected, it ends up to database and will be executed on any user's terminal who will be viewing comments. Front end allows usafe html-content to be rendered (see: {{ comment.text|safe }} on row 19 of comment_thank_you.html). However, fixing the frontend wouldn't fix the actual problem, which is in polls/models.py where plain text (text = models.TextField() on row 26) is accepted from the end-user and that text is stored to database as such. This can be demonstrated by uploading a comment: <script>alert('xss-injection attack')</script>

Fix is in polls/models.py, row 27 which shall replace row 26. On row 27 the BleachField() sanitizes (i.e. removes illegal characters from) the comment text field before it is stored into the database.
[Also {{ comment.text|safe }} may be changed to {{ comment.text }} BUT that is not enough to make the service safe.]


## FLAW 2: A04:2017-XML EXTERNAL ENTITIES

upload/views.py row 24
Creating new votes may be done by uploading an xml-file to the poll app web page. Uploading happens via 127.0.0.1:8000/upload (note: user has to be signed in first). In folder utilities/ there is one legitimate xml-file (question_legit.xml) and one malicious xml-file (question_malicious.xml). If the malicious xml-file is uploaded, malicious code is executed. In the example code etc/passwd file's content is read and written to a new poll. I.e. passwd-file is compromised and it can then be seen via polls if user browses to http://127.0.0.1:8000/polls/. (The malicious xml-file is only for demonstarting xml-execution purpose.)

This is fixed by disabling the XML-parser to resolve entities. Fix on row 25 of upload/views.py.


## FLAW 3: A05:2017-BROKEN ACCESS CONTROL (+CSRF)
This vulnerability utilises CSRF and demonstration also requires exmpting it in one place. Since Django framework takes care of CSRF automatically, it has to be exempt. CSRF is exempt for upload_new_poll-function in upload/views.py (rows 2 and 16). (Using CSRF as a flaw is explicitly allowed in the exercise instructions, so here I'm actually learning the impact of two (2) flaws.)

Anybody can vote anonymously, but uploading new polls should be possible for registered users only. Uploading happens via 127.0.0.1:8000/upload.  Now the upload/-page requests to sign in, if the user is not yet signed in. But vulnerability is that only the client checks if the user is signed in or not. So, by using e.g. Burpsuite a new_vote-xml-file may be POSTed to the backend without singing in. This may be demonstrated by copying a valid POST request (of a signed-in user), altering the poll questions and choices, and then POSTing it to backend once the user is signed out. 

This flaw is fixed by verifying in backend that the user is signed in. Django provides a "user.is_authenticated"-attribute for that. It is imported (upload/views.py row 3) and taken into use (upload/views.py row 17).
Also, the exemption of not demanding CSRF has to be removed (upload/views.py, deleting row 16 (and row 2)).


## Flaw 4: A03:2017-SENSITIVE DATA EXPOSURE
polls/comment_thank_you.html

Sensitive data is leaking due to forgotten development phase console.logs and ```<li style="display: none">```-component in comment_thank_you.html. Suchkind of lines are typically added in development phase, to see what values certain variables are holding e.g. if the DB has returned correct values needed at certain point of development. Due to these, viewing the page via browser's Developer tools, email-addresses of the commentators may be seen although emails are supposed to be sensitive&hidden. And explicitly unassociated with anonymous comments.

Fix is to remove the script which causes console.logging (row 22) and removing the ```<li style="display: none">``` tagged text (row 20), as they are obsolete and the developer has been utilizing them in development phase.


## FLAW 5: A06:2017-SECURITY MISCONFIGURATION

Debugging has been forgotten to "True" in settings.py, line 26. (Furthermore, default password has been left to the service.)

Having debugging set to "True" anybody can see details of error messages without any limitations. This may lead to disclosure of sensitive information about for example environmental variables, database-/API-keys or alike.

In this service, end user may e.g. try unexisting path http://127.0.0.1:8000/polls/unexisting_path which discloses lots of hints about how the service works, it's structure etc. It for example reveals that there is a path for "admin/". Having found out that, the attacker may also try default username/password and find out that it actually is default: admin/admin. That is another flaw in this same category "A06: Security Misconfiguration".

Fix is to set the debugging to False (line 28). Setting it to False requires ALLOWED_HOSTS to be set as well. Allowed host(s) can be set simply e.g. to 127.0.0.1 which enables debugging for local host (line 29). Furthermore, the admin's default password has to be changed to more complex one, e.g. via admin page.




Lisäksi! Tarkista miten csrf käyttäytyy kun koodiin tuli csrfMiddleware-juttu (settings.py ja middleware.py) iframen toimimisen vuoksi. Eli selvitä miten csrf_exempt käyttäytyy eri tilanteissa. Voiko sen jättää pois (eli toimiiko ilman csrf_exemptiä) ja jos sen voi jättää pois, niin saako explisiittisesti korjattua jolalin %csrfllä?