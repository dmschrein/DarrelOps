"""Helper functions and utilities"""
# darrelops/services/util.py

def allowed_file(filename):
    ALLOWED_EXTS = ['zip', 'tar', 'tar.gz']
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTS
