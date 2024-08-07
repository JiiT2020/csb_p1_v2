from django.shortcuts import render

import lxml.etree as ET
from django.http import HttpResponse, HttpResponseRedirect
from polls.models import Question, Choice
from .forms import UploadPoll
from django.views.decorators.csrf import csrf_exempt     #FLAW 3 (2/4). To fix flaw 3, disable this row
#from django.contrib.auth.decorators import login_required    #FLAW 3 (4/4). To fix flaw 3, enable this row


@csrf_exempt    #FLAW 3 (1/4). To fix flaw 3, disable this row
#@login_required    #FLAW 3 (3/4). To fix flaw 3, enable this row
def upload_new_poll(request):
    if request.method == 'POST':
        form = UploadPoll(request.POST, request.FILES)
        if form.is_valid():
            xml_file = request.FILES['new_poll']
            try:
                parser = ET.XMLParser(resolve_entities=True)  # XXE vulnerability causes parser to resolve external entities
                #parser = ET.XMLParser(resolve_entities=False)  # XXE-fix: This setting to False causes external entities not to be resolved
                tree = ET.parse(xml_file, parser)
                root = tree.getroot()
 
                for question_element in root.findall('question'):
                    question_text = question_element.find('text').text

                    if question_text is None:
                        return HttpResponse(f"Uploaded XML file is empty or invalid")
                
                    question = Question.objects.create(question_text=question_text)
                    
                    for choice_element in question_element.findall('choice'):
                        choice_text = choice_element.text

                        if choice_text is None:
                            return HttpResponse(f"Uploaded XML file is empty or invalid")
                    
                        Choice.objects.create(question=question, choice_text=choice_text)
                        
                return HttpResponseRedirect('thankyou/')
            except ET.XMLSyntaxError as e:
                return HttpResponse(f"XML parsing error: {e}")
    else:
        form = UploadPoll()
    
    return render(request, 'upload/upload_new_poll.html', {'form': form, 'user': request.user, 'authenticated': request.user.is_authenticated })

def update_thankyou(request):
    return render(request, 'upload/thankyou.html')
    