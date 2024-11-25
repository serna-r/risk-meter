from flask import Flask, render_template, redirect, url_for, session
from form import RiskForm
from config import Config
from packages.calculate_risks import calculate_risk, plot_radar_risk_dimensions, get_risk_color_class, evaluate_compliance


app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form', methods=['GET', 'POST'])
def form():
    form = RiskForm()
    if form.validate_on_submit():
        # Store individual responses in the session
        session['min_length'] = form.min_length.data
        session['min_mask'] = form.min_mask.data
        session['extra_sec'] = form.extra_sec.data
        session['NIST_compliance_score'] = evaluate_compliance(form.min_length.data, form.min_mask.data, form.extra_sec.data)
        session['two_factor'] = form.two_factor.data
        session['risk_data_exp'] = form.risk_data_exp.data
        session['risk_appetite'] = int(form.risk_appetite.data[0])

        # Calculate the risk scores based on the selected elements
        risk_scores, risk_scores_weighted = calculate_risk(form.risk_data_exp.data, int(form.risk_appetite.data[0]))
        
        # Generate the radar plot and get the image path
        plot_filename = plot_radar_risk_dimensions(risk_scores, risk_scores_weighted, "Service Risk Profile", app.config['GENERATED_IMAGE_FOLDER'])

        # Store the results in the session
        session['risk_scores'] = risk_scores
        session['risk_scores_weighted'] = risk_scores_weighted
        session['plot_filename'] = plot_filename
        
        return redirect(url_for('results'))
    return render_template('form.html', title='Form', form=form)

@app.route('/results', methods=['GET'])
def results():
    # Retrieve risk scores, plot path, and other user responses from the session
    risk_scores = session.get('risk_scores', {})
    risk_scores_weighted = session.get('risk_scores_weighted', {})
    plot_filename = session.get('plot_filename', None)
    
    # Calculate totals
    totals = [sum(risk_scores.values()), sum(risk_scores_weighted.values())]
    
    # Get color scales
    total_normal_color_class = get_risk_color_class(totals[0])
    total_weighted_color_class = get_risk_color_class(totals[1])

    return render_template(
        'results.html', 
        risk_scores=risk_scores,
        risk_scores_weighted=risk_scores_weighted,
        total_normal_color_class=total_normal_color_class,
        total_weighted_color_class=total_weighted_color_class,
        plot_filename=plot_filename, 
        totals=totals
    )

