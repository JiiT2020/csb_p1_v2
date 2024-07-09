MOOC CSB Project I

LINK: [link to the repository](https://github.com/JiiT2020/csb_p1_v2/tree/master)
installation instructions if needed

There are other vulnerabilities and/or vulnerability strawmans in the code. I sketched those during the process but they didn't end up to my selection of five real threats.

Installation in virtual environment:

python3 -m venv poll_app
source poll_app/bin/activate
pip install -r requirements.txt
python3 manage.py runserver
...
deactivate
rm -rf venv

FLAW 1: A07:2017-CROSS-SITE SCRIPTING (XSS-injection)

exact source link pinpointing flaw 1...
description of flaw 1...
how to fix it...

This flaw allows XSS-injection via comment's text field. Once a vulnerability is injected, it ends up to database and will be executed on any user's terminal who will be viewing comments. Front end allows usafe html-content to be rendered (see: {{ comment.text|safe }} on row 19 of comment_thank_you.html). However, fixing the frontend wouldn't fix the actual problem, which is in polls/models.py where plain text (text = models.TextField() on row 26) is accepted from the end-user and that text is stored to database as such. This can be demonstrated by uploading a comment: <script>alert('xss-injection attack')</script>

Fix is in polls/models.py, row 27 which shall replace row 26. On row 27 the BleachField() sanitizes the comment text field before it is stored into the database.


FLAW 2: A04:2017-XML EXTERNAL ENTITIES
exact source link pinpointing flaw 2...
upload/views.py row 24
Creating new votes may be done by uploading an xml-file to the poll app web page. Uploading happens via 127.0.0.1:8000/upload (note: user has to be signed in first). In folder utilities/ there is one legitimate xml-file and one malicious xml-file. If the malicious xml-file is uploaded, malicious code is executed. In the example code etc/passwd file's content is read and written to a new poll. I.e. passwd-file is compromised andit can then be seen via polls if user browses to http://127.0.0.1:8000/polls/.

This is fixed by disabling the XML-parser to resolve entities. Fix on row 25 of upload/views.py.


FLAW 3: A05:2017-BROKEN ACCESS CONTROL (+csrf)
This vulnerability utilises CSRF and demonstration also requires exmpting it in one place. Since Django framework takes care of CSRF automatically, it has to be exempt. CSRF is exempt for upload_new_poll-function in upload/views.py (rows 2 and 16). (Using csrf as a flaw is explicitly allowed in the exercise instructions, so here I'm learning the impact of two flaws.)

Anybody can vote anonymously, but uploading new polls should be possible for registered users only. Uploading happens via 127.0.0.1:8000/upload.  Now the upload/-page requests to sign in, if the user is not signed in. But vulnerability is that only the client checks if the user is signed in or not. So, by using e.g. Burpsuite a new_vote-xml-file may be POSTed to the backend without singing in. This may be demonstrated by copying a valid POST request (of a signed-in user), altering the poll questions and choices, and then POSTing it to backend once the user is signed out. 

This flaw is fixed by verifying in backend that the user is signed in. Django provides a user.is_authenticated -attribute for that. It is imported (upload/views.py row 3) and taken into use (upload/views.py row 17).
Also, the exemption of not demanding CSRF has to be removed (upload/views.py, deleting row 16 (and row 2)).


Flaw 4: A03:2017-SENSITIVE DATA EXPOSURE
polls/comment_thank_you.html

Sensitive data is leaking due to forgotten console.logs and  <li style="display: none">-component in comment_thank_you.html. Viewing the page via developer tools, email-addresses of the commentators may be seen.

Fix is to remove the script which causes console.logging (row 22) and removing the <li style="display: none"> tagged text (row 20), as they are obsolete and the developer has been using them in development phase.


FLAW 5: A09:2017-USING COMPONENTS WITH KNOWN VULNERABILITIES


*******************EI TOIMI NÄIN*****************EI BUGAA !************************

Vulnerability in ./requirements.txt

An old component versions have slipped in to installation instructions in requirements.txt. It installs django-debug-toolbar==2.2
django-bleach==3.1.0
django-allauth==0.40.0
lxml==4.6.4
all of which except django-bleach are known to contain vulnerabilities with medium or high ranking.

(Note: not all of those vulnerabilities can be used for exploiting this app, for example django-allauth component's account hijacking (CVE-2019-19844) vulnerability would require Postgres.)

fix is to upgrade components to newer versions, like:
django-debug-toolbar==2.3
django-bleach==3.1.0
django-allauth==0.63.3
lxml==5.2.2

exact source link pinpointing flaw 5...
description of flaw 5...
how to fix it...

Kokeile tämän sijaan tehdä SQL injection searchiin viidentenä vulnerabilitynä








Lisäksi! Tarkista miten csrf käyttäytyy kun koodiin tuli csrfMiddleware-juttu (settings.py ja middleware.py) iframen toimimisen vuoksi. Eli selvitä miten csrf_exempt käyttäytyy eri tilanteissa. Voiko sen jättää pois (eli toimiiko ilman csrf_exemptiä) ja jos sen voi jättää pois, niin saako explisiittisesti korjattua jolalin %csrfllä?