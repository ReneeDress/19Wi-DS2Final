from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import os
import re
import requests

# Create your views here.

# 解决前端post请求 csrf问题
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def api_test(request):
    # #print(request)
    # #print(request.method)
    context = {}
    context['hello'] = 'Hello World!'
    context['world'] = 'Sad!'
    context['word'] = 'Success?'
    # return render(request, 'index.html', context)
    #return render(request, 'index.html', context)
    # return JsonResponse({"message": "This is a Test."})
    print(context)
    return JsonResponse(context)

@csrf_exempt
def api_init(request):
    print('init')
    filelist = os.listdir("./backend/Post/")
    d = dict()
    wl = []
    db = open("database.txt", "w")
    for fn in filelist:
        process_post(fn, db, wl, d)
    db.close()
    sortedwl = open("sortedwl.txt", "w")
    process_word(wl, sortedwl)
    sortedwl.close()
    for w in wl:
        d[w] = list(set(d[w]))
    #print(d)
    return JsonResponse(d)

@csrf_exempt
def api_input(request):
    print('input')
    # print(request.POST)
    # print(list(request.POST))
    return HttpResponse(request)


@csrf_exempt
def api_dict(request):
    print('dict')
    w = list(request.POST)
    print(w)
    word = w[0]
    detail = word_meaning(word)
    detail2 = word_synonym(word)
    detail.update(detail2)
    print(detail)
    return JsonResponse(detail)


@csrf_exempt
def api_resplit(request):
    print('resplit')
    # print(request.POST)
    dns = dict(request.POST)
    # print(dns)
    e = []
    for i in range(0, len(dns) - 1):
        i = str(i)
        # print(dns[i])
        ds = dns['d[' + i + ']'][0].split("======")
        if len(dns['word'][0]) == 1:
            word = " " + dns['word'][0] + " "
            highlight = "<span class=\"highlight\">" + word + "</span>"
            ds[0] = ds[0].replace(word, highlight)
            highlight = "<span class=\"highlight\">" + str.upper(word) + "</span>"
            ds[0] = ds[0].replace(str.upper(word), highlight)
            highlight = "<span class=\"highlight\">" + str.capitalize(word) + "</span>"
            ds[0] = ds[0].replace(str.capitalize(word), highlight)
        else:
            word = "" + dns['word'][0] + ""
            highlight = "<span class=\"highlight\">" + word + "</span>"
            ds[0] = ds[0].replace(word, highlight)
            highlight = "<span class=\"highlight\">" + str.upper(word) + "</span>"
            ds[0] = ds[0].replace(str.upper(word), highlight)
            highlight = "<span class=\"highlight\">" + str.capitalize(word) + "</span>"
            ds[0] = ds[0].replace(str.capitalize(word), highlight)
        print(ds)
        e.append(ds)
    # print(list(e))
    js = {'example': e}
    return JsonResponse(js)


def process_post(filename, database, wordlist, dict):
    file = open("./backend/Post/" + filename, "r")
    title = file.readline()
    raw = file.read()
    #print(title)
    raw = raw.replace(". ", ".")
    raw = raw.replace("? ", "?")
    raw = raw.replace("! ", "!")
    sentences = re.split('[.?!\n]', raw)
    sentences = list(filter(None, sentences))
    for s in range(0, len(sentences)):
        if len(sentences[s]) > 100:
            sentence = sentences[s]
            words = re.split('[ ,;:\'’‘()\[\]{}/1234567890"“@]', sentence)
            words = list(filter(None, words))
            if sentences[s][len(sentences[s])-1] == ':':
                sentences[s] = sentences[s][0:len(sentences[s])-1]
            sentences[s] += '. ======' + title
            sentence = sentences[s]
            for w in range(0, len(words)):
                if words[w][0] != '-' and words[w][0] != '+' and words[w][0] != '$' and words[w][0] != '&' and words[w][0] != '%':
                    word = str.lower(words[w])
                    wordlist.append(word)
                    if word in dict:
                        dict[word].append(sentence)
                    else:
                        dict[word] = []
                        dict[word].append(sentence)
            database.write(sentences[s])
            #print(sentences[s])
    return


def process_word(unsortedwl, wordlist):
    unsortedwl = list(set(unsortedwl))
    sortedwl = sorted(unsortedwl)
    for w in range(0, len(sortedwl)):
        if w != 0:
            writeword = '\n' + sortedwl[w]
        else:
            writeword = sortedwl[w]
        wordlist.write(writeword)
    return


def word_meaning(word):
    url = "http://www.iciba.com/word?w=" + word
    print(url)
    detail = {'phonetic': [], 'meaning': [], 'exchange': [], 'synonym': [], 'antonym': []}
    response = requests.get(url)
    phoneticwhole = re.findall('<ul class="Mean_symbols__5dQX7">(.*?)</ul>', response.text)
    img = re.findall('<img (.*?)>', phoneticwhole[0])
    phonetic = re.findall('<li>(.*?)</li>', phoneticwhole[0])
    if img:
        img = "<img " + img[0] + ">"
    else:
        img = ""
    if phonetic:
        for i in range(0, len(phonetic)):
            phonetic[i] = phonetic[i].replace("<!-- -->", "")
            phonetic[i] = phonetic[i].replace("&#x27;", "'")
            phonetic[i] = phonetic[i].replace(img, "")
            print(phonetic[i], end=" ")
            detail['phonetic'].append(phonetic[i])
    print('\r')
    meanwhole = re.findall('<ul class="Mean_part__1RA2V">(.*?)</ul>', response.text)
    meanline = re.findall('<li>(.*?)</li>', meanwhole[0])
    pos = []
    meaning = []
    for i in range(0, len(meanline)):
        print(meanline[i])
        posi = re.findall('<i>(.*?)</i>', meanline[i])
        if posi:
            pos.append(posi[0])
        else:
            pos.append(' ')
        meaning.append(re.findall('<span>(.*?)<!-- -->; </span>', meanline[i]))
    for i in range(0, len(pos)):
        pos[i] = pos[i].replace("&amp;", "&")
        print(pos[i], end=' ')
        posmeaning = pos[i] + ' '
        for j in range(0, len(meaning[i])):
            print(meaning[i][j], end='; ')
            posmeaning += meaning[i][j] + '; '
        if i != len(pos) - 1:
            print('\r')
        else:
            print('\n')
        detail['meaning'].append(posmeaning)
    exchange = re.findall('<ul class="Morphology_morphology__3g6fA">(.*?)</ul>', response.text)
    if len(exchange) != 0:
        print('词形变化')
        exchangeli = re.findall('<li>(.*?)</li>', exchange[0])
        for i in range(0, len(exchangeli)):
            type = re.findall('(.*?)<!-- -->:', exchangeli[i])
            change = re.findall('href="/word\?w=(.*?)"', exchangeli[i])
            print(type[0] + "：" + change[0], end='   ')
            detail['exchange'].append(type[0] + "：" + change[0])
        print('\n')
    return detail


def word_synonym(word):
    url = "http://www.iciba.com/word?w=" + word
    response = requests.get(url)
    detail = {'synonym': [], 'antonym': []}
    synonymdiv = re.findall(
        '<li><div class="FoldBox_fold__1GZ_2"><h3 class="FoldBox_title__2YVcn">同义词</h3><div class="FoldBox_content__2q-bU"><div class="Synonym_synonym__1Pp8x">(.*?)</div></div></div></li>',
        response.text)
    if synonymdiv:
        print("同义词")
        for i in range(0, len(synonymdiv)):
            synonymli = re.findall('<div class="Synonym_mean__1vKzy">(.*?)</div>', synonymdiv[i])
            for j in range(0, len(synonymli)):
                synoposmean = ''
                synopos = re.findall('<i>(.*?)</i>', synonymli[j])
                if synopos:
                    synopos[0] = synopos[0].replace("&amp;", "&")
                    print(synopos[0], end=' ')
                    synoposmean += synopos[0] + ' '
                synomean = re.findall('<span>(.*?)</span>', synonymli[j])
                for m in range(0, len(synomean)):
                    print(synomean[m])
                    synoposmean += synomean[m]
                synowl = ''
                synonymwl = re.findall('<p>(.*?)</p>', synonymli[j])
                for k in range(0, len(synonymwl)):
                    synonymw = re.findall('href="/word\?w=(.*?)"', synonymwl[k])
                    for w in range(0, len(synonymw)):
                        print(synonymw[w], end=' ')
                        synowl += synonymw[w] + ' '
                    print('\r')
                detail['synonym'].append([synoposmean, synowl])

    antonymdiv = re.findall(
        '<li><div class="FoldBox_fold__1GZ_2"><h3 class="FoldBox_title__2YVcn">反义词</h3><div class="FoldBox_content__2q-bU"><div class="Synonym_synonym__1Pp8x">(.*?)</div></div></div></li>',
        response.text)
    if antonymdiv:
        print("\n反义词")
        for i in range(0, len(antonymdiv)):
            antonymli = re.findall('<div class="Synonym_mean__1vKzy">(.*?)</div>', antonymdiv[i])
            for j in range(0, len(antonymli)):
                antoposmean = ''
                antopos = re.findall('<i>(.*?)</i>', antonymli[j])
                if antopos:
                    antopos[0] = antopos[0].replace("&amp;", "&")
                    print(antopos[0], end=' ')
                    antoposmean += antopos[0] + ' '
                antomean = re.findall('<span>(.*?)</span>', antonymli[j])
                for m in range(0, len(antomean)):
                    print(antomean[m])
                    antoposmean += antomean[m]
                antowl = ''
                antonymwl = re.findall('<p>(.*?)</p>', antonymli[j])
                for k in range(0, len(antonymwl)):
                    antonymw = re.findall('href="/word\?w=(.*?)"', antonymwl[k])
                    for w in range(0, len(antonymw)):
                        print(antonymw[w], end=' ')
                        antowl += antonymw[w] + ' '
                    print('\r')
                detail['antonym'].append([antoposmean, antowl])
    if not (synonymdiv or antonymdiv):
        print('无同义词反义词。')
    return detail