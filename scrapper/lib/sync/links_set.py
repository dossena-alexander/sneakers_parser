from scrapper import settings


def save_links(lst: list):
    with open(settings.PATH.all_links, 'a') as f:
        for link in lst:
            f.write(link)
            f.write('\n')
        

def discard_dup():
    with open(settings.PATH.all_links, 'r') as f:
        all_links = [line.rstrip() for line in f]

    links = set(all_links)
    
    with open(settings.PATH.all_links, 'w') as f:
        for link in links:
            f.write(link)
            f.write('\n')