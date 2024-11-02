import logging
import uuid
from pathlib import Path
import json
import numpy as np
import requests
from requests.exceptions import HTTPError

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s:%(message)s")
logger = logging.getLogger(__name__)
req_logger = logging.getLogger("requests.packages.urllib3")


class InferenceHTTPClient:
    """
    InferenceHTTPClient class handles the interaction with an inference API for processing images.

    Attributes:
        api_endpoint (str): The endpoint of the API.
        api_key (str): The API key for authentication.
    """

    def __init__(self, api_endpoint, api_key, debug=False):
        self.api_endpoint = api_endpoint.rstrip("/")
        self.api_key = api_key
        self.debug = debug

        if self.debug:
            logger.setLevel(logging.DEBUG)
            req_logger.setLevel(logging.DEBUG)
            req_logger.propagate = True

    def _unwrap_embedding(self, result: dict) -> dict:
        """Unwraps embedding data in the response from the Inference API."""
        embedding, shape = result["embedding"], result["shape"]

        return {"embedding": np.array(embedding).reshape(shape)}

    def infer(
        self,
        image_path,
        trained_model_uid: str = None,
        pretrained_model_type: str = None,
        **optional_infer_params,
    ):
        """Runs inference on the given image file.

        :param image_path: The path to the image file to be processed for inference.
        :param trained_model_uid: The unique identifier of the trained model to be used for inference.
        :param pretrained_model_type: The type of pretrained model.
        :param optional_infer_params: Optional params for segment everything model.
        :return: The response from the inference API.
        """
        image_path = Path(image_path)
        if not image_path.is_file():
            raise FileNotFoundError("Image file not found")

        if (not trained_model_uid and not pretrained_model_type) or (
            trained_model_uid and pretrained_model_type
        ):
            raise ValueError(
                "Must provide either a trained model UID or a pretrained model type"
            )

        try:
            # Upload the image to S3
            logger.info("Uploading the image to the server...")
            temp_filename = image_path.with_stem(f"temp_{uuid.uuid4()}").name
            presigned_url = self._generate_s3_presigned_url(temp_filename)
            logger.debug("S3 presigned URL: %s", presigned_url)
            self._upload_temp_image(image_path, presigned_url)
            logger.info("Image uploaded.")

            optional_payload = {}
            optional_payload.update(optional_infer_params)
            payload = {
                "temp_filename": temp_filename,
                "trained_model_uid": trained_model_uid,
                "pretrained_model_type": pretrained_model_type,
                "optional_infer_params": optional_payload,
            }

            # Call the inference API, using the image just uploaded to S3
            logger.info("Running inference...")
            response = requests.post(
                self.api_endpoint + "/inference",
                headers={"X-Api-Key": self.api_key},
                json=payload,
            )
            response.raise_for_status()
            logger.info("Inference completed.")

            result = json.loads(response.content)
            if pretrained_model_type == "smart_polygon":
                return self._unwrap_embedding(result)
            else:
                return result
        except Exception as e:
            logger.error(e)
            if isinstance(e, HTTPError):
                logger.error("Detail: %s", e.response.text)
            if self.debug:
                logger.exception(e)

    def _generate_s3_presigned_url(self, temp_filename):
        """Generates a presigned URL for uploading a file to a temporary location in S3.

        :param temp_filename: The name of the temporary file for which the presigned URL is to be generated.
        :return: A presigned URL for the temporary file.
        """
        response = requests.post(
            self.api_endpoint + "/temp-files",
            headers={"X-Api-Key": self.api_key},
            json={"filename": temp_filename},
        )
        return response.json()["presigned_url"]

    @staticmethod
    def _upload_temp_image(image_path, presigned_url):
        """Uses a presigned URL to upload the specified image file to a temporary location in S3.

        :param image_path: The local file path of the image to be uploaded.
        :param presigned_url: The pre-signed URL to which the image will be uploaded.
        """
        with open(image_path, "rb") as image_file:
            response = requests.put(
                presigned_url, headers={"X-Amz-Tagging": "temp=true"}, data=image_file
            )
            response.raise_for_status()