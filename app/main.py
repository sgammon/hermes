import os

if __name__ == '__main__':
	abs = os.path.abspath(__file__).split('/')[0:-2] + ['.profile', 'APIServer.profile']
	print "/".join(abs)
