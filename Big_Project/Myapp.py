import cso
import visual_data as vs
import sql_connector as sc
from flask import Flask, jsonify, render_template
import requests

cso.getFormattedAsFile(cso.covid_rates, cso.covid_cso)
cso.getFormattedAsFile(cso.death_rates, cso.death_rates_cso)
cso.getFormattedAsFile(cso.vaccination_rates, cso.vaccination_rates_cso)
vs.tables_and_bar_plot()
sc.sql_database_set_up()
import sql_dao as sd
sd.create_covid_rates_plot()
sd.create_death_rates_plot()
sd.create_vaccination_rates_plots()

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')

def main_page():
    return render_template('index.html')

@app.route('/page1')

def page1():
    # Include any dynamic content you want to pass to the template
    return render_template('page1.html', table1=vs.dublin_stats, table2=vs.cork_stats, table3=vs.gal_stats, table4=vs.lim_stats)

@app.route('/page2')

def page2():
    # Include any dynamic content you want to pass to the template
    return render_template('page2.html')

if __name__ == '__main__':
    app.run(debug=True)



