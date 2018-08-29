#! python3

import sys
import contextlib
import requests
import bs4
import pyperclip

url_base = 'http://esv.literalword.com/'


# url_sample = 'http://esv.literalword.com/?q=ps+18%3A16-19'


def main():
    if not (len(sys.argv) > 1):
        print('You must pass in a Scripture reference.')
        exit()

    reference = ' '.join(sys.argv[1:])
    url = url_from_reference(reference)

    # print(url)

    raw_html = simple_get(url)
    if raw_html:
        soup = bs4.BeautifulSoup(raw_html, 'lxml')
    else:
        print('{} : Unable to retrieve HTML.'.format(url))

    # print(raw_html)
    # exit()

    scripture_text = scripture_text_from_soup(soup)
    pyperclip.copy(scripture_text)
    print(scripture_text)


def scripture_text_from_soup(soup):
    # tags = soup.find_all('span', class_=['bV', 'bPt'])
    scripture_reference = str(soup.find('p', class_='bTitle').string).title()

    tags = soup.find_all('span', class_='bV')

    text_needed = []

    for tag in tags:
        dn_tags = tag.find_all('span', class_='divine-name')
        for t in dn_tags:
            t.string = t.string.upper()

        child_tags_needed = [t for t in tag if t not in
                             tag.find_all('span', class_=
                             ['bVN', 'bVNpt', 'bCh', 'bChpoetry', 'revspsp'])]

        has_bPt = '<span class="bPt">' in str(child_tags_needed)

        single_verse = []

        for c in child_tags_needed:
            # print(c)
            if isinstance(c, bs4.element.Tag):
                sub_string = ''.join([str(gc.string) for gc in c if gc.string])
            else:
                sub_string = str(c.string)
            single_verse.append(sub_string)

        if has_bPt:
            text_needed.append(' '.join(single_verse))
        else:
            text_needed.append(''.join(single_verse))

    text = ' '.join(text_needed).strip()
    text = text.replace('  ', ' ')
    text = '{}  [{} ESV]'.format(text, scripture_reference)

    return text


def url_from_reference(reference):
    ref_string = reference.replace(' ', '+')
    ref_string = ref_string.replace(':', '%3A')

    url = url_base + '?q=' + ref_string
    url = url.strip()

    return url


def simple_get(url):
    """
    Obtained original version of this code, June 2018, from:
    https://realpython.com/python-web-scraping-practical-introduction/
    Made my own modifications. -kshatto

    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """

    try:
        with contextlib.closing(requests.get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except requests.RequestException as e:
        print('Error during request to {} : {}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML.
    False otherwise.
    """

    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


if __name__ == '__main__':
    main()
