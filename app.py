
# A very simple Flask Hello World app for you to get started with...

#from fileinput import filename
from flask import Flask, render_template, request
import pandas as pd, re, peptide


app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/')
def index():
    return render_template("peptide_page.html")

@app.route('/success', methods = ['POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        raw_data = pd.read_excel(f)

        i = 0
        header = 0
        molecular_ion = "not found"
        while i < len(raw_data):
            if (isinstance(raw_data.iloc[i, 0], str) and re.search(r".*mass.*",  raw_data.iloc[i, 0], re.I)):
                header = i+1

            if (isinstance(raw_data.iloc[i, 0], str) and "ms2" in raw_data.iloc[i, 0]):
                molecular_ion = float(re.search(r".*ms2 *([0-9.]+)@.*",  raw_data.iloc[i, 0], re.I).group(1))

            i+=1
        raw_data = pd.read_excel(f, header=header)

        raw_data["NL"] = abs(raw_data["Mass"] - molecular_ion)

        tolerance = request.form.get("tolerance", default = 0.01)
        tolerance = request.form.get("tolerance")


        matches_unstable = peptide.Amino_acid_list(stable = False)

        if matches_unstable.endterminal_search(raw_data["NL"], tolerance):
            matches_unstable.nonterminal_search(raw_data["Mass"], molecular_ion, tolerance)

    #     matches_unstable.print_list()
    #   #  data_file_unstable = pd.DataFrame(matches_unstable.list)

    #     matches_unstable.clear()

        return render_template("peptide_page.html", upload=f.filename + " uploaded successfully!", molecular_ion=tolerance) + raw_data.to_html() + matches_unstable.to_html()

@app.route('/process', methods = ['POST'])
def process():
    return "process"

# if __name__ == '__main__':
#     app.run(debug=True)