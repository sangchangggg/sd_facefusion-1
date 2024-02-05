METADATA = \
{
    'name': 'RD FaceFusion',
    'description': 'Next generation face swapper and enhancer',
    'version': '2.2.1',
    'license': 'MIT',
    'author': 'Henry Ruhs',
    'url': 'https://facefusion.io'
}


def get(key: str) -> str:
    return METADATA[key]