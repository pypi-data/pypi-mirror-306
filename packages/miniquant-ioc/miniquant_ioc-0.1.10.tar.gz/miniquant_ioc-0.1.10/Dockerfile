FROM python:3.12


ARG MINIQUANT_SRC=/miniquant_src
ARG MINIQUANT_IOC_SRC=/miniquant_ioc_src

ARG MINIQUANT_FROM_PIP=yes
ARG MINIQUANT_IOC_FROM_PIP=yes

RUN useradd -u 9999 cthulhu && mkdir /home/cthulhu && chown cthulhu /home/cthulhu

RUN if [ -d "$MINIQUANT_SRC" ]; then \
        echo "Installing from local directory: $MINIQUANT_SRC" ;\
        pip install "$MINIQUANT_SRC"[test] ;\
    elif [ "$MINIQUANT_FROM_PIP" = "yes" ]; then \
        echo "Installing from pip" ;\
        pip install miniquant-ioc[test] ;\
    else \
        echo "\n  ***\n  *** Source not found at \$MINIQUANT_SRC ($MINIQUANT_SRC). \n  ***\n" ;\
    fi

ENV MINIQUANT_HHLIB=/usr/local/lib/hhlib.so

RUN mkdir -p `dirname $MINIQUANT_HHLIB` && \
    curl -L -o $MINIQUANT_HHLIB \
    https://github.com/PicoQuant/HH400-v3.x-Demos/raw/master/Linux/64bit/library/hhlib.so && \
    chmod a+x $MINIQUANT_HHLIB

RUN apt-get update && apt-get install -y libusb-0.1-4 

RUN if [ -d "$MINIQUANT_IOC_SRC" ]; then \
        echo "Installing from local directory: $MINIQUANT_IOC_SRC" ;\
        pip install "$MINIQUANT_IOC_SRC"[test] ;\
    elif [ "$MINIQUANT_IOC_FROM_PIP" = "yes" ]; then \
        echo "Installing from pip" ;\
        pip install miniquant-ioc[test] ;\
    else \
        echo "\n  ***\n  *** Source not found at \$MINIQUANT_IOC_SRC ($MINIQUANT_IOC_SRC) -- failing build now. \n  ***\n" ;\
        /bin/false ;\
    fi

USER cthulhu


ENTRYPOINT miniquant-ioc
