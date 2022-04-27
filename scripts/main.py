#!/usr/bin/env python3

from typing import Dict, List

from fastapi import FastAPI
from pydantic import BaseModel
import en_core_web_md as language_model


nlp = language_model.load()
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


async def lemmas(text: str):
    lemmas = (token.lemma_ for token in nlp(text))
    return {"lemmas": list(lemmas)}


app.get("/lemmas")(lemmas)
app.post("/lemmas")(lemmas)


class SyntaxToken(BaseModel):
    token_id: int
    begin_offset: int
    end_offset: int
    pos: str
    tag: str
    lemma: str
    dep: str
    head: int
    text: str


class SyntaxResponse(BaseModel):
    syntax_tokens: List[SyntaxToken]


@app.post("/syntax", response_model=SyntaxResponse)
async def syntax(text: str):
    doc = nlp(text)
    tokens = []
    for token in doc:
        syntax_token = SyntaxToken(
            token_id=token.i,
            begin_offset=token.idx,
            end_offset=token.idx + len(token),
            text=token.text,
            pos=token.pos_,
            tag=token.tag_,
            lemma=token.lemma_,
            dep=token.dep_,
            head=token.head.i,  # conform to Doc's .to_json API and return idx in Doc
            morph=getattr(token, "morph", None),  # morph isn't in spaCy 2
        )
        tokens.append(syntax_token)

    return SyntaxResponse(syntax_tokens=tokens)
