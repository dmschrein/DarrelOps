"""Darrel Ops entry point script."""
# darrelops/__main__.py

import sys
from darrelops import __app_name__, create_app

def main():
    
    app = create_app()
    
    if len(sys.argv) > 1 and sys.argv[1] == "runserver":
        # run flask api server
        app.run(debug=True)
    else:
        print(f"Can't run server")

    
if __name__ == '__main__':
    main()
    