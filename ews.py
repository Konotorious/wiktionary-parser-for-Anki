# -*- coding: utf-8 -*-

from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

"""
filename = "anki_import.txt"
f = open(filename, "w")

f.write("    "+"\n")
f.close()
"""

# wiktionary base url and urls of category pages to parse the contents of
base_url = "https://en.wiktionary.org"
categories = {
    "Spanish":"/wiki/Category:Esperanto_terms_derived_from_Spanish",
    "French":"/wiki/Category:Esperanto_terms_derived_from_French"}
baseFileName = "AnkiEsperantoWordsFrom"


def getTermsLists(url, base_url=base_url, recursive = 0):
    """
    a generator of wiktionary pages urls
    """
    lis = [] # list of tags of HTML lists, with each entry as a list element (li)
    termsHeader = reachCategoryPagesListHeader(url, base_url)
    pointer = termsHeader
    counter = 0
    while True:
        try:
            if not pointer.findAll("li"):
                pointer = pointer.next_sibling
                counter += 1
                continue
            break
        except:
            pointer = pointer.next_sibling
    lis.append(pointer)

    if counter == 2:
        return lis
    elif counter == 4:
        nextPageUrl = getNextPage(getPageSoup(url))
        nextLis = getTermsLists(nextPageUrl, recursive = 1)
        lis = lis + nextLis
        return lis
    elif counter == 3:
        if recursive == 0:
            nextPageUrl = getNextPage(getPageSoup(url))
            nextLis = getTermsLists(nextPageUrl, recursive = 1)
            lis = lis + nextLis
            return lis
        else:
            return lis


def getNextPage(pageSoup):
    for a in pageSoup.findAll("a"):
        if a.text == "next page":
            urlContainer = a
            break
    nextPageUrl = urlContainer["href"]
    return nextPageUrl

def reachCategoryPagesListHeader(url, base_url=base_url):

    page_soup = getPageSoup(url, base_url=base_url)

    for title in page_soup.findAll("h2"):
        if "Pages in category" in title.text:
            termsHeader = title
    return termsHeader


def getPageSoup(url, base_url=base_url):

    # openning connection, grabbing the page
    uClient= uReq(base_url+url)
    page_html = uClient.read()
    uClient.close()
    
    # html parsing
    page_soup = soup(page_html, "html.parser")

    return page_soup



def wikiPageScraper(url, base_url=base_url):
    page_soup = getPageSoup(url)
    try:
        eo_title = page_soup.find(id="Esperanto").parent
    except:
        return None
    derivedTermUrls = []
    word_pos = None
    word_element = None
    word = None
    meaning = None
    etymology = " "
    for sibling in eo_title.next_siblings:
        if sibling.name == 'h2':
            break
        try:
            if "Etymology" in sibling.span["id"]:
                etymology = sibling.next_sibling.next_sibling.text
        except:
            continue
    for pos in ["Verb", "Noun", "Adjective", "Adverb", "Interjection", "Preposition", "Proper Noun"]:
        for sibling in eo_title.next_siblings:
            if sibling.name == 'h2':
                break
            try:
                if "Derived_terms" in sibling.span["id"]:
                    for sibling_word in sibling.next_sibling.next_sibling.findAll("li"):
                        derivedTermUrls.append(sibling_word.a["href"])
                    break
            except:
                continue

        for sibling in eo_title.next_siblings:
            if sibling.name == 'h2':
                break
            try:
                if pos in sibling.span["id"]:
                    word_pos = pos
                    word_element = sibling.next_sibling.next_sibling
                    word = word_element.strong.text
                    meaning = word_element.next_sibling.next_sibling.text
                    break
            except:
                continue
    return (word, word_pos, meaning, etymology), derivedTermUrls
"""
    try: 
        return (word, word_pos, meaning, etymology), derivedTermUrls
    except:
        try:
            return (None, None, None, None), derivedTermUrls
        except:
            print(url)
"""

def main():
    urlToFile.scraped_words= set()
    for cat in categories:
        filename = baseFileName+cat+".txt"
        f = open(filename, 'w', encoding='utf-8')
        lis = getTermsLists(categories[cat])
        for i in lis:
            for li in i.findAll("li"):
                term_url = li.a["href"]
                urlToFile(term_url, f)
        f.close()

                                          
def urlToFile(term_url, f):
    if not term_url.rsplit("/",1)[1] in urlToFile.scraped_words:
        scraping = wikiPageScraper(term_url)
        urlToFile.scraped_words.add(term_url.rsplit("/",1)[1])
        if scraping:
            parseParserOutput(scraping, f)

def parseParserOutput(output, f):
    content, derivedTermUrls = output
    if content[0]:
        writeLineToFile(content, f)
    if derivedTermUrls:
        for termUrl in derivedTermUrls:
            if not "redlink=1" in termUrl:
                urlToFile(termUrl, f)
        
def writeLineToFile(_input_, f):
    line = u""
    if _input_[0]: # a word of the chosen categories (e.g. not a preposition)
        for i in _input_: # Discard examples, as well as additional definitions:
            oneLine = str(i).split("\n")[0] 
            line = line+oneLine+" \t"
        line = line+" \n"
        #print(line)
        f.write(line)

if __name__ == "__main__":
    main()
