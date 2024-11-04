import os
from setuptools import setup

version = '1.1.1'

with open("README.md", "r", encoding='utf-8') as fh:
    readme = fh.read()
    setup(
        name='funcspy',
        version=version,
        url='https://github.com/gabriellopesdesouza2002/funcspy',
        license='MIT License',
        author='Gabriel Lopes de Souza',
        long_description=readme,
        long_description_content_type="text/markdown",
        author_email='gabriellopesdesouza2002@gmail.com',
        keywords='Functions to help you develop any program or script you want',
        description=u'Functions to help you develop any program or script you want',
        
        packages= [
            os.path.join('funcspy', 'emails_funcs'),
            os.path.join('funcspy', 'exceptions_funcs'),
            os.path.join('funcspy', 'gui_funcs'),
            os.path.join('funcspy', 'pdf_funcs', 'ocr_funcs'),
            os.path.join('funcspy', 'pdf_funcs', 'pdfutils'),
            os.path.join('funcspy', 'python_funcs'),
            os.path.join('funcspy', 'regex_funcs'),
            os.path.join('funcspy', 'selenium_funcs'),
            os.path.join('funcspy', 'utils_funcs'),
        ],
        
        install_requires= [
            'selenium',
            'bs4',
            'requests',
            'html5lib',
            'webdriver-manager',
            'pretty-html-table',
            'xlsxwriter',
            'pandas',
            'sqlalchemy',
            'rich',
            'pyinstaller',
            'filetype',
            # for ocr
            'pytesseract',
            'tqdm',
            'pillow',
            'PyMuPDF',
            'holidays',
            'numpy==1.26.0',
        ],
    #     extras_require={
    #         'openai': [ # for chatpdf
    #             'openai',
    #         ]
    # },
)
