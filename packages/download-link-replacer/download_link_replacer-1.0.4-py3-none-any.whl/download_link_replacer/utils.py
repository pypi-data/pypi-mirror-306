from pkg_resources import get_distribution
from sphinx.util import logging

VERSION = get_distribution("download_link_replacer").version

SPHINX_LOGGER = logging.getLogger(__name__)
ENV_PROPERTY_NAME = "download_link_replacements"
