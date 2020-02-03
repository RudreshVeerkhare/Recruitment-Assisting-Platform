from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from .apps import HomeConfig
from .forms import FilterForm, FileUploadForm
from django.core.files.storage import default_storage



df = HomeConfig.df
lda_model = HomeConfig.lda_model
dictionary = HomeConfig.dictionary


def predict(words):
    other_texts = [words]
    print(other_texts)
    other_corpus = [dictionary.doc2bow(text) for text in other_texts]
    unseen_doc = other_corpus[0]
    vector = lda_model[unseen_doc]
    return vector

def resume(wordslist):
    temp = list()
    for word in wordslist:
        temp.append(word[0].upper() + word[1:].lower())
    print("resume", temp)
    vec = predict(temp)
    topic = max(vec,key=lambda item:item[1])[0]
    filename = list()
    sorted_df = df.sort_values(topic, axis=0, ascending=False)
    filename.append(sorted_df.iloc[0]['filename'])
    for i in range(1, 10):
        if sorted_df.iloc[i][topic] >= 0.6:
            filename.append(sorted_df.iloc[i]['filename'])
    return filename, topic

filename = None
topic = None

def homepage(request):

    form = FilterForm()
    if request.method == 'POST':
        form = FilterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            tags = data.get('tags')

            temp = list()
            for word in tags.split(","):
                word = word.rstrip()
                temp.append(word[0].upper() + word[1:].lower())
            print("homepage", temp)
            global filename
            global topic

            filename, topic = resume(temp)
            return redirect('result')
    else:
        context = {"form" : form}   
    

    return render(request,'home/home.html', context)


def result(request):
    files = list()
    for file in filename:
        files.append((file, default_storage.url(file)))
    return render(request, 'home/result.html', { "topic" : topic, 'files' : files})


def upload_file(request):
    
    if request.method == 'POST':
        file_upload_form = FileUploadForm(request.POST, request.FILES)
        # name = file_upload.cleaned_data.get('name')
        # resume_file = file_upload.cleaned_data.get('resume')
        if file_upload_form.is_valid():
            data = file_upload_form.cleaned_data
            resume = data.get('resume')
            file_name = default_storage.save(resume.name, resume)
            print(file_name)
            print(default_storage.url(file_name))

    else :
        file_upload_form = FileUploadForm()

    context = {
        "form" : file_upload_form,
    }

    return render(request,'home/file_upload.html',context)    