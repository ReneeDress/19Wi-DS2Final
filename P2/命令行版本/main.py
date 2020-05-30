import os
import re
import requests


def process_post(filename, database, wordlist, dict):
    file = open("Post/" + filename, "r")
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
            sentences[s] += '. ' + '======' + title
            sentence = sentences[s]
            for w in range(0, len(words)):
                if len(words[w]) > 1 and words[w][0] != '-':
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
    print('\r')
    meanwhole = re.findall('<ul class="Mean_part__1RA2V">(.*?)</ul>', response.text)
    meanline = re.findall('<li>(.*?)</li>', meanwhole[0])
    pos = []
    meaning = []
    for i in range(0, len(meanline)):
        posi = re.findall('<i>(.*?)</i>', meanline[i])
        if posi:
            pos.append(posi[0])
        else:
            pos.append(' ')
        meaning.append(re.findall('<span>(.*?)<!-- -->; </span>', meanline[i]))
    for i in range(0, len(pos)):
        pos[i] = pos[i].replace("&amp;", "&")
        print(pos[i], end=' ')
        for j in range(0, len(meaning[i])):
            print(meaning[i][j], end='; ')
        if i != len(pos) - 1:
            print('\r')
        else:
            print('\n')
    exchange = re.findall('<ul class="Morphology_morphology__3g6fA">(.*?)</ul>', response.text)
    if len(exchange) != 0:
        print('词形变化')
        exchangeli = re.findall('<li>(.*?)</li>', exchange[0])
        for i in range(0, len(exchangeli)):
            type = re.findall('(.*?)<!-- -->:', exchangeli[i])
            change = re.findall('href="/word\?w=(.*?)"', exchangeli[i])
            print(type[0] + "：" + change[0], end='   ')
        print('\n')
    return


def word_synonym(word):
    url = "http://www.iciba.com/word?w=" + word
    response = requests.get(url)

    synonymdiv = re.findall(
        '<li><div class="FoldBox_fold__1GZ_2"><h3 class="FoldBox_title__2YVcn">同义词</h3><div class="FoldBox_content__2q-bU"><div class="Synonym_synonym__1Pp8x">(.*?)</div></div></div></li>',
        response.text)
    if synonymdiv:
        print("同义词")
        for i in range(0, len(synonymdiv)):
            synonymli = re.findall('<div class="Synonym_mean__1vKzy">(.*?)</div>', synonymdiv[i])
            for j in range(0, len(synonymli)):
                synopos = re.findall('<i>(.*?)</i>', synonymli[j])
                if synopos:
                    synopos[0] = synopos[0].replace("&amp;", "&")
                    print(synopos[0], end=' ')
                synomean = re.findall('<span>(.*?)</span>', synonymli[j])
                for m in range(0, len(synomean)):
                    print(synomean[m])
                synonymwl = re.findall('<p>(.*?)</p>', synonymli[j])
                for k in range(0, len(synonymwl)):
                    synonymw = re.findall('href="/word\?w=(.*?)"', synonymwl[k])
                    for w in range(0, len(synonymw)):
                        print(synonymw[w], end=' ')
                    print('\r')

    antonymdiv = re.findall(
        '<li><div class="FoldBox_fold__1GZ_2"><h3 class="FoldBox_title__2YVcn">反义词</h3><div class="FoldBox_content__2q-bU"><div class="Synonym_synonym__1Pp8x">(.*?)</div></div></div></li>',
        response.text)
    if antonymdiv:
        print("\n反义词")
        for i in range(0, len(antonymdiv)):
            antonymli = re.findall('<div class="Synonym_mean__1vKzy">(.*?)</div>', antonymdiv[i])
            for j in range(0, len(antonymli)):
                antopos = re.findall('<i>(.*?)</i>', antonymli[j])
                if antopos:
                    antopos[0] = antopos[0].replace("&amp;", "&")
                    print(antopos[0], end=' ')
                antomean = re.findall('<span>(.*?)</span>', antonymli[j])
                for m in range(0, len(antomean)):
                    print(antomean[m])
                antonymwl = re.findall('<p>(.*?)</p>', antonymli[j])
                for k in range(0, len(antonymwl)):
                    antonymw = re.findall('href="/word\?w=(.*?)"', antonymwl[k])
                    for w in range(0, len(antonymw)):
                        print(antonymw[w], end=' ')
                    print('\r')
    if not (synonymdiv or antonymdiv):
        print('无同义词反义词。')
    return


if __name__ == '__main__':
    filelist = os.listdir("Post")
    d = dict()
    wl = []
    db = open("database.txt", "w")
    for fn in filelist:
        process_post(fn, db, wl, d)
    db.close()
    sortedwl = open("sortedwl.txt", "w")
    process_word(wl, sortedwl)
    sortedwl.close()
    #print(wl)
    for w in wl:
        d[w] = list(set(d[w]))
    var = 1
    MIN = 5
    while var == 1:
        print('欢迎来到计算机英语句句搜。\n作者：林艺珺 18120189\n输入单词进行查询。输入">>>"退出。\n')
        target = input()
        if target in d:
            word_meaning(target)
            print('例句')
            if len(d[target]) < MIN:
                for i in range(0, len(d[target])):
                    print(d[target][i])
            else:
                for i in range(0, MIN):
                    print(d[target][i])
            print('是否查看同义词及反义词？(y/n)', end=' ')
            while var == 1:
                yon = input()
                if yon == 'y':
                    word_synonym(target)
                    break
                elif yon == 'n':
                    break
                else:
                    print('请输入y/n。')
                    continue
            print('\n========' + target + '查询完毕。========\n')
        elif target == '>>>':
            break
        else:
            print("词库中不存在此单词例句。\n")