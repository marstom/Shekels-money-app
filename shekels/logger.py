import logging

def setup():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(name)s %(levelname)s %(message)s'
    )
    logging.getLogger('werkzeug').setLevel(logging.WARNING)