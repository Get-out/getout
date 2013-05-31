from setuptools import setup

# Setup the project
setup(
	  name = "get-out"
	, version = '0.1'
	, packages = ['get_out']

	, package_data =
	  {
	  }

	, install_requires =
	  [ 'flask'
	  ]

	, entry_points =
	  { 'console_scripts':
	    [ 'get-out = get_out.main:main'
	    ]
	  }

	# metadata
	, description = "A GovHack 2013 idea"
	, license = "Other/Proprietary"
	)

