# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['libgen_api_modern']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.9.5,<4.0.0', 'bs4>=0.0.2,<0.0.3']

entry_points = \
{'console_scripts': ['libgen_api_modern = libgen_api_modern:main']}

setup_kwargs = {
    'name': 'libgen-api-modern',
    'version': '0.1.12',
    'description': 'Search Library Genesis. This library enables you to search Library Genesis programmatically for Non-fiction/Sci-tech, Fiction, and Sci-mag - Scientific articles.',
    'long_description': '# libgen-api-modern\n\nSearch Library Genesis programmatically using an enhanced Python library. This fork extends the original `libgen-api` by [Harrison Broadbent](https://github.com/harrison-broadbent/libgen-api) and `libgen-api-enhanced` by [Onurhan](https://github.com/onurhanak/libgen-api-enhanced) with added features like direct download links and book cover links. It also returns 100 results by default.\n\n## Contents\n\n- [libgen-api-modern](#libgen-api-modern)\n  - [Contents](#contents)\n  - [Getting Started](#getting-started)\n  - [NOTICE](#notice)\n    - [Non-fiction/Sci-tech](#non-fictionsci-tech)\n    - [Fiction](#fiction)\n    - [Sci-mag - Scientific articles](#sci-mag---scientific-articles)\n  - [Basic Searching](#basic-searching)\n    - [Title](#title)\n    - [Author](#author)\n  - [Filtered Searching](#filtered-searching)\n    - [Filtered Title Searching](#filtered-title-searching)\n    - [Non-exact Filtered Searching](#non-exact-filtered-searching)\n  - [Results Layout](#results-layout)\n    - [Non-fiction/sci-tech result layout](#non-fictionsci-tech-result-layout)\n    - [Fiction result layout](#fiction-result-layout)\n    - [Sci-mag results layout](#sci-mag-results-layout)\n  - [Contributors](#contributors)\n\n## Getting Started\n\nInstall the package -\n\nusing pipx\n\n```\npipx install libgen-api-modern\n```\n\nusing poetry\n\n```\npoetry add libgen-api-modern\n```\n\n## NOTICE\n\nWith libgen-api-modern library, you can search for:\n\n- non-fiction/sci-tech\n- fiction\n- scientific articles\n\n*For the proxy, use only http proxy.*\n\nPerform a basic search -\n\n### Non-fiction/Sci-tech\n\n```python\n# search()\n\nfrom libgen_api_modern import LibgenSearch\nresults = await LibgenSearch.search("The Alchemist")\nprint(results)\n```\n\n### Fiction\n\n```python\n# search_fiction()\n\nfrom libgen_api_modern import LibgenSearch\nresults = await LibgenSearch.search_fiction("How to kill men and get away with it")\nprint(results)\n```\n\n### Sci-mag - Scientific articles\n\n```python\n# search_scientific_articles()\n\nfrom libgen_api_modern import LibgenSearch\nresults = await LibgenSearch.search_scientific_articles("Solar")\nprint(results)\n```\n\n## Basic Searching\n\nSearch by title or author:\n\n### Title\n\n```python\n# search title\n\nfrom libgen_api_modern import LibgenSearch\nresults = await LibgenSearch.search("Pride and Prejudice", search_type = "title")\nprint(results)\n```\n\n### Author\n\n```python\n# search author\n\nfrom libgen_api_modern import LibgenSearch\nresults = await LibgenSearch.search("Jane Austen", search_type = "author")\nprint(results)\n```\n\n> You can provide title, author, ISBN, publisher, year, language, or series as arguments to search_type\n\n## Filtered Searching\n\n- You can define a set of filters, and then use them to filter the search results that get returned.\n- By default, filtering will remove results that match the filters exactly (case-sensitive) -\n  - This can be adjusted by setting `exact_match=True` when calling one of the filter methods, which allows for case-insensitive and substring filtering.\n\n### Filtered Title Searching\n\n```python\n# search_filtered()\n\nfrom libgen_api_modern import LibgenSearch\n\ntitle_filters = {"Year": "2007", "Extension": "epub"}\ntitles = await LibgenSearch.search_filtered("Pride and Prejudice", title_filters, exact_match=True)\nprint(titles)\n```\n\n### Non-exact Filtered Searching\n\n```python\n# search filtered \n# exact_match = False\n\nfrom libgen_api_modern import LibgenSearch\n\npartial_filters = {"Year": "2000"}\ntitles = await LibgenSearch.search_filtered("Agatha Christie", partial_filters, exact_match=False)\nprint(titles)\n\n```\n\n## Results Layout\n\n### Non-fiction/sci-tech result layout\n\nResults are returned as a list of dictionaries:\n\n```json\n[\n  {\n    "Title": "The war of art", \n    "Author(s)": "Mits Free", \n    "Series": "example series", \n    "Periodical": "", \n    "Publisher": "Libre publishers", \n    "City": "New York, NY", \n    "Year": "2002", \n    "Edition": "1st ed",\n    "Language": "English",\n    "Pages": "165[159]",\n    "ISBN": "123456789",\n    "ID": "1487009",\n    "Size": "430 Kb (440781)",\n    "Extension": "pdf",\n    "Cover": "https://covers.xyz.jpg", \n    "Direct_Download_Link": "https://download.xyz/book.pdf"\n  }\n]\n\n```\n\n### Fiction result layout\n\n```json\n\n[\n  {\n    "Title": "How to Get Away With It",\n    "Language": "English",\n    "Year": "1873",\n    "Publisher": "Pub",\n    "Format": "EPUB",\n    "ID": "4263532",\n    "Authors": "John Doe",\n    "Cover": "https://cover.xyz.book.jpg",\n    "Direct_Download_Link": "https://download.xyz.book.epub"\n  }\n]\n```\n\n### Sci-mag results layout\n\n```json\n\n[\n  {\n    "Title": "Superhuman-like dominance", \n    "Authors": "Goated Johnnie", \n    "DOI": "15.142/cze.12345", \n    "Journal": "The Journal of Complete dominance", \n    "Publisher": "Johnnie prods", \n    "Year": "2002", \n    "Volume": "445", \n    "Issue": "4", \n    "Pages": "374—387", \n    "ID": "1142493", \n    "Direct_Download_Link_1": "", \n    "Direct_Download_Link_2": "https://example.zxy/article.pdf"\n  }\n]\n```\n\n## Contributors\n\nPlease don\'t hesitate to raise an issue, or [fork this project](https://github.com/johnnie-610/libgen-api-modern) and improve on it.\n\nThanks to the following people:\n\n- [harrison-broadbent](https://github.com/harrison-broadbent) who wrote the original Libgen API.\n- [calmoo](https://github.com/calmoo)\n- [HENRYMARTIN5](https://github.com/HENRYMARTIN5)\n- [Onurhan](https://github.com/onurhanak)\n\nPlease star [this library on Github](https://github.com/johnnie-610/libgen-api-modern) if you like it.\n',
    'author': 'Johnnie',
    'author_email': '99084912+johnnie-610@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
