import re
import requests
import json
import time
from typing import Optional, Dict, Any, List

class ReadPDFs:
    def __init__(self, api_key: str, base_url: str = "https://backend.readpdfs.com"):
        self.api_key = api_key
        self.base_url = base_url

    def _poll_task_status(self, task_id: str, timeout: int = 300, interval: int = 2) -> Dict[str, Any]:
        """
        Poll the task status until completion or timeout.
        Args:
            task_id (str): The ID of the task to poll.
            timeout (int): Maximum time to wait in seconds.
            interval (int): Time between polls in seconds.
        Returns:
            dict: The completed task response.
        """
        endpoint = f"{self.base_url}/task_status/{task_id}"
        headers = {"x-api-key": self.api_key}
        start_time = time.time()
        
        while True:
            if time.time() - start_time > timeout:
                raise TimeoutError(f"Task {task_id} did not complete within {timeout} seconds")
            
            response = requests.get(endpoint, headers=headers)
            if response.status_code != 200:
                raise Exception(f"Error checking task status: {response.status_code} - {response.text}")
            
            status_data = response.json()
            if status_data["status"] == "completed":
                return status_data
            elif status_data["status"] == "failed":
                raise Exception(f"Task failed: {status_data.get('error', 'Unknown error')}")
            
            time.sleep(interval)

    def process_pdf(self, 
                   pdf_url: Optional[str] = None, 
                   file_content: Optional[bytes] = None,
                   filename: Optional[str] = None,
                   quality: str = "standard") -> Dict[str, Any]:
        """
        Process a PDF file and convert it to markdown.
        Args:
            pdf_url (str, optional): URL of the PDF file to process.
            file_content (bytes, optional): Raw bytes of the PDF file to upload.
            filename (str, optional): Name of the file when uploading raw bytes.
            quality (str, optional): Quality of processing, either "standard" or "high".
        Returns:
            dict: A dictionary containing the response from the API.
        """
        endpoint = f"{self.base_url}/process_pdf/"
        headers = {"x-api-key": self.api_key}
        
        # Validate inputs
        if pdf_url and file_content:
            raise ValueError("Provide either pdf_url or file_content, not both")
        if not pdf_url and not file_content:
            raise ValueError("Either pdf_url or file_content must be provided")
        if file_content and not filename:
            raise ValueError("filename must be provided when using file_content")
            
        if pdf_url:
            # URL-based processing
            data = {"pdf_url": pdf_url, "quality": quality}
            response = requests.post(endpoint, headers=headers, json=data)
        else:
            # File upload processing
            params = {'uploadFile': 'True', 'quality': quality}
            files = {'file': (filename, file_content, 'application/pdf')}
            response = requests.post(endpoint, params=params, headers=headers, files=files)
            
        if response.status_code == 202:
            task_data = response.json()
            task_id = task_data["task_id"]
            return self._poll_task_status(task_id)
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")

    def process_image(self,
                     image_url: Optional[str] = None,
                     file_content: Optional[bytes] = None,
                     filename: Optional[str] = None,
                     quality: str = "standard") -> Dict[str, Any]:
        """
        Process an image file and convert it to markdown.
        Args:
            image_url (str, optional): URL of the image file to process.
            file_content (bytes, optional): Raw bytes of the image file to upload.
            filename (str, optional): Name of the file when uploading raw bytes.
            quality (str, optional): Quality of processing, either "standard" or "high".
        Returns:
            dict: A dictionary containing the response from the API.
        """
        endpoint = f"{self.base_url}/process-image/"
        headers = {"x-api-key": self.api_key}
        
        # Validate inputs
        if image_url and file_content:
            raise ValueError("Provide either image_url or file_content, not both")
        if not image_url and not file_content:
            raise ValueError("Either image_url or file_content must be provided")
        if file_content and not filename:
            raise ValueError("filename must be provided when using file_content")
            
        if image_url:
            data = {"image_url": image_url, "quality": quality}
            response = requests.post(endpoint, headers=headers, json=data)
        else:
            params = {'uploadFile': 'True', 'quality': quality}
            files = {'file': (filename, file_content, 'image/jpeg')}
            response = requests.post(endpoint, params=params, headers=headers, files=files)
            
        if response.status_code == 202:
            task_data = response.json()
            task_id = task_data["task_id"]
            return self._poll_task_status(task_id)
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")

    def fetch_markdown(self, url: str) -> str:
        """
        Fetch the markdown content from a given URL.
        Args:
            url (str): URL of the markdown content.
        Returns:
            str: The markdown content.
        """
        endpoint = f"{self.base_url}/fetch_markdown/"
        params = {"url": url}
        response = requests.get(endpoint, params=params)
        
        if response.status_code == 200:
            return response.text
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")

    def process_markdown(self, content: str) -> Dict[int, str]:
        """
        Process markdown content and split it into pages.
        Args:
            content (str): The markdown content to process.
        Returns:
            Dict[int, str]: Dictionary of page numbers and their content.
        """
        if not content:
            raise ValueError("Empty markdown content")

        try:
            pages = re.split(r'<!-- PAGE \d+ -->', content)
            pages = [page.strip() for page in pages if page.strip()]
            page_dict = {i: content for i, content in enumerate(pages, start=1)}

            if not page_dict:
                raise ValueError("No extractable text found in the markdown")

            return page_dict
        except Exception as e:
            raise ValueError(f"Failed to process markdown: {str(e)}")

    def get_user_documents(self) -> List[Dict[str, Any]]:
        """
        Get all documents for the authenticated user.
        Returns:
            List[Dict[str, Any]]: List of documents and their metadata.
        """
        endpoint = f"{self.base_url}/user_documents/"
        headers = {"x-api-key": self.api_key}
        
        response = requests.get(endpoint, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """
        Get the current status of a task.
        Args:
            task_id (str): The ID of the task to check.
        Returns:
            Dict[str, Any]: The task status and related information.
        """
        endpoint = f"{self.base_url}/task_status/{task_id}"
        headers = {"x-api-key": self.api_key}
        
        response = requests.get(endpoint, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")

    # def get_task_timestamps(self) -> Dict[str, Any]:
    #     """
    #     Get timestamps for all tasks.
    #     Returns:
    #         Dict[str, Any]: Dictionary containing task timestamps and related information.
    #     """
    #     endpoint = f"{self.base_url}/tasks/timestamps"
    #     headers = {"x-api-key": self.api_key}
        
    #     response = requests.get(endpoint, headers=headers)
        
    #     if response.status_code == 200:
    #         return response.json()
    #     else:
    #         raise Exception(f"Error: {response.status_code} - {response.text}")

    def process_pdf_async(self, 
                        pdf_url: Optional[str] = None, 
                        file_content: Optional[bytes] = None,
                        filename: Optional[str] = None,
                        quality: str = "standard") -> str:
        """
        Process a PDF file asynchronously and return the task ID for manual polling.
        Args:
            pdf_url (str, optional): URL of the PDF file to process.
            file_content (bytes, optional): Raw bytes of the PDF file to upload.
            filename (str, optional): Name of the file when uploading raw bytes.
            quality (str, optional): Quality of processing, either "standard" or "high".
        Returns:
            str: The task ID for polling the status.
        """
        endpoint = f"{self.base_url}/process_pdf/"
        headers = {"x-api-key": self.api_key}
        
        # Validate inputs
        if pdf_url and file_content:
            raise ValueError("Provide either pdf_url or file_content, not both")
        if not pdf_url and not file_content:
            raise ValueError("Either pdf_url or file_content must be provided")
        if file_content and not filename:
            raise ValueError("filename must be provided when using file_content")
            
        if pdf_url:
            data = {"pdf_url": pdf_url, "quality": quality}
            response = requests.post(endpoint, headers=headers, json=data)
        else:
            params = {'uploadFile': 'True', 'quality': quality}
            files = {'file': (filename, file_content, 'application/pdf')}
            response = requests.post(endpoint, params=params, headers=headers, files=files)
            
        if response.status_code == 202:
            task_data = response.json()
            return task_data["task_id"]
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")

    def process_image_async(self,
                        image_url: Optional[str] = None,
                        file_content: Optional[bytes] = None,
                        filename: Optional[str] = None,
                        quality: str = "standard") -> str:
        """
        Process an image file asynchronously and return the task ID for manual polling.
        Args:
            image_url (str, optional): URL of the image file to process.
            file_content (bytes, optional): Raw bytes of the image file to upload.
            filename (str, optional): Name of the file when uploading raw bytes.
            quality (str, optional): Quality of processing, either "standard" or "high".
        Returns:
            str: The task ID for polling the status.
        """
        endpoint = f"{self.base_url}/process-image/"
        headers = {"x-api-key": self.api_key}
        
        # Validate inputs
        if image_url and file_content:
            raise ValueError("Provide either image_url or file_content, not both")
        if not image_url and not file_content:
            raise ValueError("Either image_url or file_content must be provided")
        if file_content and not filename:
            raise ValueError("filename must be provided when using file_content")
            
        if image_url:
            data = {"image_url": image_url, "quality": quality}
            response = requests.post(endpoint, headers=headers, json=data)
        else:
            params = {'uploadFile': 'True', 'quality': quality}
            files = {'file': (filename, file_content, 'image/jpeg')}
            response = requests.post(endpoint, params=params, headers=headers, files=files)
            
        if response.status_code == 202:
            task_data = response.json()
            return task_data["task_id"]
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")