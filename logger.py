import logging
import sys
from datetime import datetime
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

log_filename = LOG_DIR / f"requests_{datetime.now().strftime('%Y-%m-%d')}.log"

logger = logging.getLogger("verification_api")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(log_filename, encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler(
    stream=open(sys.stdout.fileno(), mode="w", encoding="utf-8", buffering=1)
)
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

def log_incoming_request(product_id, title, category, media_count):
    logger.info(f"[REQUEST] Incoming verification | productId={product_id} | title='{title}' | category='{category}' | images={media_count}")

def log_image_fetch(media_id, url):
    logger.debug(f"[FETCH] Downloading image | mediaId={media_id} | url={url}")

def log_image_fetch_success(media_id, url):
    logger.info(f"[FETCH] OK - Image downloaded | mediaId={media_id} | url={url}")

def log_image_fetch_error(media_id, url, error):
    logger.error(f"[FETCH] FAILED - Could not download | mediaId={media_id} | url={url} | error={error}")

def log_gemini_request(media_id, category, title):
    logger.info(f"[GEMINI] Sending to Gemini API | mediaId={media_id} | category='{category}' | title='{title}'")

def log_gemini_response(media_id, confidence, verdict):
    logger.info(f"[GEMINI] OK - Response received | mediaId={media_id} | confidence={confidence}% | verdict={verdict}")

def log_gemini_error(media_id, error):
    logger.error(f"[GEMINI] FAILED - API error | mediaId={media_id} | error={error}")

def log_result_summary(product_id, overall_verdict, overall_confidence, duration_ms):
    logger.info(f"[DONE] Verification complete | productId={product_id} | verdict={overall_verdict} | confidence={overall_confidence}% | duration={duration_ms:.0f}ms")