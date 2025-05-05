from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer
from dotenv import dotenv_values
from tqdm import tqdm


def build_title_vectors(model, config):
    """
    Method that embeds titles to BERT vectors and updates the database
    :param model: the loaded Bert model
    :param config: the configuration parameters
    """
    title_node_query = """
    MATCH (d:Document)-[r]->(l:Literal)
    WHERE type(r) IN ['HAS_TITLE']
    RETURN l AS node, l.value AS text
    """

    driver = GraphDatabase.driver(config["NEO4J_URI"],
                                  auth=(config["NEO4J_USERNAME"], config["NEO4J_PASSWORD"]))

    with driver.session() as session:
        result = session.run(title_node_query)
        records = list(result)
        for record in tqdm(records, desc="Encoding titles"):
            title_text = record["text"]
            title_embedding = model.encode(title_text)

            session.run("""
            MATCH (l:Literal)
            WHERE l.value = $title_text
            SET l.title_embedding = $title_embedding
            """, title_text=title_text, title_embedding=title_embedding)


def build_abstract_vectors(model, config):
    """
    Method that embeds abstracts to BERT vectors and updates the database
    :param model: the loaded Bert model
    :param config: the configuration parameters
    """
    abstract_node_query = """
    MATCH (d:Document)-[r]->(l:Literal)
    WHERE type(r) IN ['HAS_ABSTRACT']
    RETURN l AS node, l.value AS text
    """

    driver = GraphDatabase.driver(config["NEO4J_URI"],
                                  auth=(config["NEO4J_USERNAME"], config["NEO4J_PASSWORD"]))

    with driver.session() as session:
        result = session.run(abstract_node_query)
        records = list(result)
        for record in tqdm(records, desc="Encoding titles"):
            abstract_text = record["text"]
            abstract_embedding = model.encode(abstract_text)

            session.run("""
            MATCH (l:Literal)
            WHERE l.value = $abstract_text
            SET l.abstract_embedding = $abstract_embedding
            """, abstract_text=abstract_text, abstract_embedding=abstract_embedding)


def main_embedding_title_abstract_vectors(embed_title=True, embed_abstract=False):
    """
    Method launching the embedding of titles and/or abstracts
    :param model: the loaded Bert model
    :param config: the configuration parameters
    """
    config = dotenv_values(".env")
    model = SentenceTransformer(config["BERT_MODEL"])
    if embed_title:
        build_title_vectors(model, config)
    if embed_abstract:
        build_abstract_vectors(model, config)

if __name__ == "__main__":
    main_embedding_title_abstract_vectors()
