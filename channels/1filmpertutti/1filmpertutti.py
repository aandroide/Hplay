# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# Canale per 'idcanale nel json'
# By: pincopallo!
# Eventuali crediti se vuoi aggiungerli
# ------------------------------------------------------------
# Rev: 0.2
# Update 12-10-2019
# fix:
# 1. aggiunto pagination e sistemate alcune voci
# 2. modificato problemi in eccezioni
# 3. aggiunta la def check
# 4. modifica alla legenda e altre aggiunte

# Questo vuole solo essere uno scheletro per velocizzare la scrittura di un canale.
# La maggior parte dei canali può essere scritta con il decoratore.
# I commenti sono più un promemoria... che una vera e propria spiegazione!
# Niente di più.
# Ulteriori informazioni sono reperibili nel wiki:
# https://github.com/stream4me/addon/wiki/decoratori
 
"""
    Questi sono commenti per i beta-tester.

    Su questo canale, nella categoria 'Ricerca Globale'
    non saranno presenti le voci 'Aggiungi alla Videoteca'
    e 'Scarica Film'/'Scarica Serie', dunque,
    la loro assenza, nel Test, NON dovrà essere segnalata come ERRORE.

    Novità. Indicare in quale/i sezione/i è presente il canale:
       - Nessuna, film, serie, anime...

    Avvisi:
        - Eventuali avvisi per i tester

    Ulteriori info:

"""
# CANCELLARE Ciò CHE NON SERVE per il canale, lascia il codice commentato ove occorre,
# ma fare PULIZIA quando si è finito di testarlo

# Qui gli import
#import re

# per l'uso dei decoratori, per i log, e funzioni per siti particolari
from core import httptools, support, scrapertools

# in caso di necessità
from core import scrapertools, httptools, servertools, tmdb
#from core.item import Item # per newest
#from lib import unshortenit
from platformcode import config, logger

##### fine import

# se il sito ha un link per ottenere l'url corretto in caso di oscuramenti
# la funzione deve ritornare l'indirizzo corretto, verrà chiamata solo se necessario (link primario irraggiungibile)


# se si usa findhost metti in channels.json l'url del sito che contiene sempre l'ultimo dominio

# se non si usa metti direttamente l'url finale in channels.json
host = "https://filmpertutti.pizza"
headers = [['Referer', host]]

### fine variabili

#### Inizio delle def principali ###

@support.menu
def mainlist(item):
    support.info(item)

    # Ordine delle voci
    # Voce FILM, puoi solo impostare l'url
    film = ['/film/', # url per la voce FILM, se possibile la pagina principale con le ultime novità
        #Voce Menu,['url','action','args',contentType]
        ('Film al Cinema', ['/cinema/', 'peliculas', '']),
        ('Sub Ita', ['/sub-ita/', 'peliculas'])
        ]

    tvshow = ['/serie-tv/',
             ]
    
    generi = [('Generi', ['', 'genres'])]


    """
        Eventuali Menu per voci non contemplate!
    """

    # se questa voce non è presente il menu genera una voce
    # search per ogni voce del menu. Es. Cerca Film...
    search = '' # se alla funzione search non serve altro

    return locals()


# Legenda known_keys per i groups nei patron
# known_keys = ['url', 'title', 'title2', 'season', 'episode', 'thumb', 'quality',
#                'year', 'plot', 'duration', 'genere', 'rating', 'type', 'lang']
# url = link relativo o assoluto alla pagina titolo film/serie
# title = titolo Film/Serie/Anime/Altro
# title2 = titolo dell'episodio Serie/Anime/Altro
# season = stagione in formato numerico
# episode = numero episodio, in formato numerico.
# thumb = linkrealtivo o assoluto alla locandina Film/Serie/Anime/Altro
# quality = qualità indicata del video
# year = anno in formato numerico (4 cifre)
# duration = durata del Film/Serie/Anime/Altro
# genere = genere del Film/Serie/Anime/Altro. Es: avventura, commedia
# rating = punteggio/voto in formato numerico
# type = tipo del video. Es. movie per film o tvshow per le serie. Di solito sono discrimanti usati dal sito
# lang = lingua del video. Es: ITA, Sub-ITA, Sub, SUB ITA.
# AVVERTENZE: Se il titolo è trovato nella ricerca TMDB/TVDB/Altro allora le locandine e altre info non saranno quelle recuperate nel sito.!!!!
@support.scrape
def peliculas(item):
    support.info(item)
    #support.dbg() # decommentare per attivare web_pdb

    #action = 'check'
    #blacklist = ['']
    patron = r'<div class.*?><a href="(?P<url>[^"]+)">\s*<div style="background-image:\s*url\((?P<thumb>[^)]+)\);">\s*<div class="title">(?P<title>[^\(\[<]+)(?:\[(?P<quality1>(HD.*?|SD|TS))\])?'
    #patronBlock = r'<div id="dle-content">(?P<block>.*?)(?=<div class="navigation">)'   #(?P<title>[^\(\[<]+)(?P<title>[^\<]+)     (?:\[(?P<quality1>HD)\])?
    patronNext = '<a href="([^"]+)"\s*>Pagina successiva'
    #pagination = ''
    def itemHook(item):
        if item.quality1:
            item.quality = item.quality1
            item.title += support.typo(item.quality, '_ [] color std')
        if item.lang2:
            item.contentLanguage = item.lang2
            item.title += support.typo(item.lang2, '_ [] color std')
        if item.args == 'novita':
            item.title = item.title

        return item


    debug = True  # True per testare le regex sul sito
    return locals()


@support.scrape
def episodios(item):
    patron = r'data-num="(?P<season>.*?)x(?P<episode>.*?)"\s*data-title="(?P<title>[^"]+)(?P<lang>[sS][uU][bB]\-[iI][tT][aA]+)?".*?<div class="mirrors"(?P<server_links>.*?)<!---'
    action = 'findvideos'
    return locals()


# Questa def è utilizzata per generare i menu del canale
# per genere, per anno, per lettera, per qualità ecc ecc
@support.scrape
def genres(item):
    action = 'peliculas'
    blacklist = ['Serie TV']
    patronMenu = r'<li><a href="(?P<url>[^"]+)">[^>]+>[^>]+>(?P<title>[^<>]+)</a></li>'
    patronBlock = r'</i>.*?Genere</div>(?P<block>.*?)</section>'
    return locals()

############## Fine ordine obbligato
## Def ulteriori

# per quei casi dove il sito non differenzia film e/o serie e/o anime
# e la ricerca porta i titoli mischiati senza poterli distinguere tra loro
# andranno modificate anche le def peliculas e episodios ove occorre

def check(item):
    item.data = httptools.downloadpage(item.url).data
    if 'stagione' in item.data.lower():
        item.contentType = 'tvshow'
        return episodios(item)
    else:
        return findvideos(item)

############## Fondo Pagina
# da adattare al canale
def search(item, text):    
    item.url = "{}/?{}".format(host, support.urlencode({'story': text,'do':'search', 'subaction':'search'}))
    try:
        item.args = 'search'
        return peliculas(item)

    # Continua la ricerca in caso di errore
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


# da adattare al canale
# inserire newest solo se il sito ha la pagina con le ultime novità/aggiunte
# altrimenti NON inserirlo   



# da adattare...
# consultare il wiki sia per support.server che ha vari parametri,
# sia per i siti con hdpass
#support.server(item, data='', itemlist=[], headers='', AutoPlay=True, CheckLinks=True)

def findvideos(item):
    if item.server_links:
        return support.server(item, data = item.server_links)

    video_url = support.match(item.url, patron=r'player[^>]+>[^>]+>.*?src="([^"]+)"').match

    if (video_url == ''):
       return []

    itemlist = [item.clone(action="play", url=srv) for srv in support.match(video_url, patron='<li class="(?:active)?" data-link=\"([^"]+)').matches]
    itemlist = support.server(item,itemlist=itemlist)
    return itemlist