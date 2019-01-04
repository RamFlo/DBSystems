import logging
import logging.config

class Logger:
  def __init__(self,):
    logging.config.fileConfig('logging.conf')
    self.logger = logging.getLogger("michaelsProject")
    