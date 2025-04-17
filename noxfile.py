import nox

# imports all nox task provided by the toolbox
from exasol.toolbox.nox.tasks import *  # type: ignore

from exasol_script_languages_container_ci.lib.config.data_model_generator import config_data_model_default_output_file, \
    generate_config_data_model

# default actions to be run if nothing is explicitly specified with the -s option
nox.options.sessions = ["project:fix"]


@nox.session(name="regenerate-config-model", python=False)
def run_regenerate_config_model(session: nox.Session):
    """
    Updates the `exasol/slc_ci/lib/config/config_data_model.py` from `exasol/slc_ci/lib/templates/config_schema.json`
    """
    outfile = config_data_model_default_output_file()
    generate_config_data_model(outfile)
