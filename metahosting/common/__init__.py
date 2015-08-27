import argparse
import logging
import uuid


def argument_parsing():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug",
                        help="get debug output",
                        action="store_true")
    parser.add_argument("--logstash",
                        help="log everything (in addition) to logstash "
                             ", give host:port")
    parser.add_argument("--envfile",
                        help="provide a file that tells which not-default "
                        "environment variables to use")
    parser.add_argument("--config",
                        help="provide a config file")
    return parser.parse_args()


def logging_setup(arguments):
    logger = logging.getLogger()
    logger.addHandler(logging.StreamHandler())
    if arguments.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    if arguments.logstash:
        import logstash
        host, port = arguments.logstash.split(':')
        logger.addHandler(logstash.TCPLogstashHandler(host=host,
                                                      port=int(port),
                                                      version=1))


def get_uuid(filename=None):
    try:
        filehandler = open(filename, 'r')
        content = (filehandler.read()).rstrip()
        return str(uuid.UUID(content))
    except IOError:
        if filename:
            logging.error('Not able to read file: %s ', filename)
    except ValueError:
        logging.error('Not able to validate uuid: %s ', content)
    except KeyError:
        logging.error('No path for uuid file in conf' )
    return str(uuid.uuid4())