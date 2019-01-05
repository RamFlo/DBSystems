import logging
import logging.config

class Logger:
  def __init__(self, t="valid"):
    logging.config.fileConfig('logging.conf')
    if (t == "error"):
        self.logger = logging.getLogger("michaelsProjectError")
    else:
        self.logger = logging.getLogger("michaelsProject")
    