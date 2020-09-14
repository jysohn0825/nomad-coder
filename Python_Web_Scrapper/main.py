from flask import Flask, render_template, request, send_file
from scrap import scrapping
import csv

db={}

app = Flask("Challenge")

@app.route("/")
def honme():
  return render_template("home.html")

@app.route("/search")
def search():
  term = request.args.get("term").lower()
  db, count = scrapping(term)
  return render_template("read.html", infos = db[term],count = count, term = term)

@app.route("/export/<term>", methods=['GET'])
def export(term):
  db, count = scrapping(term)
  file = open(f"{term}.csv", mode="w")
  writer = csv.writer(file)
  writer.writerow(["Title", "Company", "Link"])
  for scrap in db[term]:
    writer.writerow([scrap["title"],scrap["name"],scrap["link"]])  
  file.close
  return send_file(f"{term}.csv", as_attachment = True, attachment_filename = f"{term}.csv", cache_timeout=0 )

@app.after_request
def add_header(request):
    request.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    request.headers["Pragma"] = "no-cache"
    request.headers["Expires"] = "0"
    request.headers['Cache-Control'] = 'public, max-age=0'
    return request
  
app.run(host="0.0.0.0")
