import re, time, random

try:
    import web, db, classes
    from platforms.oracle import chat
except:
    from . import web, db, classes
    from .platforms.oracle import chat
import logging
from selectolax.parser import HTMLParser, Node
from concurrent.futures import ThreadPoolExecutor


def dedup_dicts(list_of_dicts, key):
    """Deduplicate a list of dictionaries based on the given key.
    Preserves all dictionary items while deduplicating."""
    seen = set()
    result = []
    for d in list_of_dicts:
        if d[key] not in seen:
            seen.add(d[key])
            result.append(d)
    return result


def parse_and_store_index(urltemplate, posts_collection: db._Collection, parser_url=None, start_page=95, end_page=1000):
    """
    Scans index pages and stores articles in MongoDB
    - parser_url is used to parse individual page picked from index
    """

    if not parser_url:
        raise ValueError("parser_url is required")

    for page_num in range(start_page, end_page + 1):
        url = urltemplate.format(pageno=page_num)
        page = web.req(url)['data']

        # Extract article links
        urls = HTMLParser(page).css("div.wp-block-columns:nth-child(4) > div:nth-child(1) .loop-card__title-link")
        urls = [{"url": u.attributes['href']} for u in urls if u]
        urls = dedup_dicts(urls, key="url")
        posts_collection += urls  # Write with ignore dupes
        print(posts_collection.last_inserted)

        if not urls:
            # No more articles found
            break

    return posts_collection


def parse_geeksforgeeks_index(category="dsa", start_page=1, end_page=1000):
    """
    Scans GeeksForGeeks DSA index pages and stores articles in MongoDB using parallel threads
    """
    posts_collection = db.mongo()["TechNews"]["gfg"]
    posts_collection.create_index([("url", 1)], unique=True)

    urltemplate = "https://www.geeksforgeeks.org/category/dsa/{category}/page/{pageno}/?type=popular"

    def process_page(page_num):
        nonlocal posts_collection
        try:
            url = urltemplate.format(pageno=page_num, category=category)
            page = web.req(url)['data']
            parser = HTMLParser(page)

            urls = []
            for article in parser.css("a.article_heading"):
                urls.append({"url": article.attributes['href']})

            urls = dedup_dicts(urls, key="url")
            posts_collection += urls  # Write with ignore dupes
            print(f"Page {page_num}: Found {len(urls)} articles")

            # Rate limiting
            time.sleep(random.uniform(1, 3))

            return len(urls)
        except Exception as e:
            print(f"Error processing page {page_num}: {e}")
            return 0

    with ThreadPoolExecutor(max_workers=8) as executor:
        future_to_page = {executor.submit(process_page, page_num): page_num for page_num in range(start_page, end_page + 1)}

        for future in future_to_page:
            page_num = future_to_page[future]
            try:
                num_articles = future.result()
                if num_articles == 0:
                    print(f"No articles found on page {page_num}")
                    break
            except Exception as e:
                print(f"Error processing page {page_num}: {e}")

    return posts_collection


def mdfication(url, select="article"):
    md = web.to_md(web.req(url)['data'], select)
    md = re.sub(r"\n+", "\n", md)  # using regex if consequtive new niles replace to only 1 \n
    return md


def ai_summary(text, system_msg_profile="gfg"):
    SYSTEMS = {
        'techcrunch': {
            'system': """
                RULES:
                1. analyze this article in depth, in 300-500 words as Well formatted markdown, use only "h1, ### h3" heading for in content titles
                2. only give final output, no other explanations, no footer , no helper messages.  
                3. our publication name is swamix.com, so replace wherever possible as first person, for example, swamix reviewed, as per swamix analysis... etc, max 3 times in the body
                5. the title should be very clickbait, and catchy, engaging style, and overall content geared towards non tech saavy people, explain any phrases which may not understand.
                6. add intermittent explanations in block quotes, for even the slightest technical terms, in between
                7. decorate with alt codes characters/glyphs math symbols wherever possible, example for fractions ¼,  enumerate ¤ , « to enumerate
                8. since we are a consultancy, the implications/opportunities to business should be written from our perspective where end user is a business owner.
                Footer:
                - add a glossary for any other technical words.
                - add simple mermaid diagram with branches for logical overview, it should be atleast 3 levels deep, Title "swamix Logic diagram"
                - IMPORTANT: Creative call to action, and sense of urgency to book free call with swamix, 
                
                Sample mermaid diagram:
                ``` mermaid
                flowchart TD
                    A[Christmas] -->|Get money| B(Go shopping)
                    B --> C{Let me think}
                    C -->|One| D[Laptop]
                    C -->|Two| E[iPhone]
                    C -->|Three| F[fa:fa-car Car]
                ```
            """
        },
        'gfg': {
            'system': """
                You are a technical blog writer.
                approx words 500-5000.
                
                >> ALWAYS write in Programming Languages (ignore other c,cpp,java etc...):
                - python implementation
                - javascript implementation
                - RUST implementation
                
                >> Writing RULES:
                - if you encounter an index page with too many links, give the content within and try to expand as many concepts / code.
                - Important: Always prefer builtin implemmentation or import . allowed 3rd party is implementation is easy
                - Important: Put a TLDR at top with optional code snippets.
                - Put attractive title, 
                - rewrite in creative style, as a Company tone, our company name is swamix.com
                - well commented code
                - use blockquotes to explain any technical terms.
                
                >> Footer
                - Always include shortcut methods at the end
                - add a glossary for any other technical words.
            """.replace(
                "\t", ""
            ).replace(
                "  ", ""
            )
        },
    }
    msgs = [SYSTEMS[system_msg_profile], {'user': f"<article>{text}</article>"}]
    # print(msgs)
    resp = chat(msgs)

    meta = metadata["name == usage"]
    toks = meta[0]['oracle_llm_toks']

    metadata["name == usage"] = {"$inc": {"oracle_llm_toks.in": len(str(msgs)), "oracle_llm_toks.out": len(str(resp))}}
    print("io_toks:", toks['in'], toks['out'], "=>", toks['out'] + toks['in'])
    # _in += len(str(msgs))
    # _out += len(str(resp))
    # update count
    return resp


def map_reducer(colname, workers=100):
    col = db.mongo()["TechNews"][colname]
    col.create_index([("url", 1)], unique=True)
    shutdown = False
    LLLIMIT = 320_000_000
    docs = list(col["ai_summary ?? false"])
    # print(docs)
    if not docs:
        print("No more documents to process")
        return

    def process_doc(doc):
        if sum(metadata["name == usage"][0]['oracle_llm_toks'].values()) > LLLIMIT:
            print(f"INFO: Reached the allocated LLLIMIT {LLLIMIT}")
            executor.shutdown()

        time.sleep(random.random() * 5)
        try:
            print(f"Processing {doc['url']}")
            text = mdfication(doc["url"])
            col.update_one({"_id": doc["_id"]}, {"$set": {"text": text, "ai_summary": ai_summary(text)}})
        except Exception as e:
            # set ai summary and text to empty tring
            col.update_one({"_id": doc["_id"]}, {"$set": {"text": "", "ai_summary": ""}})
            print(f"Error processing {doc['url']}: {e}")

    with ThreadPoolExecutor(max_workers=workers) as executor:
        executor.map(process_doc, docs)


if __name__ == "__main__":
    # Initialize MongoDB collections
    metadata = db.mongo()["TechNews"]["metadata"]

    if not metadata["name == usage"]:
        print("creating tracker")
        metadata += {"name": "usage", "oracle_llm_toks": {"in": 0, "out": 0}}
    # print()
    # parse_geeksforgeeks_index()

    # ai = ai_summary(
    #     mdfication("https://www.geeksforgeeks.org/implement-stack-using-array/"),
    #     "gfg",
    # )
    # print(ai)
    map_reducer('gfg')

    # p = db.mongo()["TechNews"]["posts"]['ai_summary ?? false']

    # Parse and store TechCrunch AI articles
    # urltemplate = "https://techcrunch.com/category/artificial-intelligence/page/{pageno}/"
    # parse_and_store_index(urltemplate, posts, parser_url)
