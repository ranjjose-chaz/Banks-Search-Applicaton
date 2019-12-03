from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.forms.models import model_to_dict

from .models import Greeting
from .models import Banks
from .models import BankBranches

import requests
import os
import json
import jwt

def validate_jwt(f):    
    def wrapper(*args, **kw):
        #token = args[0].GET.get('jwt')
        #print ('token -- >', token)
        #print (type(token))
        token_header = args[0].META.get('HTTP_AUTHORIZATION')
        #print ('token_header -- >', token_header)
        #print (type(token_header))

        try:
            jwt.decode(token_header, 'secret', algorithms=['HS256'])
        except Exception as e:
            print(e)
            return JsonResponse({"message": "JWT token invalid"}, status=401)             
        return f(*args, **kw)      
    return wrapper


#def jwt_not_validated(token):
#    try:
#        jwt.decode(token, 'secret', algorithms=['HS256'])
#    except:
#        return True
#    return False	

# Create your views here.
def index(request):
    times = int(os.environ.get('TIMES',3))
    return HttpResponse('Hello! ' * times)


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})


def banks_html(request):
    banks_list = Banks.objects.all()[:10] 
    return render(request, "banks.html", {"banks": banks_list, 'count': len(banks_list)}) 
    #return HttpResponse("There are {} Banks".format(len(banks)))   

@validate_jwt
def banks(request, ifsc=None):
    if ifsc:

        #if jwt_not_validated(request.GET.get('jwt')):
        #    return JsonResponse({"message": "JWT token invalid"}, status=401)  

        try:
            bank = BankBranches.objects.get(ifsc=ifsc)
        except BankBranches.DoesNotExist:
            return JsonResponse({"message": "The item does not exist"}, status=404)    
        #return JsonResponse(render_json(bank));
        #return JsonResponse(serializers.serialize('json', [bank]))
        #return JsonResponse(model_to_dict(bank))
        return JsonResponse(model_to_dict(bank))
        

    return JsonResponse()    


@validate_jwt
def branches(request):
    bank_name = request.GET.get('bank_name')
    city = request.GET.get('city')
    limit = request.GET.get('limit')
    offset = request.GET.get('offset')
    if bank_name and city and limit and offset and limit.isdigit() and offset.isdigit() and int(limit) > 1:
        limit = int(limit)
        offset = int(offset)
        print("All good..!!")
        branch_list = BankBranches.objects.filter(city=city, bank_name=bank_name).order_by('ifsc')[offset:(offset+limit)]
        if not branch_list:
            return JsonResponse({"message": "The item does not exist"}, status=404)    
        return JsonResponse([model_to_dict(branch) for branch in branch_list], safe=False)
    return JsonResponse({"message": "The request can't be processed"}, status=422)    
    #return JsonResponse(render_json([branch for branch in branch_list]), safe=False);
    #return JsonResponse(serializers.serialize('json', branch_list), safe=False)
    
    #return render(request, "branch_list.html", {"branch_list": branch_list})  



def bank_details_html(request, ifsc=None):
    branch_list = BankBranches.objects.filter(ifsc=ifsc) if ifsc else BankBranches.objects.all()[:50]
    return render(request, "branch_list.html", {"branch_list": branch_list})  


def branches2_html(request):
    bank_name = request.GET.get('bank_name')
    city = request.GET.get('city')
    limit = request.GET.get('limit')
    offset = request.GET.get('offset')
    if bank_name and city and limit and offset and limit.isdigit() and offset.isdigit() and int(limit) > 1:
        limit = int(limit)
        offset = int(offset)
        branch_list = BankBranches.objects.filter(city=city, bank_name=bank_name).order_by('ifsc')[offset:(offset+limit)]
    else:
        branch_list = []    

    return render(request, "branch_list.html", {"branch_list": branch_list})    


    
def to_dict(model):
    if isinstance (model, BankBranches):
        return {'ifsc': model.ifsc, 
                'bank_id':model.bank_id,
                'branch':model.branch,
                'address':model.address,
                'city':model.city,
                'district':model.district,
                'state':model.state, 
                'bank_name':model.bank_name }
    return {}       

def render_json(data):
    if isinstance (data, BankBranches):
        print(" response is NOT list ")
        return to_dict(data)
    elif isinstance (data, list):
        print(" response is list ")
        return [to_dict(i) for i in data]
    else:
        print(" response is unhandled")
        print(type(data))
        return []