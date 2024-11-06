from langchain.vectorstores import Chroma
# from langchain_community.vectorstores import Chroma
from langchain_community.vectorstores.utils import filter_complex_metadata
from langchain_core.embeddings import Embeddings


from langchain.docstore.document import Document

from langchain.document_loaders import DataFrameLoader

from langchain.text_splitter import TextSplitter

# from langchain_community.document_loaders.hugging_face_dataset import HuggingFaceDatasetLoader


class DataFrameToVectorDB:
    def __init__(self,
                 collection_name,
                 persist_directory,
                 embeddings: Embeddings,
                 text_splitter: TextSplitter, 
                 chunk_size=1000, 
                 chunk_overlap=20):
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self.embeddings = embeddings
        self.text_splitter = text_splitter
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.vectordb = Chroma(collection_name=collection_name,
                               persist_directory=persist_directory,
                               embedding_function=embeddings)

    def __split_docs(self, documents):
        docs = self.text_splitter.split_documents(documents)
        return docs

    def __split_list(self, input_list, chunk_size):
        for i in range(0, len(input_list), chunk_size):
            yield input_list[i:i + chunk_size]

    def store(self, df, columns, page_content_columns, max_batch_size=1000):
        for page_content_column in page_content_columns:
            copy_columns = columns.copy()
            copy_columns.append(page_content_column)
            col_df = df[copy_columns].copy()
            col_df.dropna(subset=[page_content_column], inplace=True)
            col_df['type'] = page_content_column  # Set the type column
            documents = []

            loader = DataFrameLoader(data_frame=col_df, page_content_column=page_content_column)
            loaded_docs = loader.load()
            documents.extend(self.__split_docs(loaded_docs))

            split_docs_chunked = self.__split_list(documents, max_batch_size)

            for split_docs_chunk in split_docs_chunked:
                # vectordb = Chroma.from_documents(
                #     collection_name=collection_name,
                #     documents=split_docs_chunk,
                #     embedding=embeddings,
                #     persist_directory=persist_directory,
                # )
                self.vectordb.add_documents(split_docs_chunk)
                self.vectordb.persist()


 