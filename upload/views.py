from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
#from django.contrib.auth.decorators import login_required    #FLAW 3 FIX (2/3): enable this

# Create your views here.

import lxml.etree as ET
#from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from polls.models import Question, Choice
from .forms import UploadPoll

#def upload_new_poll(request):
#    return render(request, 'upload/upload_new_poll.html')

@csrf_exempt    #FLAW 3 FIX (1/3): disable this
#@login_required    #FLAW 3 FIX (3/3): enable this
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
    