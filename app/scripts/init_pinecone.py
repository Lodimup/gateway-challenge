"""
Script to create a Pinecone index for the RAGS dataset
"""

import logging

from services.oai.rags import create_index

logger = logging.getLogger(__name__)


def main():
    try:
        logger.info("Creating Pinecone default index")
        create_index("default")
    except Exception as e:
        logger.error(f"Error: {e}")

    logging.info("Pinecone index created successfully")


if __name__ == "__main__":
    main()
