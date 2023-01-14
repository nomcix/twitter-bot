import logging
import os
from dotenv import load_dotenv
import tweepy

logger = logging.getLogger(__name__)

load_dotenv()

API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")


def post_image_to_twitter(image_path, term):
    logger.info("Posting tweet...")
    try:
        auth = tweepy.OAuth1UserHandler(
            API_KEY,
            API_SECRET,
            ACCESS_TOKEN,
            ACCESS_TOKEN_SECRET
        )
        api = tweepy.API(auth)

        if not os.path.exists(image_path):
            logger.error(f"Image not found at: {image_path}")
            raise FileNotFoundError("Image not found")

        media = api.media_upload(filename=image_path)
        api.update_status(status=f"> {term}", media_ids=[media.media_id_string])
        logger.info("Tweet posted...")
    except Exception as err:
        logger.error("Error posting tweet...", exc_info=True)
        raise
