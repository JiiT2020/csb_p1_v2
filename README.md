
# MOOC CSB Project I

LINK: [link to the repository](https://github.com/JiiT2020/csb_p1_v2/tree/master)

This application is based on Django starter webapp (polls) [ref: https://docs.djangoproject.com/en/3.1/intro/tutorial01/] which was pointed out as a possible baseline for Project I in exercise instructions. I have extended the service with multiple features/functionalities and now briefly the user can: register to the service, login/logout, cast votes in various polls, leave anonymous comments per each poll after voting, search for polls and upload new polls using xml-templates.

I have chosen below five OWASP-flaws according to **OWASP 2017 top-ten**-list. However, there are other vulnerabilities and/or vulnerability strawmans in the code. I sketched those during the process but they didn't qualify / end up to my selection of five real flaws/threats. (For example out-dated components; although CVE-vulnerabilites became included they were not relevant for this service or my environment.)

Installation in virtual environment, just run:
```bash
./setup.sh
```
Service then runs in http://127.0.0.1:8000


## FLAW 1: A07:2017-CROSS-SITE SCRIPTING (XSS-injection)

https://github.com/JiiT2020/csb_p1_v2/blob/master/polls/models.py#L26

When user is leaving a comment, this flaw allows XSS-injection via comment's text field. Once a vulnerability is injected, it ends up to database and will be executed on any user's terminal who will be viewing comments. Frontend allows unsafe html-content to be rendered (see: {{ comment.text|safe }} on row 19 of [comment_thank_you.html](https://github.com/JiiT2020/csb_p1_v2/blob/master/polls/templates/polls/comment_thank_you.html#L19). However, fixing the frontend wouldn't fix the actual problem, which is in polls/models.py where plain text (text = models.TextField() on row 26) is accepted from the end-user and that input text is stored to database as such. This can be demonstrated by uploading a comment: ```<script>alert('xss-injection attack')</script>```. Once the comment is rendered/viewed anfter that, the script will be executed. (The not-so-malicious XSS-script is only for demonstrating purposes.)

Fix is in [polls/models.py, row 27](https://github.com/JiiT2020/csb_p1_v2/blob/master/polls/models.py#L27) which shall replace row 26. On row 27 the BleachField() sanitizes (i.e. removes illegal characters from) the comment text field before it is stored into the database.

[Also {{ comment.text|safe }} may be changed to {{ comment.text }} in [comment_thank_you.html](https://github.com/JiiT2020/csb_p1_v2/blob/master/polls/templates/polls/comment_thank_you.html#L19), BUT that is not enough to make the service safe since it does not prevent root cause injection.]


## FLAW 2: A04:2017-XML EXTERNAL ENTITIES

https://github.com/JiiT2020/csb_p1_v2/blob/master/upload/views.py#L24

Creating new votes may be done by uploading an xml-file to the poll app web page. Uploading happens via 127.0.0.1:8000/upload (note: user has to be signed in first). In folder utilities/ there is one legitimate xml-file [question_legit.xml](https://github.com/JiiT2020/csb_p1_v2/blob/master/utils/question_legit.xml) which is a valid template for uploading polls in xml-format and one malicious xml-file [question_malicious.xml](https://github.com/JiiT2020/csb_p1_v2/blob/master/utils/question_malicious.xml). If the malicious xml-file is uploaded, malicious code is executed. In this example case, code etc/passwd file's content is read and written to a new poll's subject. I.e. passwd-file is compromised and it can then be seen via polls if user browses to http://127.0.0.1:8000/polls/. (The not-so-malicious xml-file is only for demonstarting purposes.)

This is fixed by disabling the XML-parser to resolve entities (setting it to False). Fix on [row 25 of upload/views.py](https://github.com/JiiT2020/csb_p1_v2/blob/master/upload/views.py#L24) which replaces row 24.


## FLAW 3: A05:2017-BROKEN ACCESS CONTROL (+CSRF)

https://github.com/JiiT2020/csb_p1_v2/blob/master/upload/views.py#L16
and
https://github.com/JiiT2020/csb_p1_v2/blob/master/upload/views.py#L17

This vulnerability utilizes CSRF and demonstration also requires exmpting it in one place. Since Django framework takes care of CSRF automatically, it has to be exempt. CSRF is exempt for upload_new_poll-function in upload/views.py ([rows 2](https://github.com/JiiT2020/csb_p1_v2/blob/master/upload/views.py#L2) and [16](https://github.com/JiiT2020/csb_p1_v2/blob/master/upload/views.py#L16)). (Using CSRF as a flaw is explicitly allowed in the exercise instructions, so here I'm actually learning the impact of two (2) flaws.)

Anybody can vote anonymously, but uploading new polls should be possible for registered users only. Uploading happens via 127.0.0.1:8000/upload. Now the upload/-page requests to sign in, if the user is not yet signed in. But vulnerability is that only the client checks if the user is signed in or not. So, by using e.g. Burpsuite a new_vote-xml-file may be POSTed to the backend without singing in. This may be demonstrated by copying a valid POST request (of a signed-in user), altering the poll questions and choices, and then POSTing it to backend (to 127.0.0.1:800/upload) once the user is signed out.

This flaw is fixed by verifying in backend that the user is signed in. Django provides a "user.is_authenticated"-attribute for that. It is imported [(upload/views.py row 3)](https://github.com/JiiT2020/csb_p1_v2/blob/master/upload/views.py#L3) and taken into use [(upload/views.py row 17)](https://github.com/JiiT2020/csb_p1_v2/blob/master/upload/views.py#L17).
Also, the exemption of not demanding CSRF has to be removed ([upload/views.py, deleting row 16](https://github.com/JiiT2020/csb_p1_v2/blob/master/upload/views.py#L16) (and [on row 2](https://github.com/JiiT2020/csb_p1_v2/blob/master/upload/views.py#L2))).


## FLAW 4: A03:2017-SENSITIVE DATA EXPOSURE

https://github.com/JiiT2020/csb_p1_v2/blob/master/polls/templates/polls/comment_thank_you.html#L20
and
https://github.com/JiiT2020/csb_p1_v2/blob/master/polls/templates/polls/comment_thank_you.html#L22

Sensitive data is leaking due to forgotten development phase console.logs and ```<li style="display: none">```-component in comment_thank_you.html. Such kind of lines are typically added in development phase, to see what values certain variables are holding at a time being, e.g. if the db has returned correct values needed at certain point of UI-flow. Due to these, viewing the page via browser's Developer tools, email-addresses of the commentators may be seen although emails are supposed to be sensitive&hidden - and explicitly unassociated with anonymous comments.

Fix is to [remove the script which causes console.logging (row 22)](https://github.com/JiiT2020/csb_p1_v2/blob/master/polls/templates/polls/comment_thank_you.html#L22) and [removing the ```<li style="display: none">``` tagged text (row 20)](https://github.com/JiiT2020/csb_p1_v2/blob/master/polls/templates/polls/comment_thank_you.html#L20), as they are obsolete and the developer (me ;-) has been utilizing them in development phase.


## FLAW 5: A06:2017-SECURITY MISCONFIGURATION

https://github.com/JiiT2020/csb_p1_v2/blob/master/mysite/settings.py#L26

Debugging has been forgotten to "True" in settings.py, line 26. (Furthermore, default password for "admin" has been left to the service.)

Having debugging set to "True" anybody can see details of error messages without any limitations. This may lead to disclosure of sensitive information about for example file/path names, environmental variables or even maybe API-keys or alike.

In this service, end user may e.g. try some unexisting path http://127.0.0.1:8000/polls/unexisting_path which discloses lots of hints about how the service works, it's structure etc. It for example reveals that there is a path for "admin/". Having found out that, the attacker may also try default username/password and find out that it actually is default: admin/admin. That is another flaw in this same category "A06: Security Misconfiguration".

Fix is to [set the debugging to False (line 28)](https://github.com/JiiT2020/csb_p1_v2/blob/master/mysite/settings.py#L28). Setting it to False requires ALLOWED_HOSTS to be set as well. Allowed host(s) can be set simply e.g. to 127.0.0.1 which enables debugging for local host [(line 29)](https://github.com/JiiT2020/csb_p1_v2/blob/mysite/settings.py#L29). Furthermore, the admin's default password has to be changed to more complex one, e.g. via admin page.
