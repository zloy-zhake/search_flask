from flask import Flask, render_template, request, redirect, url_for
from .search_akorda import search_akorda_db

app = Flask(import_name=__name__)


@app.route(rule="/")
def hello() -> str:
    return render_template(template_name_or_list="search_akorda.html")


@app.route(rule="/search_akorda", methods=["GET", "POST"])
def search_akorda():
    if "query" not in request.form:
        return render_template(template_name_or_list="search_akorda.html")
    search_query = request.form["query"]

    # if request.form["tok_check_box"]:
    #     search_result = search_akorda_db(query=search_query, mode="tokenized")
    # else:
    #     search_result = search_akorda_db(query=search_query, mode="default")
    search_results = search_akorda_db(query=search_query, mode="default")

    num_found = len(search_results)
    # if self.tokenization_check_box.isChecked():
    #     output = "Tokenized search mode is on.\n\n"
    # else:
    #     output = ""
    # output = ""
    # output += f"{num_found} құжат табылды.<br />"
    # output += "<br />"
    # ind = 0
    # for found_item in search_result:
    #     ind += 1
    #     output += str(ind) + ": "
    #     output += "url-адрес:<br />" + found_item[0] + "<br />"
    #     if found_item[1] != "":
    #         output += "Тақырыптық бөлімі:<br />" + found_item[1]
    #         output += "<br />"
    #     output += "Құжат тақырыбы:<br />" + found_item[2]
    #     output += "<br />"
    #     output += "Уақыты:<br />" + found_item[3]
    #     output += "<br />"
    #     output += "<br />"
    return render_template(
        template_name_or_list="search_akorda.html",
        search_results=search_results,
    )


app.run()