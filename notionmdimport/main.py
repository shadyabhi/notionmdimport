import logging
import click

from .utils import importer


@click.command()
@click.option('--token_v2', help="token_v2 from notion cookies", required=True)
@click.option('--basepage', help="Base page URL where all files will be added", required=True)
@click.option('--localwiki', help="Base page URL where all files will be added", required=True)
def main(token_v2, basepage, localwiki):
    controller = importer.Notion(token_v2, basepage)
    controller.upload_wiki(localwiki)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.exception("Error running program, got exception", e)
