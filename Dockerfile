FROM python:3.12.7
WORKDIR /usr/src/app
RUN pip install annotated-types==0.7.0
RUN pip install anyio==4.8.0
RUN pip install blinker==1.9.0
RUN pip install certifi==2024.8.30
RUN pip install charset-normalizer==3.4.0
RUN pip install click==8.1.7
RUN pip install colorama==0.4.6
RUN pip install distro==1.9.0
RUN pip install Flask==3.1.0
RUN pip install h11==0.14.0
RUN pip install httpcore==1.0.7
RUN pip install httpx==0.28.1
RUN pip install idna==3.10
RUN pip install itsdangerous==2.2.0
RUN pip install Jinja2==3.1.4
RUN pip install jiter==0.8.2
RUN pip install MarkupSafe==3.0.2
RUN pip install notion-client==2.3.0
RUN pip install openai==1.59.8
RUN pip install pydantic==2.10.5
RUN pip install pydantic_core==2.27.2
RUN pip install requests==2.32.3
RUN pip install sniffio==1.3.1
RUN pip install tqdm==4.67.1
RUN pip install typing_extensions==4.12.2
RUN pip install urllib3==2.2.3
RUN pip install Werkzeug==3.1.3
CMD ["flask", "run", "--host=0.0.0.0", "--debug"]