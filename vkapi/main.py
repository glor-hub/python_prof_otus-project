import argparse
import logging

def logging_init(logging_file):
    # initialize script logging
    logging.basicConfig(filename=logging_file,
                        format='[%(asctime)s] %(levelname).1s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.INFO)


if __name__ == '__main__':

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-p', '--period', help='Poll period', default=CRAWLING_PERIOD, type=int)
    arg_parser.add_argument('-p', '--log', help='Log file', default=None, type=str)
    args = arg_parser.parse_args()
    logging_init(None)
    asyncio.run(main())
