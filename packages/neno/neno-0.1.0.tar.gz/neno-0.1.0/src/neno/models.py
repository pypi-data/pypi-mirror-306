from marshmallow import Schema, fields, validate
from enum import Enum

class FsBackendSchema(Schema):
  """Configuration for a filesystem backend.
  
  This configuration schema is used to configure both a data backend and a config backend,
  each of which store information as files on the filesystem. The main advantage of this backend
  is that it is very easy to set up and does not require any additional software to be installed.
  The main disadvantage is that it does not support clustering or high availability."""
  path = fields.String(required=True)

class DataBackendSchema(Schema):
  """Configuration for a data backend.
  
  A data backend is a system for storing deployed notebooks and the output of runs of those notebooks (including generated files)."""
  filesystem = fields.Nested(FsBackendSchema, required=False)

class ConfigBackendSchema(Schema):
  """Configuration for a config backend.
  
  A config backend is a system for storing and retrieving information about the noto cluster as well
  as the API resources that are currently deployed on the cluster. If the backend supports some form of clustering,
  then the config backend also handles the discovery of other noto instances in the cluster as well as role assignment."""
  filesystem = fields.Nested(FsBackendSchema, required=False)

class BackendsSchema(Schema):
  """Backend configuration for a noto instance.

  Each noto instance must have a data backend and a config backend.
  These backends are configured independently from each other by providing values
  in the `dataBackend` and `configBackend` fields.
  """
  dataBackend = fields.Nested(DataBackendSchema, required=True)
  configBackend = fields.Nested(ConfigBackendSchema, required=True)

class NotaConfigSchema(Schema):
  """Top-level schema for the config of a noto instance.
  
  This is where the hostname, port, and backends are defined.
  """
  host = fields.String(required=False, load_default='localhost')
  port = fields.Integer(required=False, load_default=5000)
  backends = fields.Nested(BackendsSchema, required=True)


KEEP_RUNS_CONFIG_ALWAYS = 'always'
KEEP_RUNS_CONFIG_FAILED = 'failed'
KEEP_RUNS_CONFIG_NEVER = 'never'


class RunOutputs(str, Enum):
  CELL = 'cell'
  HTML = 'html'
  NOTEBOOK = 'notebook'

# Possible values for the `output` field in an endpoint schema
# These values determine what the endpoint should return after a run
RUN_OUTPUT_CELL = RunOutputs.CELL.value # return either the content of the last output cell, or the content of the cell tagged "response"
RUN_OUTPUT_NOTEBOOK_HTML = RunOutputs.HTML.value # return the output notebook as HTML
RUN_OUTPUT_NOTEBOOK = RunOutputs.NOTEBOOK.value # return the output notebook as a .ipynb file

class EndpointSchema(Schema):
  name = fields.String(required=True)
  method = fields.String(required=False, load_default='GET')
  content_type = fields.String(required=False, load_default='application/json')
  kernel = fields.String(required=False, load_default='python3')
  keep_runs = fields.String(required=False, load_default=KEEP_RUNS_CONFIG_FAILED,
                            validate=validate.OneOf([KEEP_RUNS_CONFIG_ALWAYS, KEEP_RUNS_CONFIG_FAILED, KEEP_RUNS_CONFIG_NEVER]))
  notebook = fields.String(required=True)
  revision = fields.String(required=False)
  output = fields.String(required=False, default=RunOutputs.CELL.value,
                         validate=validate.OneOf([RunOutputs.CELL.value, RunOutputs.HTML.value, RunOutputs.NOTEBOOK.value]))

class ScheduledJobSchema(Schema):
  name = fields.String(required=True)
  endpointRef = fields.String(required=True)
  schedule = fields.String(required=True)

class EndpointRunSchema(Schema):
  id = fields.String(required=True)
  success = fields.Boolean(required=True)
  output_notebook = fields.String(required=True)
  endpoint = fields.Nested(EndpointSchema, required=True)
  error_message = fields.String(required=False, allow_none=True)
  timestamp = fields.Float(required=False)

class ConfigMapSchema(Schema):
  data = fields.Dict(required=True)
  name = fields.String(required=True)
