from flask import Flask, render_template, request
from .search_akorda import search_akorda_db
from .repeats import is_similar

app = Flask(import_name=__name__)


@app.route(rule="/")
def hello() -> str:
    return render_template(template_name_or_list="search_akorda.html")


@app.route(rule="/search_akorda", methods=["GET", "POST"])
def search_akorda():
    if "query" not in request.form:
        return render_template(template_name_or_list="search_akorda.html")
    set_query = True
    search_query = request.form["query"]

    set_tok_check_box = False
    set_limit_20_check_box = False
    set_deduplicate_check_box = False

    if request.form.get(key="tok_check_box"):
        mode = "tokenized"
        set_tok_check_box = True
    else:
        mode = "default"

    if request.form.get(key="limit_20_check_box"):
        res_limit = 20
        set_limit_20_check_box = True
    else:
        res_limit = -1

    search_results = search_akorda_db(
        query=search_query, mode=mode, num_results=res_limit
    )

    if request.form.get(key="deduplicate_check_box"):
        dedup_results = list()
        dedup_results.append(search_results[0])
        for item in search_results[1:]:
            to_be_added = True
            for dedup_item in dedup_results:
                is_sim, _ = is_similar(str1=item[4], str2=dedup_item[4])
                if is_sim:
                    to_be_added = False
                    break
            if to_be_added:
                dedup_results.append(item)

        search_results = dedup_results
        set_deduplicate_check_box = True

    num_results = len(search_results)

    return render_template(
        template_name_or_list="search_akorda.html",
        search_query=search_query,
        search_results=search_results,
        num_results=num_results,
        set_tok_check_box=set_tok_check_box,
        set_limit_20_check_box=set_limit_20_check_box,
        set_deduplicate_check_box=set_deduplicate_check_box,
        set_query=set_query,
    )


app.run()
