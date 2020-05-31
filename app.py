from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, validators, RadioField
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'DontTellAnyone'
app.config["MONGO_URI"] = "mongodb://localhost:27017/BBC"
mongo = PyMongo(app)


class SearchForm(FlaskForm):  # Form structure
    pid = StringField('PID', default=' ', validators=[validators.Optional()])
    epoch_start = StringField('Start time', default=' ', validators=[validators.Optional()])
    epoch_end = StringField('End time', default=' ', validators=[validators.Optional()])
    complete_title = StringField('Complete title', default=' ', validators=[validators.Optional()])
    media_type = StringField('Media type', default=' ',
                             validators=[validators.Optional(), validators.AnyOf(values=['audio', 'video', ' ']),
                                         validators.Optional()])
    masterbrand = StringField(default=' ', validators=[validators.Optional()])
    service = StringField(default=' ', validators=[validators.Optional()])
    brand_pid = StringField(default=' ', validators=[validators.Optional()])
    is_clip = StringField('Is clip', default=' ',
                          validators=[validators.Optional(), validators.AnyOf(values=['1', '0', ' ']),
                                      validators.Optional()])
    categories = StringField(default=' ', validators=[validators.Optional()])
    tags = StringField(default=' ', validators=[validators.Optional()])
    order_by = SelectField(validators=[validators.Optional()],
                           choices=[('pid', 'pid'), ('epoch_start', 'start time'), ('epoch_end', 'end time'),
                                    ('complete_title', 'complete title'), ('media_type', 'media type'),
                                    ('service', 'service'), ('brand_pid', 'brand pid'),
                                    ('is_clip', 'is clip'), ('categories', 'categories'), ('tags', 'tags')])
    limit = IntegerField(default=7788, validators=[validators.Optional()])
    submit = SubmitField()
    or_and = RadioField(default='or', choices=[('or', 'or'), ('and', 'and')], validators=[validators.Optional()])


@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm(request.form)  ## create an object of the SearchForm

    pid = form.pid.data
    epoch_start = form.epoch_start.data
    epoch_end = form.epoch_end.data
    complete_title = form.complete_title.data
    media_type = form.media_type.data
    masterbrand = form.masterbrand.data
    service = form.service.data
    brand_pid = form.brand_pid.data
    is_clip = form.is_clip.data
    categories = form.categories.data
    tags = form.tags.data
    order_by = form.order_by.data
    limit = form.limit.data
    or_and = form.or_and.data


    if request.method == 'POST' and form.validate_on_submit():
        results = mongo.db.Program.find({'$' + or_and: [
            {'pid': {'$regex': pid}},
            {'complete_title': {'$regex': complete_title}},
            {'epoch_start': {'$regex': epoch_start}},
            {'epoch_end': {'$regex': epoch_end}},
            {'media_type': {'$regex': media_type}},
            {'masterbrand': {'$regex': masterbrand}},
            {'service': {'$regex': service}},
            {'brand_pid': {'$regex': brand_pid}},
            {'is_clip': {'$regex': is_clip}},
            {'categories': {'$regex': categories}},
            {'tags': {'$regex': tags}}
        ]}).sort(order_by).limit(limit)

        return render_template('index.html', results=results, form=form, count=results.count())
    return render_template("index.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)
    app.static_folder = 'static'
