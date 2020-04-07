from app.main import bp

from log import debug_logger

@bp.route('/')
def index():
	debug_logger.info("Loading the index page")
	return "index page"