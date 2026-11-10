```mermaid
graph TD
    requests["requests"] --> charsetnormalizer["charset-normalizer"]
    requests["requests"] --> idna["idna"]
    requests["requests"] --> urllib3["urllib3"]
    requests["requests"] --> certifi["certifi"]
    requests["requests"] --> pysocks["pysocks"]
    requests["requests"] --> chardet["chardet"]
    
    idna["idna"] --> ruff["ruff"]
    idna["idna"] --> mypy["mypy"]
    idna["idna"] --> ty["ty"]
    idna["idna"] --> pytest["pytest"]
    idna["idna"] --> hypothesis["hypothesis"]
    idna["idna"] --> coverage["coverage"]
    
    urllib3["urllib3"] --> brotli["brotli"]
    urllib3["urllib3"] --> brotlicffi["brotlicffi"]
    urllib3["urllib3"] --> h2["h2"]
    urllib3["urllib3"] --> pysocks["pysocks"]
    urllib3["urllib3"] --> backportszstd["backports-zstd"]
