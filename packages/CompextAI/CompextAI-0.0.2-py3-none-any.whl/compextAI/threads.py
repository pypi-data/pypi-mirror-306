from src.compextAI.api.api import APIClient

class ThreadExecutionResponse:
    thread_execution_id: str
    thread_id: str

class Thread:
    thread_id: str
    title: str
    metadata: dict

    def __init__(self, thread_id:str, title:str, metadata:dict):
        self.thread_id = thread_id
        self.title = title
        self.metadata = metadata

    def __str__(self):
        return f"Thread(thread_id={self.thread_id}, title={self.title}, metadata={self.metadata})"
    
    def execute(self, client:APIClient, model: str, temperature: float, timeout: int, max_completion_tokens: int, top_p: float, max_output_tokens: int, response_format:any, append_assistant_response:bool=True) -> ThreadExecutionResponse:
        response = client.post(f"/thread/{self.thread_id}/execute", data={
            "model": model,
            "temperature": temperature,
            "timeout": timeout,
            "max_completion_tokens": max_completion_tokens,
            "top_p": top_p,
            "max_output_tokens": max_output_tokens,
            "response_format": response_format,
            "append_assistant_response": append_assistant_response
        })

        status_code: int = response["status"]
        data: dict = response["data"]
        
        if status_code != 200:
            raise Exception(f"Failed to execute thread, status code: {status_code}, response: {data}")
        
        return ThreadExecutionResponse(data["identifier"], self.thread_id)


def get_thread_object_from_dict(data:dict) -> Thread:
    return Thread(data["identifier"], data["title"], data["metadata"])

def list(client:APIClient) -> list[Thread]:
    response = client.get("/thread")
    
    status_code: int = response["status"]
    data: dict = response["data"]
    
    if status_code != 200:
        raise Exception(f"Failed to list threads, status code: {status_code}, response: {data}")
    
    threads = [get_thread_object_from_dict(thread) for thread in data]
    
    return threads

def retrieve(client:APIClient, thread_id:str) -> Thread:
    response = client.get(f"/thread/{thread_id}")
    
    status_code: int = response["status"]
    data: dict = response["data"]
    
    if status_code != 200:
        raise Exception(f"Failed to retrieve thread, status code: {status_code}, response: {data}")
    
    return get_thread_object_from_dict(data)

def create(client:APIClient, title:str=None, metadata:dict={}) -> Thread:
    response = client.post(f"/thread", data={"title": title, "metadata": metadata})

    status_code: int = response["status"]
    data: dict = response["data"]
    
    if status_code != 201:
        raise Exception(f"Failed to create thread, status code: {status_code}, response: {data}")
    
    return get_thread_object_from_dict(data)

def update(client:APIClient, thread_id:str, title:str=None, metadata:dict={}) -> Thread:
    response = client.put(f"/thread/{thread_id}", data={"title": title, "metadata": metadata})

    status_code: int = response["status"]
    data: dict = response["data"]
    
    if status_code != 200:
        raise Exception(f"Failed to update thread, status code: {status_code}, response: {data}")
    
    return get_thread_object_from_dict(data)

def delete(client:APIClient, thread_id:str) -> bool:
    response = client.delete(f"/thread/{thread_id}")
    return response["status"] == 204
