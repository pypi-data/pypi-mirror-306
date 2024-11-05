#!/usr/bin/python3

from miniquant_ioc.application import init_app
import logging

logger = logging.getLogger("miniquant_ioc")

def main():
    miniApp, cmdline = init_app()
    
    loglevel = getattr(logging, (cmdline.logging or 'INFO').upper(), None)
    logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s", level=loglevel)
    logging.basicConfig(level=loglevel)
    
    miniApp.runIoc()

    
if __name__ == "__main__":
    main()
