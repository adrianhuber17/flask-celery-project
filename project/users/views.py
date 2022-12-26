from flask import Blueprint,jsonify,render_template
from . import users_blueprint
from project.users.forms import YourForm
import requests


@users_blueprint.route('/webhook_test/', methods=('POST', ))
@csrf.exempt
def webhook_test():
    if not random.choice([0, 1]):
        # mimic an error
        raise Exception()

    # blocking process
    requests.post('https://httpbin.org/delay/5')
    return 'pong'

@users_blueprint.route('/form_ws/', methods=('GET', 'POST'))
def subscribe_ws():
    form = YourForm()
    if form.validate_on_submit():
        task = sample_task.delay(form.email.data)
        return jsonify({
            'task_id': task.task_id,
        })
    return render_template('form_ws.html', form=form)