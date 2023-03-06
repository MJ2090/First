from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from embedding.forms.training import TrainingForm
from embedding.forms.translation import TranslationForm
from embedding.forms.grammar import GrammarForm
from embedding.forms.prompt_model import PromptModelForm
from embedding.forms.summary import SummaryForm
from embedding.forms.image import ImageForm
from embedding.forms.chat import ChatForm
from embedding.forms.contact import ContactForm
from embedding.forms.signup import SignupForm
from embedding.forms.signin import SigninForm
from embedding.openai.run import run_it_4, run_it_5, run_it_6, run_it_7, run_it_8, run_it_9
from embedding.openai.run3 import run_it_3
from embedding.models import TokenConsumption, PromptModel
from django.shortcuts import render
from django.db import transaction
from .utils import load_random_string, get_basic_data
from embedding.models import UserProfile
import embedding.static_values as sc
import json


def home(request):
    ret = get_basic_data(request)
    return render(request, 'embedding/home.html', ret)


def embedding(request):
    ret = get_basic_data(request)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TrainingForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            if form.cleaned_data["password"] != "sky":
                return render(request, 'embedding/error.html', {})
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            my_text = form.cleaned_data["message"]
            qs = [form.cleaned_data["q1"]]
            if "q2" in form.cleaned_data and form.cleaned_data["q2"] != "":
                qs.append(form.cleaned_data["q2"])
            if "q3" in form.cleaned_data and form.cleaned_data["q3"] != "":
                qs.append(form.cleaned_data["q3"])
            if "q4" in form.cleaned_data and form.cleaned_data["q4"] != "":
                qs.append(form.cleaned_data["q4"])
            ans = run_it_3(my_text, qs)
            ret['ans'] = ans
            return render(request, 'embedding/answer.html', ret)
        else:
            print("Data not clean!")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TrainingForm()

    return render(request, 'embedding/embedding.html', {'form': form, 'aa': 'sssss'})


def add_prompt_model(request):
    ret = get_basic_data(request)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PromptModelForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            cd = form.cleaned_data
            name = cd.get('name', '')
            history = cd.get('history')
            new_model = PromptModel.objects.create(owner=get_user(request),
                                                   name=name,
                                                   history=history)
            new_model.save()
            return HttpResponse('Done sir.')
        else:
            print("Data not clean!")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PromptModelForm()

    return render(request, 'embedding/super.html', {'form': form, })


def sendchat_t(request):
    model = request.POST.get('model', '')
    new_message = request.POST['message']
    character = request.POST['character']

    my_m = PromptModel.objects.get(name=character)
    messages = json.loads(my_m.history)
    history = request.POST.get('history')
    my_json = json.loads(history)
    messages.extend(my_json)
    messages.append({"role": "user", "content": new_message})

    print("Character: ", character)
    print("Msg sent to openai: ", messages)

    openai_response = run_it_9(messages, model=model)
    ai_message = openai_response["choices"][0]["message"]["content"]
    record_consumption(request, sc.MODEL_TYPES_CHAT, openai_response)
    return HttpResponse(ai_message)


def sendchat(request):
    model = request.POST.get('model', '')
    if model == "gpt-3.5-turbo":
        return sendchat_t(request)
    message = request.POST['message']
    character = request.POST['character']
    history = request.POST.get('history')
    print('model is ', model, history)

    pre_text_dict = {
        "Common AI": "",
        "Assistant": "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n",
        "Mr. President": "In this conversation, AI acts as the President Biden of USA. He serves his contry.\n",
        "Therapist": "In this conversation, AI acts as a top ranked Therapist. He always speaks a lot, providing advices to his patients. He is always nice, friendly and very helpful to his patients.\n",
    }
    pre_text = pre_text_dict.get(character, "")
    post_text = "\nAI: "
    openai_response = run_it_7(pre_text + message + post_text, model=model)
    ai_message = openai_response["choices"][0]["text"]
    record_consumption(request, sc.MODEL_TYPES_CHAT, openai_response)
    return HttpResponse(message + post_text + ai_message + "\nHuman: ")


def chat(request):
    ret = get_basic_data(request)
    form = ChatForm()
    ret['form'] = form
    return render(request, 'embedding/chat.html', ret)


def answer(request):
    ret = get_basic_data(request)
    return render(request, 'embedding/answer.html', ret)


def about(request):
    ret = get_basic_data(request)
    return render(request, 'embedding/about.html', ret)


def payments(request):
    ret = get_basic_data(request)
    return render(request, 'embedding/payments.html', ret)


def settings(request):
    ret = get_basic_data(request)
    return render(request, 'embedding/settings.html', ret)


def contact(request):
    ret = get_basic_data(request)
    # if this is a POST request we need to process the form data

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ContactForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # name = form.cleaned_data["username"]
            print(form.cleaned_data, 88888)
            # ...
            # redirect to a new URL:
            # return render(request, 'embedding/contact.html', {'name': name})
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ContactForm()
    ret['form'] = form
    return render(request, 'embedding/contact.html', ret)


def signout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return HttpResponseRedirect('/')


def signin(request):
    ret = get_basic_data(request)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SigninForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            if do_login(request, username, password):
                print(881)
                # Redirect to a success page.
                print(form.cleaned_data, 4444, request.GET, request.POST)
                next_url = form.cleaned_data.get('next', '/')
                if (not next_url) or next_url.strip() == '':
                    next_url = '/'
                return HttpResponseRedirect(next_url)
            else:
                return render(request, 'embedding/error.html', {'Your account does not exist or has been accidently deleted, sorry about that.'})
        else:
            print("Data not clean!")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SigninForm()
        form.fields['next'].initial = request.GET.get('next', None)
        print(884)

    ret['form'] = form
    return render(request, 'embedding/signin.html', ret)


def signup_async(request):
    return True


def signup(request):
    ret = get_basic_data(request)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SignupForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            cd = form.cleaned_data
            username = cd["username"]
            password = cd["password"]
            do_register(cd)
            do_login(request, username, password)
            return HttpResponseRedirect("/")
        else:
            print("Data not clean!")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SignupForm()
    ret['form'] = form
    return render(request, 'embedding/signup.html', ret)


def send_translation(request):
    ret = get_basic_data(request)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TranslationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            original_text = form.cleaned_data["text"]
            openai_response = run_it_4(original_text, model='text-davinci-003')
            translated_text = openai_response["choices"][0]["text"]
            print(translated_text)
            ret['translated_text'] = translated_text
            record_consumption(
                request, sc.MODEL_TYPES_TRANSLATE, openai_response)
            return render(request, 'embedding/answer.html', ret)
        else:
            print("Data not clean!")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TranslationForm()

    ret['form'] = form
    return render(request, 'embedding/translation.html', ret)


def image(request):
    ret = get_basic_data(request)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ImageForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            if form.cleaned_data["password"] != "sky":
                return render(request, 'embedding/error.html', ret)
            description = form.cleaned_data["text"]
            openai_response = run_it_8(description)
            image_url = openai_response['data'][0]['url']
            print(image_url)
            ret['image_url'] = image_url
            return render(request, 'embedding/answer.html', ret)
        else:
            print("Data not clean!")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ImageForm()
    ret['form'] = form
    return render(request, 'embedding/image.html', ret)


def translation_async(request):
    original_text = request.POST.get('original_text', '')
    openai_response = run_it_4(original_text, model='text-davinci-003')
    translated_text = openai_response["choices"][0]["text"]
    record_consumption(
        request, sc.MODEL_TYPES_TRANSLATE, openai_response)
    print(translated_text)
    return HttpResponse(translated_text.strip())


def translation(request):
    ret = get_basic_data(request)
    ret['form'] = TranslationForm()
    return render(request, 'embedding/translation.html', ret)


def grammar_async(request):
    original_text = request.POST.get('original_text', '')
    openai_response = run_it_5(original_text, model='text-davinci-003')
    fixed_text = openai_response["choices"][0]["text"]
    record_consumption(
        request, sc.MODEL_TYPES_GRAMMAR, openai_response)
    print(fixed_text)
    return HttpResponse(fixed_text.strip())


def grammar(request):
    ret = get_basic_data(request)
    ret['form'] = GrammarForm()
    return render(request, 'embedding/grammar.html', ret)


def summary_async(request):
    original_text = request.POST.get('original_text', '')
    openai_response = run_it_6(original_text, model='text-davinci-003')
    summary_text = openai_response["choices"][0]["text"]
    record_consumption(
        request, sc.MODEL_TYPES_SUMMARY, openai_response)
    print(summary_text)
    return HttpResponse(summary_text.strip())


def summary(request):
    ret = get_basic_data(request)
    ret['form'] = SummaryForm()
    return render(request, 'embedding/summary.html', ret)


@login_required
def collection(request):
    ret = get_basic_data(request)
    return render(request, 'embedding/collection.html', ret)


def do_login(request, username, password):
    user = auth.authenticate(username=username, password=password)
    if user:
        auth.login(request, user)
        return True
    return False


def do_register(cd):
    with transaction.atomic():
        userProfile = UserProfile.objects.create_user(username=cd.get('username', ''),
                                                      password=cd.get(
                                                          'password', ''),
                                                      )
        userProfile.is_staff = False
        userProfile.is_superuser = False
        userProfile.external_id = load_random_string(20)
        userProfile.save()
    return userProfile


def record_consumption(request, model_type, openai_response, secret=''):
    with transaction.atomic():
        token_amount = openai_response["usage"]["total_tokens"]
        consumption = TokenConsumption.objects.create(user=get_user(request),
                                                      model_type=model_type,
                                                      token_amount=token_amount,
                                                      secret=secret)
        consumption.save()
        if request.user.is_authenticated:
            request.user.left_token -= token_amount
            request.user.used_token += token_amount
            request.user.save()


def get_user(request):
    if request.user.is_authenticated:
        return request.user
    return UserProfile.objects.get(username="default_user")
