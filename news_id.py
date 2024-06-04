import flask
from flask import jsonify
from data.jobs import Jobs

from data import db_session

blueprint = flask.Blueprint('jobs_api', __name__,
                            template_folder='templates')


@blueprint.route('/api/jobs/<int:job_id>')
def get_jobs(jobs_id):
    session = db_session.create_session()
    jobs = session.query(Jobs).filter(Jobs.id == jobs_id)
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=(
                    'id', 'team_leader', 'job', 'work_size', 'collaborators', 'start_date',
                    'end_date', 'is_finished'))
                    for item in jobs]
        }
    )
