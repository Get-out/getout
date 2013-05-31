import argparse
import logging

from get_out.app import make_app

log = logging.getLogger("get-out-server")

def serve_forever(host, port, debug=False):
	'''Start the flask app'''
	app = make_app(debug=debug)
	app.run(host, port, threaded=True, debug=debug)

def setup_logger():
	log = logging.getLogger('')
	formatter = logging.Formatter("[%(asctime)s] %(name)s: %(message)s")
	stream_logger = logging.StreamHandler()
	stream_logger.setFormatter(formatter)
	stream_logger.setLevel(logging.INFO)
	log.addHandler(stream_logger)
	log.setLevel(logging.INFO)

def make_parser():
	parser = argparse.ArgumentParser(description="get-out server")
	parser.add_argument('--port'
		, type=int
		, default=4000
		, help='API bind port'
		)
	parser.add_argument('--host'
		, default='localhost'
		, help='API bind address'
		)
	parser.add_argument('--debug'
		, help = "whether to have debug pages"
		, action = 'store_true'
		)
	return parser

def main():
	parser = make_parser()
	args = parser.parse_args()
	setup_logger()

	try:
		serve_forever(args.host, args.port, debug=args.debug)
	except KeyboardInterrupt:
		print 'Shutting down...'
