from setuptools import setup

# Setup the project
setup(
      name = "get-out"
    , version = '0.1'
    , packages = ['get_out', 'atlas_api']

    , package_data =
      { 'get_out':
        [ 'templates/*.html'
        , 'static/js/*.js'
        ]
      }

    , install_requires =
      [ 'django'
      , 'psycopg2'
      , 'requests'
      ]

    # metadata
    , description = "A GovHack 2013 idea"
    , license = "Other/Proprietary"
    )

