"""Darrel Ops entry point script."""
# darrelops/__main__.py

import sys
from darrelops import app, create_database, cli, __app_name__
import darrelops.api

def main():

    create_database()
    
    if len(sys.argv) > 1 and sys.argv[1] == "runserver":
        # run flask api server
        app.run(debug=True)
    else:
        cli.app(prog_name=__app_name__)

    
if __name__ == '__main__':
    main()
    