# Base image
FROM python:3.11-slim

LABEL maintainer="Stefan Bogdanel <stefan@izdrail.com>"

# Install OS dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl nodejs gcc g++ make procps libssl-dev npm \
    htop mlocate supervisor software-properties-common git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*



RUN npm install -g vite

   
# Upgrade pip and install supervisord and pipx
RUN pip install --no-cache-dir --upgrade pip \
    && pip install pipx

# Clone SpiderFoot and install its dependencies
WORKDIR /home
RUN git clone https://github.com/izdrail/spiderfoot.git
WORKDIR /home/spiderfoot
RUN pip install -r requirements.txt

WORKDIR /home
RUN git clone https://github.com/izdrail/bbot.izdrail.com.git
RUN pipx install bbot

# Clone, build, and install Skraper
# RUN git clone https://github.com/izdrail/skraper.izdrail.com.git
# WORKDIR /home/skraper.izdrail.com
# RUN ./mvnw clean package -DskipTests=true \
#     && mkdir -p /usr/local/skraper \
#     && cp cli/target/cli.jar /usr/local/skraper/ \
#     && echo '#!/bin/bash\njava -jar /usr/local/skraper/cli.jar "$@"' > /usr/local/bin/skraper \
#     && chmod +x /usr/local/bin/skraper

# Set up FastAPI app
WORKDIR /home/app
COPY app . 

RUN pip install --no-cache-dir --upgrade -r requirements.txt \
    && pip install fastapi-versioning pymupdf4llm python-multipart yake tls_client uvicorn litellm asent spacyfishing\
    && python3 -m nltk.downloader -d /usr/local/share/nltk_data wordnet punkt stopwords vader_lexicon \
    && python3 -m spacy download en_core_web_md \
    && python3 -m textblob.download_corpora

# Clean up
RUN apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /home/osint/app/.git \
    && updatedb

# Copy Supervisor configuration
COPY docker/supervisord.conf /etc/supervisord.conf
#COPY doker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf


# FRONTEND - TODO: Make this work
WORKDIR /home/frontend
COPY frontend /home/frontend/

RUN npm install
RUN npm run build
#Now copy to 



# Expose application ports
EXPOSE 10000 10001 10002 
# Run application
ENTRYPOINT ["supervisord", "-c", "/etc/supervisord.conf", "-n"]

