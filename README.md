# Gateway Challenge
The application is live at [https://gateway.lodimup.com/docs](https://gateway.lodimup.com/docs)
- file upload apart from provided sample files are disabled
# System Design
![System Design](./img/system-design.png)
There are two main components in the system:
- **Gateway**: The gateway is the entry point for all incoming requests. It is responsible for routing the requests to the appropriate service.
- **Worker**: The workers are responsible for processing long running requests and returning the response to the gateway. The result, and queue status are stored in Redis.
- **MongoDB**: Is used to store uploaded file metatdata such OCR state, md5 hashes, ownership etc. see `app.services.db.IUploads`
- **Redis**: Is used for caching, primarily for rate limiting. It is also used for task queueing by Celery worker
- **Bucket**: Is used to store the uploaded files.
- **Nginx**: Is used as a reverse proxy to route requests to the gateway, this allows horizontal scaling of Gateway.
- **Pinecone**: Is used to store embeddings and metadata of uploaded files. This is used for similarity search.
- **OpenAI**: Is used to generate embedding vectors and generate netural language response.
## File Storage
when a file is uploaded it is stored in a bucket. The metadata is stored in MongoDB. MD5 hash, id, and user_id is used to identify the file and ownership. These metadata are stored:
id, file extension, md5 hash, file name, url, user_id, ocr_status, schema_version
Since we use MongoDB, schema version is used to track changes in the schema. This is used to ensure that the data is consistent.
## OCR and embedings
OCR and embedding is done by the worker. The worker is responsible for processing long running tasks. The worker will download the file from the bucket, process it and store the result in MongoDB and Pinecone. The worker will also update the metadata in MongoDB with the status of the OCR and embedding. The query embbedding could be persisted.
## Task Queue
Endpoint that request long running tasks will return task_id which can be used to check task status.
## Extraction
Extraction is done by embedding the query and query pinecone for similar embeddings. The result is then converted to natural language for furthur processing.
## System Layers
![System Layers](./img/layers.png)
System is divided into 5 layers:
- **Serializer**: Ensures that the incoming request is in the correct format. It also ensures that the response is in the correct format.
- **Controller**: The controller is responsible for handling the incoming request and sending it to the appropriate service.
- **Service**: The service is responsible for processing the request. It can call other services or the database. Ihis include task queue.
- **Store**: The database is responsible for storing and retrieval of the data.
- **Eternal service**: The external layer is responsible for handling external services like Pinecone, OpenAI etc.
## Security
Endpoints are protected by OAuth bearer token and moving window ratelimiting
The user system is mocked as discussed.
## Logging
- Unhandled exceptions and ERROR level are logged to a file `error.log`
- Operations that are likely to fail is logged using INFO level
example
```
[2024-06-03 15:05:25,917: INFO/ForkPoolWorker-6] HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
[2024-06-03 15:05:27,497: INFO/ForkPoolWorker-6] user_id='czRvNxms7BeqfbBFWhM_r' md5_hash='be5b625ae79945b5257ccc30a321e984' len(metadata)=54 embedding 14 done
[2024-06-03 15:05:27,499: INFO/ForkPoolWorker-6] user_id='czRvNxms7BeqfbBFWhM_r' md5_hash='be5b625ae79945b5257ccc30a321e984' len(metadata)=54 inserting 14 started
[2024-06-03 15:05:31,289: INFO/ForkPoolWorker-6] user_id='czRvNxms7BeqfbBFWhM_r' md5_hash='be5b625ae79945b5257ccc30a321e984' len(metadata)=54 inserting 14 done
[2024-06-03 15:05:31,290: INFO/ForkPoolWorker-6] user_id='czRvNxms7BeqfbBFWhM_r' md5_hash='be5b625ae79945b5257ccc30a321e984' len(metadata)=66 embedding 15 started
```
# Usage
There is a Makefile for your convenience, check it out for more commands.

**Running services locally requires**
- docker
- GNU Make
- .env file with correct values
pinecone database can be initialized with the following command once
```
python scripts/init_pinecone.py
```
then, you can start the services with
```
make compose-up
```
the following services will go online:
- gateway
- worker
- redis
- mongodb

Access the API at `http://localhost:8000/docs`
**Running tests**
```
make compose-test
```
# Local Development in devcontainers
## Development
Requires:
- docker
- vscode with remote containers extension installed
- .env file in the root directory with correct values

A devcontainer is preconfigured for your convenience. Simply `CTRL+SHIFT+P or CMD+SHIFT+P` and select `Remote-Containers: Reopen in Container`.  
You will start working in a docker container with tools and requires dependencies pre-installed. Envronment variable will be reloaded each time you open a new terminal. Makefile is provided for convenience. All database will also be up and running. Check with `docker ps`
Make sure you're in devcontainer by running the following command
```
lsb_release -a
```
Once in container you can start dev server with
```
fastapi dev
```
You should also start a worker if features you're working on requires it
You can force workload to run on fastapi, by setting `CELERY_ALWAYS_EAGER=True`.
```
make worker
```
You can run unit tests locally with
```
cd .. && make test
```
## Releasing
Once your PR is merged, you can release the code to a docker image by running the following command
```
make release
```
A tag will be pushed to the repository, then the image will be built and pushed to the registry. https://github.com/Lodimup/gateway-challenge/pkgs/container/gateway-challenge

## CI/CD
The CI/CD pipeline is setup with Github Actions. It will run tests on each PR and deploy to the registry on PRs and pushes.
- **Linting** is done with `Ruff`
- **Testing** is done with `pytest`
- **Docker** image is built and pushed to the registry when a git tag is pushed.
To deploy to production you can use `docker-compose.yml` as a template


# Endpoints
Automatic documentation, and example usage is available at [http://localhost:8000/docs](http://localhost:8000/docs) locally and [https://gateway.lodimup.com/docs](https://gateway.lodimup.com/docs) on cloud.

Using the api
- start with logging in by clicking Authorize on the top right of https://gateway.lodimup.com/docs
use username: `johndoe` password will be given to you via email. This is essentially obtaining a bearer token
- upload a file using `/upload`
you will receive a response
```json
{
  "files": [
    {
      "id": "DEVAjDtXec-Qao8dKqzw6",
      "ext": "pdf",
      "md5": "99ef153b76c24ee4703f3b9e025bab09",
      "file_name": "東京都建築安全条例.pdf",
      "url": "https://0d7d94b1ba744108db383f...ae0a74eb80508821b4e29a67de56f40f5",
      "user_id": "czRvNxms7BeqfbBFWhM_r"
    }
  ]
}
```
Note down the id and url
- order an ocr using `/ocr` this will mock ocr as well as embed using OpenAI and store result to pinecone
```json
{
  "url": <url> from previous step
}
```
- you will receive a task_id
```json
{
  "task_id": "26ce9f2d-e889-4bc0-93ef-3fccded022e5"
}
```
- check the status of the task using `/ocr/{task_id}/status`
- once the task is complete you can query the file using `/extract`
```json
{
  "query": "第一節の二 適用区域(第一条の二)",
  "file_id": <id from /upload>
}
```
you will receive a response
which chatbot_response is in natural langauge and query_responses are the results

```json
{ 
  "chatbot_response": "The first result is found on page 1 and has the following span: offset 125, length 17. The content of this result is \"第一節の二 適用区域(第一条の二)\".\n\nThe second result is also found on page 1 and has the following span: offset 143, length 17. The content of this result is \"第一節の三 適用除外(第一条の三)\".\n\nThe third result is found on page 2 and has the following span: offset 1126, length 67. The content of this result is \"(昭三五条例四四 · 昭四七条例六一 ·昭六二条例七四 · 平一五条例三二 · 平三〇条 例九七 · 一部改正) 第一節の二 適用区域\".",
  "query_responses": [
    {
      "id": "YrMqzzOzR5cQmEKLNTWW4",
      "score": 0.999999464,
      "metadata": {
        "md5_hash": "99ef153b76c24ee4703f3b9e025bab09",
        "meta": "{\"spans\":[{\"offset\":125,\"length\":17}],\"boundingRegions\":[{\"pageNumber\":1,\"polygon\":[1.4449,3.9391,3.7618,3.9391,3.7618,4.1115,1.4449,4.1115]}],\"content\":\"第一節の二 適用区域(第一条の二)\"}",
        "user_id": "czRvNxms7BeqfbBFWhM_r",
        "model": "text-embedding-3-small"
      }
    },
    {
      "id": "ks7gqK1MQyRvNNfBQmNNE",
      "score": 0.76601392,
      "metadata": {
        "md5_hash": "99ef153b76c24ee4703f3b9e025bab09",
        "meta": "{\"spans\":[{\"offset\":143,\"length\":17}],\"boundingRegions\":[{\"pageNumber\":1,\"polygon\":[1.4601,4.1926,3.7669,4.1926,3.7669,4.3599,1.4601,4.3599]}],\"content\":\"第一節の三 適用除外(第一条の三)\"}",
        "user_id": "czRvNxms7BeqfbBFWhM_r",
        "model": "text-embedding-3-small"
      }
    },
    {
      "id": "nVtnsFJesIsjKI2uXHcYG",
      "score": 0.733506,
      "metadata": {
        "md5_hash": "99ef153b76c24ee4703f3b9e025bab09",
        "meta": "{\"spans\":[{\"offset\":1126,\"length\":67}],\"boundingRegions\":[{\"pageNumber\":2,\"polygon\":[1.7386,5.7237,7.0775,5.7186,7.0782,6.3842,1.7392,6.3892]}],\"content\":\"(昭三五条例四四 · 昭四七条例六一 ·昭六二条例七四 · 平一五条例三二 · 平三〇条 例九七 · 一部改正) 第一節の二 適用区域\"}",
        "user_id": "czRvNxms7BeqfbBFWhM_r",
        "model": "text-embedding-3-small"
      }
    }
  ]
}
```
</details>