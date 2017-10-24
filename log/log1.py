'''

loggery tworzą drzewo loggerów,
może być ich wiele
p
ten pierwszy nazywa się root.. i od niego wszystko wychodzi
każdy logger ma coś takiego jak propagate i przekazuje to wyżej do root
propagate jest domyślnie włączone ale można je wyłączyć
propagate powoduje że logger wykorzystuje swoje ustawienia + ustawienia root

jeden logger możem mieć więcej handlerów

wszystkie moduły w pythonie są singleton, tzn. jeśli zaimportujemy go w kilku plikahc
to i tak zostanie wykonany tylko raz

logger można modyfikować - może zapisywać do pliku / bazy danych/ po sieci/
dotatkowo logger może np co godzine tworzyć nowy log albo rozbijać sam duże logi na mniejsze pliki
'''
import logging
import time

logger = logging.getLogger()

logging.basicConfig(level=logging.DEBUG,
                    filename='logi.log',
                    format='%(asctime)s %(relativeCreated)s %(name)s %(levelname)s >>> %(message)s'
                    )

logging.info('info')
logging.debug('to ejst debug coś źle działą')
time.sleep(0.5)
logging.warning('wiadomosc warning')
logging.critical('popsulo sie.')
time.sleep(0.2)
# logging.log(logging.ERROR, 'wiadaomość log 12')
time.sleep(0.2)
logging.warning('Watch out!')  # will print a message to the console
time.sleep(0.2)
logging.info('I told you so')  # will not p
# rint anything
