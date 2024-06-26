#
#   Logging functionality
#   Tanguy Ophoff
#

def add_log_level(name, level):
    """
    This function adds an extra logging level to the logging module, that can be used by any logger.

    Args:
        name (str): Name of the new logging level
        level (int): Logging level you want to add

    Returns:
        None

    Required Libraries:
        -

    Example:
        >>> add_log_level('TRACE', logging.DEBUG - 5)
        >>> log = logging.getLogger('test')
        >>> log.trace('testing new loglevel')
    """
    import logging

    level_name = name.upper()
    method_name = name.lower()
    if hasattr(logging, level_name):
        raise AttributeError('{} already defined in logging module'.format(level_name))
    if hasattr(logging, method_name):
        raise AttributeError('{} already defined in logging module'.format(method_name))
    if hasattr(logging.getLoggerClass(), method_name):
        raise AttributeError('{} already defined in logger class'.format(method_name))

    def log_for_level(self, message, *args, **kwargs):
        if self.isEnabledFor(level):
            self._log(level, message, args, **kwargs)
            
    def log_to_root(message, *args, **kwargs):
        logging.log(level, message, *args, **kwargs)

    logging.addLevelName(level, level_name)
    setattr(logging, level_name, level)
    setattr(logging.getLoggerClass(), method_name, log_for_level)
    setattr(logging, method_name, log_to_root)


if __name__ == '__main__':
    print('functions: add_log_level')
