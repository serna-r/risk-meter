from flask import Flask, render_template, flash, redirect
from form import RiskForm
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form', methods=['GET', 'POST'])
def form():
    form = RiskForm()
    if form.validate_on_submit():
        flash('Min length {}, Min mask {}, Extra sec {}'.format(
            form.min_length.data, form.min_mask.data, form.extra_sec.data))
        return redirect('/')
    return render_template('form.html', title='Form', form=form)