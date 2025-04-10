from flask import Blueprint, abort, send_file, make_response
from app_utils import *
import logging
import os
import yt_dlp
import tempfile
from werkzeug.utils import secure_filename
import uuid
from services.cloud_storage import upload_file
from services.authentication import authenticate
from services.file_management import download_file
from urllib.parse import quote
from config import LOCAL_UPLOAD_STORAGE_PATH

v1_media_local_download_bp = Blueprint('v1_media_local_download', __name__)
logger = logging.getLogger(__name__)

@v1_media_local_download_bp.route('/v1/BETA/media/downloadl/<string:file_name>', methods=['GET'])
#@authenticate
@queue_task_wrapper(bypass_queue=False)
def download_media_local(job_id, data, file_name):

    logger.info(f"Job {job_id}: Received local download request for {file_name}")

    file_path = os.path.join(LOCAL_UPLOAD_STORAGE_PATH, file_name)

    try:
        # Check if the file exists
        if not os.path.isfile(file_path):
            logger.error(f"Job {job_id}: File not found - {file_path}")
            return "File not found.", "/v1/BETA/media/downloadl", 404 

        response = make_response(send_file(file_path, as_attachment=True, download_name=file_name))

        return response, "/v1/BETA/media/downloadl", 200 # Return the file specified by filename

    except Exception as e:
        logger.error(f"Job {job_id}: Error during download process - {str(e)}")
        return str(e), "/v1/BETA/media/downloadl", 500 