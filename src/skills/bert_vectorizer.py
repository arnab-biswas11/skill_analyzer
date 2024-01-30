from sentence_transformers import SentenceTransformer
import time
import logging
import torch


class BertVectorizer:
    """
    Use a pretrained transformers model to embed sentences.
    In this form so it can be used as a step in the pipeline.
    """

    def __init__(
        self,
        bert_model_name="sentence-transformers/all-MiniLM-L6-v2",
        multi_process=False,
        batch_size=32,
        verbose=True,
    ):
        self.bert_model_name = bert_model_name
        self.multi_process = multi_process
        self.batch_size = batch_size
        self.verbose = verbose

    def fit(self, *_):
        device = torch.device(f"cuda:0" if torch.cuda.is_available() else "cpu")
        self.bert_model = SentenceTransformer(self.bert_model_name, device=device)
        self.bert_model.max_seq_length = 512
        return self

    def transform(self, texts):
        t0 = time.time()
        if self.multi_process:
            # logger.info(".. with multiprocessing")
            pool = self.bert_model.start_multi_process_pool()
            self.embedded_x = self.bert_model.encode_multi_process(
                texts, pool, batch_size=self.batch_size
            )
            self.bert_model.stop_multi_process_pool(pool)
        else:
            self.embedded_x = self.bert_model.encode(texts, batch_size=self.batch_size)
        return self.embedded_x
