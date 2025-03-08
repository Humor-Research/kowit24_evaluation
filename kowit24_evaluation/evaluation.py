import re
import pymorphy3


morph = pymorphy3.MorphAnalyzer()


def parse_one_annotation(annot):

    searcheable_elements = list()
    searcheable_links = list()

    if isinstance(annot["reference_string"], list):
        for i in range(len(annot["reference_string"])):
            searcheable_elements.append(
                annot["reference_string"][i]
            )
    elif isinstance(annot["reference_string"], str) and annot["reference_string"].strip() != "":
        searcheable_elements.append(
                annot["reference_string"]
        )

    if isinstance(annot["reference_url"], list):
        for i in range(len(annot["reference_url"])):
            searcheable_links.append(
                annot["reference_url"][i]
            )
    elif isinstance(annot["reference_url"], str) and annot["reference_url"].strip() != "":
        searcheable_links.append(
                annot["reference_url"]
        )

    return searcheable_elements, searcheable_links

def extract_searcheable_elements_and_links(annotations):

    searcheable_elements = list()
    searcheable_links = list()

    for annot in annotations:
        if isinstance(annot, dict):
            tmp_elements, tmp_links = parse_one_annotation(annot)
            searcheable_elements.extend(
                tmp_elements
            )
            searcheable_links.extend(
                tmp_links
            )
        elif isinstance(annot, list):
            for single_annot in annot:
                tmp_elements, tmp_links = parse_one_annotation(single_annot)
                searcheable_elements.extend(
                    tmp_elements
                )
                searcheable_links.extend(
                    tmp_links
                )
    
    return searcheable_elements, searcheable_links


def tokenize(text: str):
    return " ".join(re.findall(r'\b\w+\b', text.lower()))


def lemmatize(tokens: str):
    tokens = tokens.split(" ")
    morph = pymorphy3.MorphAnalyzer()
    return " ".join([morph.parse(token)[0].normal_form for token in tokens])


def normalize_text(text):
    tokens = tokenize(text)
    lemmas = lemmatize(tokens)
    return " ".join(lemmas)


def normalize_link(link):
    if "https://ru.wikipedia.org" in link:
        link = link.split("https://ru.wikipedia.org/wiki/")[1]
    elif "https://ru.wiktionary.org" in link:
        link = link.split("https://ru.wiktionary.org/wiki/")[1]
    
    if "#" in link:
        position = link.find("#")
        link = link[:position]
    
    link = re.sub(r'\(.*?\)', '', link).strip()

    link = re.sub(r'[^a-zA-Zа-яА-ЯёЁ]', ' ', link)
    link = re.sub(r'\s+', ' ', link).strip()

    return link.lower()


def check_interpretation(annotation: dict, text: str) -> bool:
    
    searcheable_elements, searcheable_links = extract_searcheable_elements_and_links(annotation)
    
    searcheable_elements = [str.lower(t) for t in searcheable_elements]
    searcheable_links = [normalize_link(t) for t in searcheable_links]
    searcheable_links = [str.lower(t) for t in searcheable_links]

    searcheable_elements_tokenized = [tokenize(t) for t in searcheable_elements]
    searcheable_links_tokenized = [tokenize(t) for t in searcheable_links]

    searcheable_elements_normalized = [lemmatize(t) for t in searcheable_elements_tokenized]
    searcheable_links_normalized = [lemmatize(t) for t in searcheable_links_tokenized]

    all_searcheable_elements = list()
    all_searcheable_elements.extend(searcheable_links)
    all_searcheable_elements.extend(searcheable_links_tokenized)
    all_searcheable_elements.extend(searcheable_links_normalized)

    all_searcheable_elements.extend(searcheable_elements)
    all_searcheable_elements.extend(searcheable_elements_tokenized)
    all_searcheable_elements.extend(searcheable_elements_normalized)


    all_texts = list()

    all_texts.append(
        str.lower(text)
    )

    all_texts.append(
        tokenize(str.lower(text))
    )

    all_texts.append(
        lemmatize(tokenize(str.lower(text)))
    )

    results = list()
    results.append(-1)

    for elem in all_searcheable_elements:
        for text in all_texts:
            results.append(
                str.find(text, elem)
            )
    
    results = max(results)
    results = True if results >= 0 else False

    return results
    