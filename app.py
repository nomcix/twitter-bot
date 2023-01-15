import log_config
import logging
import db_connector
import image_generator
import tweet_poster

logger = logging.getLogger(__name__)


def main():
    try:
        logger.info("Starting app...")
        term, definition = db_connector.fetch_random_term()
        print(term, definition)
        image_path = image_generator.create_tweet_image(term, definition) 
        tweet_poster.post_image_to_twitter(f"tweets/{image_path}.png", f"{term}")
        db_connector.update_posted(term)
        logger.info("App finished...")
    except Exception:
        logger.info("App finished with errors...")


if __name__ == "__main__":
    main()
