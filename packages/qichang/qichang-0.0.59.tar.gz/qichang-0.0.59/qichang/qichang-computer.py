"""
@author: Qichang Zheng
@email: qichangzheng@uchicago.edu
@date: 2023-11-11
@personal website: http://qichangzheng.net
This is a personal API developed by Qichang Zheng. If you have any questions, please feel free to contact me via email.
"""

import requests
import json
from time import sleep
from ping3 import ping
from bs4 import BeautifulSoup
import os
from tqdm import tqdm
from openai import OpenAI
from func_timeout import func_set_timeout

print("Welcome to Qichang Zheng's package!\n"
      "This package provides a set of APIs to chat with LLMs, download models, and text embedding\n"
      "If you have any questions, please refer to the documentation at https://github.com/QichangZheng/qichang.git,\n"
      "or contact me via email for latest features: qichang.zheng2000@gmail.com / qichangzheng@uchicago.edu")

__version__ = '0.0.54'

app_api_dict = {
    "GPT3.5": 'fastgpt-yRydGHPQX3tPKXPv49BhQOtQNK3BY6VxL',
    'GPT4': 'fastgpt-78OsKUkyugC5WjH4Z3BVE7tDJEh4',
    'stock_api': 'fastgpt-c2LGig65WlHTN3wNKrEkJxzEA',
    'shannon_test1': 'fastgpt-I8yveuOpvtf5NNjCc4feXkscEQGiKxwH3J',
    'Claude3': 'fastgpt-BRWNNH7JOvqbvRi4iDRGElOZRbcd6xOZIOd9BNSeHs8O7GzV5cVHAlEy8jVjLVARC',
    'hongkun-gpt3.5': 'fastgpt-Qc7ApCwWFVb7JQVCurYpsLxifYOdx9x2gpcyj9fufFLTTyKR9b5c89hYTinS',
    'hongkun-gpt4': 'fastgpt-NGB3LLPRCYHv1oA0kP0uuFIasS2D62mebC6HKkc9iOZIGvp9xP2zUqplMfgQ'
}




class LLM_API:
    def __init__(self):
        self.app_api_dict = {
            "GPT3.5": 'fastgpt-AMgpHRPsa4JRErrZz06BzT5zveUhiigHGY1UhUclrytvy1TaoBwS',
            'GPT4': 'fastgpt-5e6SgKLQG7kgDGjydzxSIbFIz0J6LcSE7rWN5MJhMK5aWu0XE5ar',
            'Claude3': 'fastgpt-fLkBU7lnMNS2wMSbPAdfGYdJX89uEWNj40fdrJCNxbFeNQWjj7CMw9YnbIiKuIIy',
            'Gemini': 'fastgpt-4a5RosYVdyMHM6HVIqlXss7cI22IU4ZsSoCa8eoiYTdiVYjC6PkWtNAse7WEUTvVO',
            'stock_api': 'fastgpt-he0hshgxJDA55zIwx7yfZyOeDONUPRtKN1aHqchsjHfmKSSesAGIBOBybhj',
        }
        self.server_dict = {
            'Virginia': '54.159.212.206',
            'Singapore': '20.189.76.86',
        }
        # self.server_dict = {
        #     'Virginia': 'http://dify.qichangzheng.net',
        #     'Singapore': 'http://difynb.qichangzheng.net',
        #     'Local': '127.0.0.1:81'
        # }
        self.base = {
            'Virginia': 'http://dify.qichangzheng.net/v1/chat-messages',
            'Singapore': 'http://difynb.qichangzheng.net/v1/chat-messages',
            'Local': 'http://localhost:81/v1/chat-messages',
            'Dify': 'https://api.dify.ai/v1/chat-messages',
        }
        self.data = {
            "inputs": {},
            "query": '1',
            "response_mode": "blocking",
            "conversation_id": '',
            "user": "abc-123",
        }
        try:
            self.server = self.select_server()
        except:
            print(f'Auto server selection failed, using default server Virginia, '
                  f'you can also select server manually by setting self.server = "Singapore",'
                  f'available servers: {list(self.server_dict.keys())}')
            self.server = 'Virginia'


    def select_server(self):
        # Initialize a dictionary to store ping results
        ping_results = {}

        # Ping each server and store the results
        for server_name, server_ip in self.server_dict.items():
            ping_result = ping(server_ip)
            if ping_result is not None:
                ping_results[server_name] = ping_result

        # Find the server with the lowest ping
        lowest_ping_server = min(ping_results, key=ping_results.get)
        lowest_ping = ping_results[lowest_ping_server]

        # Print the ping results
        print("Ping")
        for server_name, ping_time in ping_results.items():
            print(f"{server_name}: {ping_time:.2f} ms")

        # Print the server with the lowest ping
        print(f"{lowest_ping_server} with lowest ping ({lowest_ping:.2f} ms) selected.")
        return lowest_ping_server


    def fastgpt(self, apikey, message, chatId=None, timeout=60):
        # if app_or_key.startswith('fastgpt-'):
        #     apikey = app_or_key
        # else:
        #     try:
        #         apikey = app_api_dict[app_or_key]
        #     except KeyError:
        #         raise KeyError(f'App {app_or_key} not found, available apps are {list(app_api_dict.keys())}')
        if apikey in app_api_dict:
            apikey = app_api_dict[apikey]
        url = self.fastgpt_server[self.server]
        headers = {
            "Authorization": 'Bearer ' + apikey,
            "Content-Type": "application/json"
        }
        data = {
            "chatId": chatId,
            "stream": False,
            "detail": False,
            "messages": [
                {
                    "content": message,
                    "role": "user"
                }
            ]
        }
        @func_set_timeout(timeout)
        def request():
            response = requests.post(url, headers=headers, json=data).json()['choices'][0]['message']['content']
            return response
        while True:
            try:
                response = request()
                break
            except:
                sleep(3)
        return response

    def dify(self, apikey, message, chatId='', timeout=60):
        # if apikey in app_api_dict:
        #     apikey = app_api_dict[apikey]
        base_url = self.base[self.server]
        headers = {
            "Authorization": 'Bearer ' + apikey,
            "Content-Type": "application/json"
        }
        self.data['query'] = message
        self.data['conversation_id'] = chatId
        # @func_set_timeout(timeout)
        # def request():
        #     res = requests.post(base_url, headers=headers, data=json.dumps(self.data)).json()
        #     response, id = res['answer'], res['conversation_id']
        #     return response, id
        # while True:
        #     try:
        #         response, id = request()
        #         break
        #     except:
        #         sleep(3)
        res = requests.post(base_url, headers=headers, data=json.dumps(self.data)).json()
        response, id = res['answer'], res['conversation_id']
        return response, id

    def openai(self, message, model_name='gpt-4o-mini', apikey=os.environ.get('OPENAI_API_KEY', 'sk-123'), base_url=os.environ.get('OPENAI_API_BASE', 'sk-123'), temperature=0.0):
        client = OpenAI(
            api_key=apikey,
            base_url=base_url,
        )
        messages = [{"role": "user", "content": message}]
        completion = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=temperature
        )
        return completion.choices[0].message.content


    def _parse_qa_from_response(self, response_text):
        response_text = response_text
        if '[Q]:' not in response_text or '[A]:' not in response_text:
            return ['Error'], ['Empty response']
        if response_text.count('[Q]:') != response_text.count('[A]:'):
            return ['Error'], ['Unmatched Q&A']
        response_text = response_text[response_text.find('[Q]:'):]
        q_prefix, a_prefix = "[Q]: ", "[A]: "
        last_updated = None
        questions, answers = [], []

        for line in response_text.split("\n"):
            if line.startswith(q_prefix):
                questions.append(line[len(q_prefix):])
                last_updated = "Q"
            elif line.startswith(a_prefix):
                answers.append(line[len(a_prefix):])
                last_updated = "A"
            else:  # Q or A spread across multiple lines
                assert last_updated is not None, "Parsing error: First line must be a question"
                if last_updated == "Q":
                    questions[-1] += "\n" + line
                else:
                    answers[-1] += "\n" + line
        if len(questions) != len(answers):
            return ['Error'], ['Unmatched Q&A']
        return questions, answers

    def QAJudger(self, question, correct_answer, apikey='app-leu73Kec6zSgVFc0QvZzywAr'):
        base_url = self.base[self.server]
        headers = {
            'Authorization': f'Bearer {apikey}',
            'Content-Type': 'application/json'
        }
        self.data['inputs'] = {'question': question, 'correct_answer': correct_answer}

        response = requests.post(base_url, headers=headers, data=json.dumps(self.data))
        return response.json()['answer'] == 'Correct'

    def QAExtractor(self, url, apikey='app-FfdBP42DWkmhgB1phDRPjTpn'):
        base_url = self.base[self.server]
        headers = {
            'Authorization': f'Bearer {apikey}',
            'Content-Type': 'application/json'
        }
        self.data['inputs'] = {'url': url}

        response = requests.post(base_url, headers=headers, data=json.dumps(self.data))
        return response.json()['answer']

    def AzureQAExtractor(self, url, apikey='app-AgnEAcCe8CDI9HPDyUgXPPeG'):
        base_url = self.base[self.server]
        headers = {
            'Authorization': f'Bearer {apikey}',
            'Content-Type': 'application/json'
        }
        self.data['inputs'] = {'url': url}

        response = requests.post(base_url, headers=headers, data=json.dumps(self.data)).json()['answer']
        return self._parse_qa_from_response(response)

class Model_Downloader:
    def __init__(self):
        self.revision = 'revision_not_found'
        print("You may use the downloader by: Model_Downloader().download(model_name, path)")


    def get_redirect_urls(self, urls):
        result = []
        for url in urls:
            res = requests.get(url, allow_redirects=False)
            result.append('https://cdn.qichangzheng.net' + res.text.split('huggingface.co')[1])
        return result

    def get_file_urls(self, model):
        # Base URL for the model directory
        base_url = f"https://huggingface.qichangzheng.net/{model}/tree/main"

        # Send a GET request to fetch the page content
        response = requests.get(base_url)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')
        self.revision = soup.find('a', attrs={'class': 'rounded border bg-gray-50 px-1.5 text-sm hover:underline dark:border-gray-800 dark:bg-gray-900'})['href'].split('/')[-1]

        names = [i.text for i in soup.find_all('span', attrs={'class': 'truncate group-hover:underline'})]
        # Find all the <a> tags with the 'download' attribute
        direct_urls = []
        redirect_urls = []
        for tag in soup.find_all('a', attrs={'title': 'Download file'}):
            url = 'https://huggingface.qichangzheng.net' + tag['href']
            if tag.find('svg').next_sibling.strip() == '':
                direct_urls.append(url)
            else:
                direct_urls.append(self.get_redirect_urls([url])[0])
        return dict(zip(names, direct_urls))

    def download(self, model_name, path):
        # Ensure the download directory exists
        print('Fetching download links...')
        urls = self.get_file_urls(model_name)
        path = path + '/models--' + '--'.join(model_name.split('/')) + f'/snapshots/{self.revision}'
        print(f'Model will be saved at {path}')
        if not os.path.exists(path):
            os.makedirs(path)

        for filename, url in tqdm(urls.items(), desc="Downloading files", unit="file"):
            # Extract the file name from the URL
            # filename = url.split('/')[-1].split('?')[0]  # Assumes the URL ends with filename?download=true
            full_path = os.path.join(path, filename)

            # Stream the download to avoid using too much memory
            response = requests.get(url, stream=True)

            # Check if the request was successful
            if response.status_code == 200:
                # Open the file to write as binary - 'wb'
                with open(full_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:  # filter out keep-alive new chunks
                            f.write(chunk)
            else:
                print(f"Failed to download {url}")

class Embedder:
    def __init__(self):
        try:
            self.api_key = os.environ['OPENAI_API_KEY']
        except:
            raise KeyError(
                'OpenAI API key not found, please set the environment variable OPENAI_API_KEY by os.environ["OPENAI_API_KEY"] = "your_api_key"')
        self.client = OpenAI(api_key=self.api_key, base_url="https://openai.qichangzheng.net/v1")
        pass

    def embedding(self, text):
        text = text.replace("\n", " ")
        return self.client.embeddings.create(input=[text], model="text-embedding-ada-002").data[0].embedding
