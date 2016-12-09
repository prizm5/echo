""" fauxmo_minimal.py - Fabricate.IO

    This is a demo python file showing what can be done with the debounce_handler.
    The handler prints True when you say "Alexa, device on" and False when you say
    "Alexa, device off".

    If you have two or more Echos, it only handles the one that hears you more clearly.
    You can have an Echo per room and not worry about your handlers triggering for
    those other rooms.

    The IP of the triggering Echo is also passed into the act() function, so you can
    do different things based on which Echo triggered the handler.
"""

import logging
import time
import fauxmo

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    # Startup the fauxmo server
    fauxmo.DEBUG = True
    P = fauxmo.poller()
    U = fauxmo.upnp_broadcast_responder()
    U.init_socket()
    P.add(U)

    # Register the device callback as a fauxmo handler
    D = fauxmo.rest_api_handler(
        'http://192.168.0.106/rfoutlet/toggle.php?outletStatus=on&outletId=',
        'http://192.168.0.106/rfoutlet/toggle.php?outletStatus=off&outletId=')
    for trig, port in D.TRIGGERS.items():
        fauxmo.fauxmo(trig, U, P, None, port["port"], D)

    # Loop and poll for incoming Echo requests
    logging.debug("Entering fauxmo polling loop")
    while True:
        try:
            # Allow time for a ctrl-c to stop the process
            P.poll(100)
            time.sleep(0.1)
        except Exception, e:
            logging.critical("Critical exception: " + str(e))
            break
