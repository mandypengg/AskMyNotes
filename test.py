from rag import answer_question

answer = answer_question(
    "In what line is the lyric 'Now I'll just see you when I'm on business with everyone' on?",
    pdf_path="sweetboy-lyrics.pdf"
)

print(answer)