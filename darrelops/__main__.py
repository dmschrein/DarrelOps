"""Darrel Ops entry point script."""
# darrelops/__main__.py

from darrelops import cli, __app_name__

def main():
    cli.app(prog_name=__app_name__)
    
if __name__ == '__main__':
    main()
    
    
