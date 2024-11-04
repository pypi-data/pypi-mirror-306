import logging

import dotenv

from src.config.project_paths import top_level_dir

logging.basicConfig(format='%(name)s-%(levelname)s|%(lineno)d:  %(message)s',
                    level=logging.INFO)
log = logging.getLogger(__name__)

log.debug(top_level_dir / '.env')
dotenv.load_dotenv(top_level_dir / '.env')
