#!/usr/bin/env python3

from typing import Dict

from fastapi import FastAPI
from pydantic import BaseModel
import en_core_web_sm as language_model


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


# lemma_
# pos_ (upos)
# i (token index)
# idx the index (in chars) of the token start

class SyntaxToken(BaseModel):
    begin_offset: int
    end_offset: int
    part_of_speech_tag: str
    text: str
    token_id: int


class SyntaxResponse(BaseModel):
    syntax_tokens: list[SyntaxToken]


@app.post("/syntax", response_model=SyntaxResponse)
async def syntax(text: str):
    doc = nlp(text)
    tokens = []
    for token in doc:
        syntax_token = SyntaxToken(
            begin_offset=token.idx,
            end_offset=token.idx + len(token),
            part_of_speech_tag=token.lemma_,
            text=token.text,
            token_id=token.i,
        )
        tokens.append(syntax_token)

    return SyntaxResponse(syntax_tokens=tokens)
