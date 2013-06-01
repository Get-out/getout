from setuptools import setup

# Setup the project
setup(
	  name = "get-out"
	, version = '0.1'
	, packages = ['get_out']

	, package_data =
	  { 'get-out':
		[ 'templates/*.html'
		]
	  }

	, install_requires =
	  [ 'django'
      , 'psycopg2'
	  ]

	# metadata
	, description = "A GovHack 2013 idea"
	, license = "Other/Proprietary"
	)

