from typing import List
import fasttext.util
import numpy as np

from datetime import date
from db_lib.crud import get_news_by_filters
from db_lib.models import News
from db_lib.database import SessionLocal
from sqlalchemy.orm import Session
import click


from natasha import (
    Segmenter,
    MorphVocab,
    
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,
    
    PER,
    NamesExtractor,

    Doc
)

def tag_news_content(news_list: List[News]) -> List[List(str)]:
    if not news_list:
        return []
    tags = []
    for news in news_list
        segmenter = Segmenter()
        morph_vocab = MorphVocab()
        emb = NewsEmbedding()
        syntax_parser = NewsSyntaxParser(emb)
        ner_tagger = NewsNERTagger(emb)
        names_extractor = NamesExtractor(morph_vocab)
        doc = Doc(news.title)
        doc.segment(segmenter)
        doc.tag_morph(morph_tagger)
        doc.parse_syntax(syntax_parser)
        doc.tag_ner(ner_tagger)
        for token in doc.tokens:
            token.lemmatize(morph_vocab)
        for span in doc.spans:
            span.normalize(morph_vocab)
        a = set()
        for span in doc.spans:
            a.add(span.normal)
        tags.append(list(a))
    return tags


@click.command()
@click.option("--start_date", type=click.DateTime(formats=["%Y-%m-%d"]),
              default=str(date.today()))
@click.option("--end_date", type=click.DateTime(formats=["%Y-%m-%d"]),
              default=str(date.today()))
def tag_messages(start_date: date, end_date: date, db: Session = SessionLocal()):

    """Загружаем все сообщения (пока сообщений немного) и кластеризуем их с помощью кластеризатора"""

    news_list = get_news_by_filters(db, topic=None, start_date=start_date, end_date=end_date, limit=LIMIT_NEWS)
    tag = tag_news_content(news_list)
    for i in range(len(news_list)):
        news_list[i].tag = tag[i]
    db.commit()


if __name__ == '__main__':
    tag_messages()