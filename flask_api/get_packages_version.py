import pkg_resources

# List of libraries and packages to check
from mastodon import Mastodon, MastodonNotFoundError
libraries = ['couchdb', 'flask', 'pandas', 'flask_cors', 'argparse','textblob','requests','mastodon.py','numpy']

# Iterate over the libraries and get their versions
for lib in libraries:
    try:
        version = pkg_resources.get_distribution(lib).version
        print(f"{lib}: {version}")
    except pkg_resources.DistributionNotFound:
        print(f"{lib}: Not installed")
