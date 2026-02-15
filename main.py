from data import db_conn, load, chunk
from model import embed, converse
from app import search
import hashlib

def test_load(container):
    text = \
        ("145% increase in goals - Harry Kane has become a penalty machine since joining Bayern Munich\n"
         "Bayern Munich continued their march to a second, successive Bundesliga title on Sunday after "
         "making short work of top-flight upstarts Hoffenheim at the Allianz Arena. Despite an impressive "
         "run of form in recent months, Christian Ilzer’s visiting side capitulated just just 20 minutes "
         "into the match, when the referee pointed to the penalty spot after Luis Díaz was pulled down in "
         "the box. To no great surprise, Harry Kane was on hand to convert the penalty, only to then double "
         "his and his team’s tally just before half-time when his Colombian teammate was once again fouled "
         "in the box. The England international made it two from two and set Bayern on their way to a comfortable win.\n"
         "How many penalties has Harry Kane scored at Bayern?\n"
         "Although it wasn’t Kane that won either penalty in the first place, the sight of the English talisman "
         "converting from the penalty spot has become a regular occurrence in German football since the towering "
         "No.9 made a €95 million move from Tottenham Hotspur to Bayern in the summer of 2023. Kane’s brace on Sunday "
         "took the striker’s tally of penalties in all competitions to 11 for the season. Which means Kane will need "
         "just three more penalties between now and May to break his record for the most penalties scored in a single "
         "season. Perhaps to no great surprise, the 32-year-old striker has found the German top-flight to be fertile "
         "ground for his style of goalscoring.\n"
         "Indeed, as we can see in the table above, Kane has always been a consistent goalscorer from the penalty spot. "
         "During his time at Tottenham he scored no less than 42 penalties in all competitions for the North London club, "
         "which worked out at an impressive 4.7 penalties per season. However, since making the move to Germany we can "
         "see that Kane has clearly become something of a specialist at not only winning penalties but also scoring them: "
         "his first two seasons at Bayern were his best ever for penalties scored and, as previously noted, this current "
         "campaign is his best yet. Which also means that Kane has gone from averaging 0.11 penalty goals every 90 minutes "
         "for Tottenham, to now averaging 0.27 penalty goals per 90 for Bayern. Essentially, Kane’s goalscoring from the "
         "penalty spot has more than doubled and almost tripled since he moved to Germany.\n"
         "To no great surprise, there are very few across Europe’s top five leagues that are capable of keeping up "
         "with the England international in this regard. According to Transfermarkt’s database, Kane has now scored "
         "32 goals in all competitions for Bayern since making the move to the club in 2023. The only player that "
         "comes close to the England striker is none other than Kylian Mbappé, who has scored 29 goals for Paris Saint-Germain "
         "and then Real Madrid in that period of time. In third place is Inter Milan set-piece specialist Hakan Çalhanoğlu, "
         "followed by Liverpool’s Mohamed Salah in fourth with 19 penalties scored for the Anfield club.")

    chunk_size = 500
    chunk_overlap = 100
    text_chunks = chunk.fixed_size_chunking(
        text = text,
        chunk_size = chunk_size,
        chunk_overlap = chunk_overlap
    )

    print(type(text_chunks))
    print(text_chunks)

    for i, text_chunk in enumerate(text_chunks):
        vector = embed.embed(text_chunk, mode="DOC")

        fingerprint = hashlib.sha256(text_chunk.encode('utf-8')).hexdigest()

        load.save_item(
            container=container,
            id=fingerprint,
            content=text_chunk,
            vector=vector,
            metadata={
                "total_chunks": len(text_chunks),
                "chunk_index": i,
                "chunk_size": len(text_chunk),
                "chunk_type": "fixed-size"
            }
        )

def test_search(container, user_query):
    user_query_vector = embed.embed(user_query, mode="QUERY")

    results = search.similarity_search(container, user_query_vector)

    return results

def test_converse(user_input, container):
    vector = embed.embed(user_input, mode="QUERY")
    results = search.similarity_search(container, vector)

    if not results:
        return "no relevant articles found"

    context = "\n---\n".join([
        f"Content: {result['content']}"
        for result in results
    ])

    answer = converse.invoke_conversation(context, user_input)
    return answer

if __name__ == "__main__":
    container = db_conn.get_cosmos_container_conn()
    query = "What has Harry Kane become since joining Bayern Munich?"

    sys_output = test_converse(query, container)
    print(sys_output)